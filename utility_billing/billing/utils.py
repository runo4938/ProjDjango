import xml.etree.ElementTree as ET
from django.core.cache import cache

def get_tariffs():
    """Получает тарифы с кэшированием"""
    if cached := cache.get('utility_tariffs'):
        return cached
        
    try:
        tree = ET.parse('tariffs.xml')
        root = tree.getroot()
        tariffs = {
            'electricity': float(root.find('electricity').text),
            'gas': float(root.find('gas').text),
            'water': float(root.find('water').text)
        }
        cache.set('utility_tariffs', tariffs, 3600)  # Кэш на 1 час
        return tariffs
    except Exception:
        return {'electricity': 5.20, 'gas': 7.50, 'water': 2.30}