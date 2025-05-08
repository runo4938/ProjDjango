from django.contrib import admin
from .models import Payer, Payment

@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payer',
        'electricity_curr',
        'gas_curr',
        'water_curr',
        'internet_cost',
        'trash_cost',
        'date',
        'electricity_diff',
        'gas_diff',
        'water_diff',
        'total_cost'
    )
    list_filter = ('payer', 'date')
    readonly_fields = (
        'electricity_diff',
        'gas_diff',
        'water_diff',
        'electricity_cost',
        'gas_cost',
        'water_cost',
        'total_cost'
    )

    fieldsets = (
        (None, {
            'fields': ('payer',)
        }),
        ('Показания', {
            'fields': ('electricity_curr', 'gas_curr', 'water_curr')
        }),
        ('Фиксированные платежи', {
            'fields': ('internet_cost', 'trash_cost')
        }),
        ('Рассчитанные значения', {
            'fields': (
                'electricity_diff',
                'gas_diff',
                'water_diff',
                'electricity_cost',
                'gas_cost',
                'water_cost',
                'total_cost'
            )
        }),
        ('Дополнительно', {
            'fields': ('date',)
        }),
    )

    def has_add_permission(self, request):
        # Запрещаем добавление через админку — только через пользовательскую форму
        return False

    def electricity_diff(self, obj):
        return obj.electricity_diff
    electricity_diff.short_description = "Электричество (разница)"

    def gas_diff(self, obj):
        return obj.gas_diff
    gas_diff.short_description = "Газ (разница)"

    def water_diff(self, obj):
        return obj.water_diff
    water_diff.short_description = "Вода (разница)"

    def electricity_cost(self, obj):
        return f"{obj.electricity_cost:.2f}"
    electricity_cost.short_description = "Стоимость электричества"

    def gas_cost(self, obj):
        return f"{obj.gas_cost:.2f}"
    gas_cost.short_description = "Стоимость газа"

    def water_cost(self, obj):
        return f"{obj.water_cost:.2f}"
    water_cost.short_description = "Стоимость воды"

    def total_cost(self, obj):
        return f"{obj.total_cost:.2f}"
    total_cost.short_description = "Итоговая сумма"