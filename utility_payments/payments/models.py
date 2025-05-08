from django.db import models

class Payer(models.Model):
    name = models.CharField("Имя плательщика", max_length=100)

    def __str__(self):
        return self.name


class Payment(models.Model):
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE, verbose_name="Плательщик")
    electricity_curr = models.PositiveIntegerField("Электричество текущее")
    gas_curr = models.PositiveIntegerField("Газ текущее")
    water_curr = models.PositiveIntegerField("Вода текущее")
    internet_cost = models.DecimalField("Интернет", max_digits=10, decimal_places=2)
    trash_cost = models.DecimalField("Вывоз мусора", max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    ELECTRICITY_TARIFF = 5.2
    GAS_TARIFF = 6.1
    WATER_TARIFF = 4.8

    @property
    def previous_payment(self):
        return Payment.objects.filter(payer=self.payer, id__lt=self.id).order_by('-id').first()

    @property
    def electricity_diff(self):
        prev = self.previous_payment
        if prev:
            return self.electricity_curr - prev.electricity_curr
        return self.electricity_curr  # Если нет предыдущих данных

    @property
    def gas_diff(self):
        prev = self.previous_payment
        if prev:
            return self.gas_curr - prev.gas_curr
        return self.gas_curr

    @property
    def water_diff(self):
        prev = self.previous_payment
        if prev:
            return self.water_curr - prev.water_curr
        return self.water_curr

    @property
    def total_cost(self):
        return (
            float(self.electricity_cost) +
            float(self.gas_cost) +
            float(self.water_cost) +
            float(self.internet_cost) +
            float(self.trash_cost)
        )
    
    @property
    def electricity_cost(self):
        tariff = Tariff.get_solo().electricity
        return round(self.electricity_diff * tariff, 2)

    @property
    def gas_cost(self):
        tariff = Tariff.get_solo().gas
        return round(self.gas_diff * tariff, 2)

    @property
    def water_cost(self):
        tariff = Tariff.get_solo().water
        return round(self.water_diff * tariff, 2)

    def __str__(self):
        return f"{self.payer} - {self.date}"
    

class Tariff(models.Model):
    electricity = models.DecimalField("Тариф за электричество", max_digits=10, decimal_places=2, default=5.2)
    gas = models.DecimalField("Тариф за газ", max_digits=10, decimal_places=2, default=6.1)
    water = models.DecimalField("Тариф за воду", max_digits=10, decimal_places=2, default=4.8)

    def __str__(self):
        return "Текущие тарифы",self.water,self.electricity

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    