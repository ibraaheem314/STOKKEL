"""
Système de métriques pour monitoring de la qualité des prévisions
Version: 1.0.0
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class ForecastMetrics:
    """Métriques d'une prévision individuelle"""
    product_id: str
    timestamp: datetime
    horizon_days: int
    mape: float
    mae: float
    rmse: float
    training_points: int
    duration_seconds: float
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire sérialisable"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


class MetricsCollector:
    """Collecteur et analyseur de métriques"""
    
    def __init__(self, metrics_dir: Optional[Path] = None):
        from config import settings
        self.metrics_dir = Path(metrics_dir or settings.metrics_dir)
        self.metrics_dir.mkdir(exist_ok=True)
        logger.info(f"📊 MetricsCollector initialisé: {self.metrics_dir}")
    
    def record_forecast(self, metrics: ForecastMetrics):
        """
        Enregistre les métriques d'une prévision
        
        Args:
            metrics: Métriques à enregistrer
        """
        try:
            # Fichier JSONL par produit
            product_file = self.metrics_dir / f"{metrics.product_id}_metrics.jsonl"
            
            with open(product_file, 'a') as f:
                json.dump(metrics.to_dict(), f)
                f.write('\n')
            
            logger.debug(
                f"📝 Métriques enregistrées | "
                f"product={metrics.product_id} mape={metrics.mape:.2f}%"
            )
        
        except Exception as e:
            logger.error(f"⚠️ Erreur enregistrement métriques: {e}")
    
    def get_metrics_history(
        self,
        product_id: str,
        last_n: Optional[int] = None
    ) -> List[Dict]:
        """
        Récupère l'historique des métriques d'un produit
        
        Args:
            product_id: Identifiant du produit
            last_n: Nombre de métriques à récupérer (None = toutes)
            
        Returns:
            Liste des métriques
        """
        product_file = self.metrics_dir / f"{product_id}_metrics.jsonl"
        
        if not product_file.exists():
            return []
        
        metrics = []
        with open(product_file, 'r') as f:
            for line in f:
                metrics.append(json.loads(line))
        
        if last_n:
            return metrics[-last_n:]
        return metrics
    
    def get_quality_trend(
        self,
        product_id: str,
        last_n: int = 10
    ) -> Dict:
        """
        Analyse la tendance de qualité des prévisions
        
        Args:
            product_id: Identifiant du produit
            last_n: Nombre de prévisions à analyser
            
        Returns:
            Dictionnaire avec statistiques et tendance
        """
        metrics = self.get_metrics_history(product_id, last_n)
        
        if not metrics:
            return {
                "product_id": product_id,
                "error": "Aucune métrique disponible",
                "forecasts_count": 0
            }
        
        # Calculer les moyennes
        avg_mape = sum(m['mape'] for m in metrics) / len(metrics)
        avg_mae = sum(m['mae'] for m in metrics) / len(metrics)
        avg_rmse = sum(m['rmse'] for m in metrics) / len(metrics)
        avg_duration = sum(m['duration_seconds'] for m in metrics) / len(metrics)
        
        # Déterminer la tendance
        if len(metrics) >= 2:
            recent_mape = metrics[-1]['mape']
            previous_avg_mape = sum(m['mape'] for m in metrics[:-1]) / (len(metrics) - 1)
            
            if recent_mape < previous_avg_mape * 0.9:
                trend = "amélioration"
                trend_emoji = "📈"
            elif recent_mape > previous_avg_mape * 1.1:
                trend = "dégradation"
                trend_emoji = "📉"
            else:
                trend = "stable"
                trend_emoji = "➡️"
        else:
            trend = "insuffisant"
            trend_emoji = "⚠️"
        
        return {
            "product_id": product_id,
            "forecasts_analyzed": len(metrics),
            "average_mape": round(avg_mape, 2),
            "average_mae": round(avg_mae, 2),
            "average_rmse": round(avg_rmse, 2),
            "average_duration_seconds": round(avg_duration, 2),
            "quality_trend": trend,
            "trend_emoji": trend_emoji,
            "latest_mape": round(metrics[-1]['mape'], 2) if metrics else None,
            "best_mape": round(min(m['mape'] for m in metrics), 2),
            "worst_mape": round(max(m['mape'] for m in metrics), 2)
        }
    
    def get_global_stats(self) -> Dict:
        """
        Récupère les statistiques globales de toutes les prévisions
        
        Returns:
            Statistiques agrégées
        """
        all_metrics = []
        
        # Charger toutes les métriques
        for metrics_file in self.metrics_dir.glob("*_metrics.jsonl"):
            product_id = metrics_file.stem.replace('_metrics', '')
            metrics = self.get_metrics_history(product_id)
            all_metrics.extend(metrics)
        
        if not all_metrics:
            return {
                "total_forecasts": 0,
                "unique_products": 0,
                "message": "Aucune métrique disponible"
            }
        
        return {
            "total_forecasts": len(all_metrics),
            "unique_products": len(list(self.metrics_dir.glob("*_metrics.jsonl"))),
            "average_mape": round(sum(m['mape'] for m in all_metrics) / len(all_metrics), 2),
            "average_duration": round(sum(m['duration_seconds'] for m in all_metrics) / len(all_metrics), 2),
            "best_mape": round(min(m['mape'] for m in all_metrics), 2),
            "worst_mape": round(max(m['mape'] for m in all_metrics), 2)
        }


# Instance globale
metrics_collector = MetricsCollector()