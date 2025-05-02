from django.core.cache import cache
from django.contrib import admin
from .models import Tariff

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('get_utility_type_display', 'rate', 'effective_from')
    readonly_fields = ('effective_from',)
    
    def save_model(self, request, obj, form, change):
        """При сохранении сбрасываем кэш"""
        super().save_model(request, obj, form, change)
        cache.delete('current_utility_rates')