"""
Système de cache avec Redis (production) ou dict (dev)
"""

from typing import Optional, Any
import json
import pickle
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class CacheBackend(ABC):
    """Interface de cache"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        pass
    
    @abstractmethod
    def delete(self, key: str):
        pass
    
    @abstractmethod
    def clear(self):
        pass

class DictCache(CacheBackend):
    """Cache en mémoire (dev)"""
    
    def __init__(self):
        self._cache = {}
        logger.info("🗄️ Cache en mémoire initialisé")
    
    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        self._cache[key] = value
        logger.debug(f"💾 Cache set | key={key}")
    
    def delete(self, key: str):
        self._cache.pop(key, None)
        logger.debug(f"🗑️ Cache delete | key={key}")
    
    def clear(self):
        self._cache.clear()
        logger.info("🗑️ Cache complet nettoyé")

class RedisCache(CacheBackend):
    """Cache Redis (production)"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        try:
            import redis
            self.client = redis.from_url(redis_url, decode_responses=False)
            # Test de connexion
            self.client.ping()
            logger.info(f"🔴 Cache Redis initialisé | url={redis_url}")
        except ImportError:
            logger.error("❌ Redis non installé. Utilisation du cache en mémoire.")
            raise ImportError("Redis non installé. Installez avec: pip install redis")
        except Exception as e:
            logger.error(f"❌ Erreur connexion Redis: {e}. Utilisation du cache en mémoire.")
            raise ConnectionError(f"Impossible de se connecter à Redis: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.client.get(key)
            if value is None:
                return None
            return pickle.loads(value)
        except Exception as e:
            logger.error(f"❌ Erreur cache get | key={key} error={e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        try:
            pickled = pickle.dumps(value)
            if ttl:
                self.client.setex(key, ttl, pickled)
            else:
                self.client.set(key, pickled)
            logger.debug(f"💾 Cache Redis set | key={key} ttl={ttl}")
        except Exception as e:
            logger.error(f"❌ Erreur cache set | key={key} error={e}")
    
    def delete(self, key: str):
        try:
            self.client.delete(key)
            logger.debug(f"🗑️ Cache Redis delete | key={key}")
        except Exception as e:
            logger.error(f"❌ Erreur cache delete | key={key} error={e}")
    
    def clear(self):
        try:
            self.client.flushdb()
            logger.info("🗑️ Cache Redis complet nettoyé")
        except Exception as e:
            logger.error(f"❌ Erreur cache clear | error={e}")

# Factory
def create_cache() -> CacheBackend:
    """Crée le cache selon l'environnement"""
    from .config import settings
    
    if hasattr(settings, 'redis_url') and settings.redis_url:
        try:
            return RedisCache(settings.redis_url)
        except (ImportError, ConnectionError):
            logger.warning("⚠️ Redis non disponible, utilisation du cache en mémoire")
            return DictCache()
    else:
        return DictCache()

# Instance globale
cache = create_cache()