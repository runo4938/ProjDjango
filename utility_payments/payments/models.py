from django.db import models
from django.urls import reverse

class Payer(models.Model):
    name = models.CharField("Имя плательщика", max_length=100)

    def __str__(self):
        return self.name

class Payment(models.Model):
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE, verbose_name="Плательщик")
    electricity_curr = models.PositiveIntegerField("Электричество текущее")
    electricity_diff = models.PositiveIntegerField("Электричество разница")
    electricity_cost = models.FloatField("Электричество сумма")
    gas_curr = models.PositiveIntegerField("Газ текущее")
    gas_diff = models.PositiveIntegerField("Газ разница")
    gas_cost = models.FloatField("Газ сумма")
    water_curr = models.PositiveIntegerField("Вода текущее")
    water_diff = models.PositiveIntegerField("Вода разница")
    water_cost = models.FloatField("Вода сумма")
    internet_cost = models.DecimalField("Интернет", max_digits=10, decimal_places=2)
    trash_cost = models.DecimalField("Вывоз мусора", max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    ELECTRICITY_TARIFF = 5.2
    GAS_TARIFF = 6.1
    WATER_TARIFF = 4.8

    def get_delete_url(self):
        print("models print")
        return reverse('delete_record', kwargs={'pk': self.pk})

    @property
    def previous_payment(self):
        return Payment.objects.filter(payer=self.payer, id__lt=self.id).order_by('-id').first()

    def save(self, *args, **kwargs):
        # Получаем предыдущий платеж
        prev_payment = Payment.objects.filter(payer=self.payer).exclude(id=self.id).order_by('-date').first()     
        # Рассчитываем разницы
        self.electricity_diff = max(self.electricity_curr - (prev_payment.electricity_curr if prev_payment else 0), 0)
        self.gas_diff = max(self.gas_curr - (prev_payment.gas_curr if prev_payment else 0), 0)
        self.water_diff = max(self.water_curr - (prev_payment.water_curr if prev_payment else 0), 0)
        
        # Получаем текущие тарифы
        tariff = Tariff.get_solo()
        
        # Рассчитываем стоимости
        self.electricity_cost = round(self.electricity_diff * tariff.electricity, 2)
        self.gas_cost = round(self.gas_diff * tariff.gas, 2)
        self.water_cost = round(self.water_diff * tariff.water, 2)       
        super().save(*args, **kwargs)


    @property
    def total_cost(self):
        return (
            float(self.electricity_cost) +
            float(self.gas_cost) +
            float(self.water_cost) +
            float(self.internet_cost) +
            float(self.trash_cost)
        )
    
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
    
    