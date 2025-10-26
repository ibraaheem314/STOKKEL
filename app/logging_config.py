"""
Configuration du logging structuré pour Stokkel
Logs JSON pour faciliter l'analyse et le monitoring
"""

import logging
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional
import traceback
from pathlib import Path

class JSONFormatter(logging.Formatter):
    """Formateur JSON pour les logs structurés"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Formate un log record en JSON"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread": record.thread,
            "process": record.process
        }
        
        # Ajouter les champs personnalisés
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'product_id'):
            log_entry['product_id'] = record.product_id
        if hasattr(record, 'duration_ms'):
            log_entry['duration_ms'] = record.duration_ms
        if hasattr(record, 'status_code'):
            log_entry['status_code'] = record.status_code
        if hasattr(record, 'error_code'):
            log_entry['error_code'] = record.error_code
        
        # Ajouter l'exception si présente
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_entry, ensure_ascii=False)

class StokkelLogger:
    """Logger personnalisé pour Stokkel avec contexte métier"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Éviter les doublons
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configure les handlers de logging"""
        # Handler console avec format JSON
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(console_handler)
        
        # Handler fichier pour les logs persistants
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f"stokkel_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(file_handler)
    
    def info(self, message: str, **kwargs):
        """Log info avec contexte métier"""
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning avec contexte métier"""
        self._log_with_context(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error avec contexte métier"""
        self._log_with_context(logging.ERROR, message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug avec contexte métier"""
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def _log_with_context(self, level: int, message: str, **kwargs):
        """Log avec contexte métier"""
        # Créer un record avec les champs personnalisés
        record = self.logger.makeRecord(
            self.logger.name, level, "", 0, message, (), None
        )
        
        # Ajouter les champs personnalisés
        for key, value in kwargs.items():
            setattr(record, key, value)
        
        self.logger.handle(record)

# Loggers spécialisés
def get_logger(name: str) -> StokkelLogger:
    """Obtient un logger Stokkel"""
    return StokkelLogger(name)

# Loggers métier
api_logger = get_logger("stokkel.api")
auth_logger = get_logger("stokkel.auth")
forecast_logger = get_logger("stokkel.forecast")
optimization_logger = get_logger("stokkel.optimization")
data_logger = get_logger("stokkel.data")

# Configuration du logging global
def setup_logging():
    """Configure le logging global pour l'application"""
    
    # Niveau de logging
    log_level = logging.INFO
    
    # Configuration du root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Supprimer les handlers existants
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Handler console avec format JSON
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)
    
    # Handler fichier
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(
        log_dir / f"stokkel_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(file_handler)
    
    # Configuration des loggers spécifiques
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    return root_logger

# Fonctions utilitaires pour le logging métier
def log_api_request(method: str, path: str, status_code: int, duration_ms: float, user_id: str = None):
    """Log une requête API"""
    api_logger.info(
        f"API Request: {method} {path}",
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=duration_ms,
        user_id=user_id
    )

def log_forecast_request(product_id: str, horizon_days: int, user_id: str = None):
    """Log une demande de prévision"""
    forecast_logger.info(
        f"Forecast request for product {product_id}",
        product_id=product_id,
        horizon_days=horizon_days,
        user_id=user_id
    )

def log_forecast_result(product_id: str, success: bool, duration_ms: float, mape: float = None):
    """Log le résultat d'une prévision"""
    level = logging.INFO if success else logging.ERROR
    message = f"Forecast {'completed' if success else 'failed'} for {product_id}"
    
    forecast_logger._log_with_context(
        level,
        message,
        product_id=product_id,
        success=success,
        duration_ms=duration_ms,
        mape=mape
    )

def log_optimization_request(product_id: str, current_stock: float, user_id: str = None):
    """Log une demande d'optimisation"""
    optimization_logger.info(
        f"Optimization request for product {product_id}",
        product_id=product_id,
        current_stock=current_stock,
        user_id=user_id
    )

def log_data_upload(filename: str, rows_count: int, user_id: str = None):
    """Log un upload de données"""
    data_logger.info(
        f"Data upload: {filename}",
        filename=filename,
        rows_count=rows_count,
        user_id=user_id
    )

def log_auth_event(event: str, username: str, success: bool):
    """Log un événement d'authentification"""
    level = logging.INFO if success else logging.WARNING
    message = f"Auth {event}: {username} ({'success' if success else 'failed'})"
    
    auth_logger._log_with_context(
        level,
        message,
        event=event,
        username=username,
        success=success
    )
