"""
Système de monitoring avec Prometheus pour Stokkel
Collecte des métriques de performance et d'usage
"""

from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

# Métriques de base
REQUEST_COUNT = Counter(
    'stokkel_requests_total', 
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'stokkel_request_duration_seconds',
    'Request latency in seconds',
    ['endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'stokkel_active_connections',
    'Number of active connections'
)

# Métriques métier
FORECAST_REQUESTS = Counter(
    'stokkel_forecast_requests_total',
    'Total number of forecast requests',
    ['product_id', 'horizon_days']
)

FORECAST_LATENCY = Histogram(
    'stokkel_forecast_duration_seconds',
    'Forecast generation latency',
    ['product_id']
)

FORECAST_ACCURACY = Gauge(
    'stokkel_forecast_mape',
    'Forecast MAPE (Mean Absolute Percentage Error)',
    ['product_id']
)

OPTIMIZATION_REQUESTS = Counter(
    'stokkel_optimization_requests_total',
    'Total number of optimization requests',
    ['product_id']
)

OPTIMIZATION_LATENCY = Histogram(
    'stokkel_optimization_duration_seconds',
    'Optimization generation latency',
    ['product_id']
)

DATA_UPLOADS = Counter(
    'stokkel_data_uploads_total',
    'Total number of data uploads',
    ['user_id']
)

DATA_ROWS_PROCESSED = Counter(
    'stokkel_data_rows_processed_total',
    'Total number of data rows processed'
)

# Métriques système
MODEL_CACHE_SIZE = Gauge(
    'stokkel_model_cache_size',
    'Number of cached models'
)

MODEL_TRAINING_TIME = Histogram(
    'stokkel_model_training_duration_seconds',
    'Model training duration',
    ['product_id']
)

MEMORY_USAGE = Gauge(
    'stokkel_memory_usage_bytes',
    'Memory usage in bytes'
)

# Métriques d'authentification
AUTH_ATTEMPTS = Counter(
    'stokkel_auth_attempts_total',
    'Total authentication attempts',
    ['username', 'success']
)

AUTH_FAILURES = Counter(
    'stokkel_auth_failures_total',
    'Total authentication failures',
    ['reason']
)

# Métriques d'erreurs
ERROR_COUNT = Counter(
    'stokkel_errors_total',
    'Total number of errors',
    ['error_type', 'endpoint']
)

class MetricsCollector:
    """Collecteur de métriques pour Stokkel"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.start_time = time.time()
    
    def record_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Enregistre une requête API"""
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=status_code
        ).inc()
        
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
    
    def record_forecast(self, product_id: str, horizon_days: int, duration: float, mape: float = None):
        """Enregistre une prévision"""
        FORECAST_REQUESTS.labels(
            product_id=product_id,
            horizon_days=horizon_days
        ).inc()
        
        FORECAST_LATENCY.labels(product_id=product_id).observe(duration)
        
        if mape is not None:
            FORECAST_ACCURACY.labels(product_id=product_id).set(mape)
    
    def record_optimization(self, product_id: str, duration: float):
        """Enregistre une optimisation"""
        OPTIMIZATION_REQUESTS.labels(product_id=product_id).inc()
        OPTIMIZATION_LATENCY.labels(product_id=product_id).observe(duration)
    
    def record_data_upload(self, user_id: str, rows_count: int):
        """Enregistre un upload de données"""
        DATA_UPLOADS.labels(user_id=user_id).inc()
        DATA_ROWS_PROCESSED.inc(rows_count)
    
    def record_auth_attempt(self, username: str, success: bool):
        """Enregistre une tentative d'authentification"""
        AUTH_ATTEMPTS.labels(
            username=username,
            success=str(success)
        ).inc()
        
        if not success:
            AUTH_FAILURES.labels(reason="invalid_credentials").inc()
    
    def record_error(self, error_type: str, endpoint: str):
        """Enregistre une erreur"""
        ERROR_COUNT.labels(
            error_type=error_type,
            endpoint=endpoint
        ).inc()
    
    def update_model_cache_size(self, size: int):
        """Met à jour la taille du cache des modèles"""
        MODEL_CACHE_SIZE.set(size)
    
    def record_model_training(self, product_id: str, duration: float):
        """Enregistre l'entraînement d'un modèle"""
        MODEL_TRAINING_TIME.labels(product_id=product_id).observe(duration)
    
    def update_memory_usage(self, usage_bytes: int):
        """Met à jour l'utilisation mémoire"""
        MEMORY_USAGE.set(usage_bytes)
    
    def get_uptime_seconds(self) -> float:
        """Retourne le temps de fonctionnement en secondes"""
        return time.time() - self.start_time

# Instance globale
metrics_collector = MetricsCollector()

# Middleware pour collecter automatiquement les métriques
class MetricsMiddleware:
    """Middleware pour collecter automatiquement les métriques"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        method = scope["method"]
        path = scope["path"]
        
        # Déterminer l'endpoint pour les métriques
        endpoint = self._get_endpoint_category(path)
        
        # Traiter la requête
        status_code = 200
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            status_code = 500
            metrics_collector.record_error("internal_error", endpoint)
            raise
        finally:
            # Enregistrer les métriques
            duration = time.time() - start_time
            metrics_collector.record_request(method, endpoint, status_code, duration)
    
    def _get_endpoint_category(self, path: str) -> str:
        """Détermine la catégorie d'endpoint pour les métriques"""
        if path.startswith("/auth/"):
            return "auth"
        elif path.startswith("/forecast/"):
            return "forecast"
        elif path.startswith("/recommendation/"):
            return "optimization"
        elif path.startswith("/upload"):
            return "data_upload"
        elif path == "/health":
            return "health"
        else:
            return "other"

# Fonctions utilitaires pour le monitoring
def start_metrics_server(port: int = 9090):
    """Démarre le serveur de métriques Prometheus"""
    try:
        start_http_server(port)
        logging.info(f"Metrics server started on port {port}")
        return True
    except Exception as e:
        logging.error(f"Failed to start metrics server: {e}")
        return False

def get_system_metrics() -> Dict[str, Any]:
    """Retourne les métriques système actuelles"""
    import psutil
    
    return {
        "uptime_seconds": metrics_collector.get_uptime_seconds(),
        "memory_usage_bytes": psutil.Process().memory_info().rss,
        "cpu_percent": psutil.cpu_percent(),
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "timestamp": datetime.utcnow().isoformat()
    }

# Décorateur pour mesurer automatiquement les performances
def measure_performance(metric_name: str):
    """Décorateur pour mesurer automatiquement les performances"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Enregistrer la métrique
                if metric_name == "forecast":
                    product_id = kwargs.get('product_id', 'unknown')
                    metrics_collector.record_forecast(product_id, 30, duration)
                elif metric_name == "optimization":
                    product_id = kwargs.get('product_id', 'unknown')
                    metrics_collector.record_optimization(product_id, duration)
                
                return result
            except Exception as e:
                duration = time.time() - start_time
                metrics_collector.record_error(metric_name, "error")
                raise
        return wrapper
    return decorator
