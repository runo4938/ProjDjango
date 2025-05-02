from django.core.cache import cache
from django.db import models
from django.urls import reverse

from django.conf import settings
# Create your models here. 

class UtilityRecord(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    
    # Электричество
    electricity_reading = models.FloatField(verbose_name="ЭлектроПоказания")
    electricity_diff = models.FloatField(verbose_name="Разница (Электричество)", blank=True, null=True)
    electricity_sum = models.FloatField(verbose_name="Сумма (Электричество)", blank=True, null=True)
    
    # Газ
    gas_reading = models.FloatField(verbose_name="ГазПоказания")
    gas_diff = models.FloatField(verbose_name="Разница (Газ)", blank=True, null=True)
    gas_sum = models.FloatField(verbose_name="Сумма (Газ)", blank=True, null=True)
    
    # Вода
    water_reading = models.FloatField(verbose_name="ВодаПоказания")
    water_diff = models.FloatField(verbose_name="Разница (Вода)", blank=True, null=True)
    water_sum = models.FloatField(verbose_name="Сумма (Вода)", blank=True, null=True)

    def __str__(self):
        return f"Запись от {self.date}"

    class Meta:
        verbose_name = "Запись коммунальных услуг"
        verbose_name_plural = "Записи коммунальных услуг"

    def get_delete_url(self):
        return reverse('delete_record', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
    # Округляем все суммы
        if self.electricity_sum is not None:
            self.electricity_sum = round(self.electricity_sum, 2)
    
        if self.gas_sum is not None:
            self.gas_sum = round(self.gas_sum, 2)
        
        if self.water_sum is not None:
            self.water_sum = round(self.water_sum, 2)
        
        super().save(*args, **kwargs)



class Tariff(models.Model):
    ELECTRICITY = 'ELEC'
    GAS = 'GAS'
    WATER = 'WATER'
    
    UTILITY_TYPES = [
        (ELECTRICITY, 'Электричество'),
        (GAS, 'Газ'),
        (WATER, 'Вода'),
    ]
    
    utility_type = models.CharField(max_length=5, choices=UTILITY_TYPES, unique=True)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    effective_from = models.DateField(auto_now_add=True)
    
    @classmethod
    def get_current_rates(cls):
        """Получает тарифы с кэшированием"""
        cache_key = 'current_utility_rates'
        rates = cache.get(cache_key)
        
        if not rates:
            rates = {
                cls.ELECTRICITY: cls.objects.get(utility_type=cls.ELECTRICITY).rate,
                cls.GAS: cls.objects.get(utility_type=cls.GAS).rate,
                cls.WATER: cls.objects.get(utility_type=cls.WATER).rate,
            }
            cache.set(cache_key, rates, 3600)  # Кэш на 1 час
        
        return rates