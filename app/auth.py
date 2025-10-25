"""
Système d'authentification JWT pour Stokkel
Gère l'authentification sécurisée des utilisateurs
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import secrets
import os
from .config import settings

# Configuration JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Configuration du hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Base de données utilisateurs (en production, utiliser une vraie DB)
# Mots de passe: admin=secret, demo=demo
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "email": "admin@stokkel.sn",
        "role": "admin",
        "company": "Stokkel"
    },
    "demo": {
        "username": "demo",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # demo
        "email": "demo@stokkel.sn",
        "role": "user",
        "company": "Demo Company"
    }
}

class User:
    """Modèle utilisateur"""
    def __init__(self, username: str, email: str, role: str, company: str):
        self.username = username
        self.email = email
        self.role = role
        self.company = company

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash un mot de passe"""
    return pwd_context.hash(password)

def get_user(username: str) -> Optional[User]:
    """Récupère un utilisateur depuis la DB"""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return User(
            username=user_dict["username"],
            email=user_dict["email"],
            role=user_dict["role"],
            company=user_dict["company"]
        )
    return None

def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authentifie un utilisateur"""
    user = get_user(username)
    if not user:
        return None
    
    # Pour l'instant, vérification simple (en production, utiliser bcrypt)
    if username == "admin" and password == "secret":
        return user
    elif username == "demo" and password == "demo":
        return user
    
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crée un JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Valide le token et retourne l'utilisateur actuel"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Retourne l'utilisateur actif"""
    return current_user

def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Vérifie que l'utilisateur est admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Endpoints d'authentification
from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint de connexion - retourne un token JWT"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "company": user.company
        }
    }

@auth_router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Retourne les informations de l'utilisateur connecté"""
    return {
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "company": current_user.company
    }

@auth_router.post("/register")
async def register_user(username: str, email: str, password: str, company: str):
    """Enregistre un nouvel utilisateur (en production, utiliser une vraie DB)"""
    if username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(password)
    fake_users_db[username] = {
        "username": username,
        "hashed_password": hashed_password,
        "email": email,
        "role": "user",
        "company": company
    }
    
    return {"message": "User registered successfully"}

@auth_router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_active_user)):
    """Rafraîchit le token JWT"""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
