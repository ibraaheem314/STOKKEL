"""
Exceptions personnalisées pour Stokkel
Gestion centralisée des erreurs métier
"""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class StokkelException(Exception):
    """Exception de base Stokkel"""
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code or "STOKKEL_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class InsufficientDataError(StokkelException):
    """Données insuffisantes pour générer une prévision"""
    def __init__(self, message: str, min_required: int = 30, actual: int = 0):
        super().__init__(
            message=message,
            error_code="INSUFFICIENT_DATA",
            details={
                "min_required": min_required,
                "actual": actual,
                "recommendation": f"Fournir au moins {min_required} jours d'historique de ventes"
            }
        )


class ModelTrainingError(StokkelException):
    """Erreur lors de l'entraînement du modèle"""
    def __init__(self, message: str, model_type: str = "Prophet", details: Dict[str, Any] = None):
        super().__init__(
            message=message,
            error_code="MODEL_TRAINING_ERROR",
            details={
                "model_type": model_type,
                **(details or {})
            }
        )


class InvalidProductError(StokkelException):
    """Produit inexistant ou invalide"""
    def __init__(self, product_id: str, available_products: list = None):
        super().__init__(
            message=f"Produit '{product_id}' inexistant",
            error_code="INVALID_PRODUCT",
            details={
                "product_id": product_id,
                "available_products": available_products or [],
                "recommendation": "Vérifier l'identifiant du produit ou uploader des données"
            }
        )


class DataValidationError(StokkelException):
    """Erreur de validation des données"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        super().__init__(
            message=message,
            error_code="DATA_VALIDATION_ERROR",
            details={
                "field": field,
                "value": str(value) if value is not None else None,
                "recommendation": "Vérifier le format et la qualité des données"
            }
        )


class ForecastError(StokkelException):
    """Erreur lors de la génération de prévision"""
    def __init__(self, message: str, product_id: str = None, horizon_days: int = None):
        super().__init__(
            message=message,
            error_code="FORECAST_ERROR",
            details={
                "product_id": product_id,
                "horizon_days": horizon_days,
                "recommendation": "Vérifier la qualité des données historiques"
            }
        )


class OptimizationError(StokkelException):
    """Erreur lors de l'optimisation des stocks"""
    def __init__(self, message: str, product_id: str = None, parameters: Dict[str, Any] = None):
        super().__init__(
            message=message,
            error_code="OPTIMIZATION_ERROR",
            details={
                "product_id": product_id,
                "parameters": parameters or {},
                "recommendation": "Vérifier les paramètres d'optimisation"
            }
        )


class AuthenticationError(StokkelException):
    """Erreur d'authentification"""
    def __init__(self, message: str = "Token d'authentification invalide"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            details={
                "recommendation": "Se reconnecter ou vérifier les credentials"
            }
        )


class RateLimitError(StokkelException):
    """Limite de taux dépassée"""
    def __init__(self, message: str, limit: int = None, window: str = None):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_ERROR",
            details={
                "limit": limit,
                "window": window,
                "recommendation": "Attendre avant de refaire une requête"
            }
        )


# Fonctions utilitaires pour convertir les exceptions
def convert_to_http_exception(exc: StokkelException) -> HTTPException:
    """Convertit une exception Stokkel en HTTPException"""
    
    # Mapping des codes d'erreur vers les codes HTTP
    error_code_mapping = {
        "INSUFFICIENT_DATA": status.HTTP_400_BAD_REQUEST,
        "INVALID_PRODUCT": status.HTTP_404_NOT_FOUND,
        "DATA_VALIDATION_ERROR": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "MODEL_TRAINING_ERROR": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "FORECAST_ERROR": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "OPTIMIZATION_ERROR": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "AUTHENTICATION_ERROR": status.HTTP_401_UNAUTHORIZED,
        "RATE_LIMIT_ERROR": status.HTTP_429_TOO_MANY_REQUESTS,
        "STOKKEL_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    
    http_status = error_code_mapping.get(exc.error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return HTTPException(
        status_code=http_status,
        detail={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )


def handle_stokkel_exception(exc: StokkelException) -> HTTPException:
    """Gère une exception Stokkel et retourne une réponse HTTP appropriée"""
    return convert_to_http_exception(exc)
