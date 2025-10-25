"""
Package page_modules pour Stokkel Dashboard
"""

from . import home
from . import data_management
from . import forecasting
from . import recommendations
from . import executive_dashboard
from . import setting

__all__ = [
    'home',
    'data_management',
    'forecasting',
    'recommendations',
    'executive_dashboard',
    'setting'
]