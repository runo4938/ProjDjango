from django import forms
from .models import UtilityRecord
import xml.etree.ElementTree as ET
from .utils import get_tariffs
from django.conf import settings
import os


class UtilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Инициализируем tariffs при создании формы
        self.tariffs = self._load_tariffs()

    def _load_tariffs(self):
        """Загружает тарифы из XML файла"""
        try:
            tree = ET.parse('tariffs.xml')
            root = tree.getroot()
            return {
                'electricity': float(root.find('electricity').text),
                'gas': float(root.find('gas').text),
                'water': float(root.find('water').text),
                'internet': float(root.find('internet').text),
                'musor': float(root.find('musor').text)
            }
        except (FileNotFoundError, AttributeError, ValueError) as e:
            # Значения по умолчанию при ошибке
            return {
                'electricity': 5.20,
                'gas': 7.50,
                'water': 2.30
            }
    class Meta: 
        model = UtilityRecord
        fields = ['electricity_reading', 'gas_reading', 'water_reading']
        labels = {
            'electricity_reading': 'Текущие показания',
            'gas_reading': 'Текущие показания',
            'water_reading': 'Текущие показания',
        }
        widgets = {
            'electricity_reading': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текущие показания',
                'step': '0.01'
            }),
            'gas_reading': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текущие показания',
                'step': '0.01'
            }),
            'water_reading': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текущие показания',
                'step': '0.01'
            }),
        }

    # ... остальной код формы без изменений ...

        fields = [
            'electricity_reading', 
            'gas_reading', 
            'water_reading'
        ]
        labels = {
            'electricity_reading': 'Текущие показания электричества',
            'gas_reading': 'Текущие показания газа',
            'water_reading': 'Текущие показания воды',
        }

    def calculate(self):
        # Парсинг тарифов из XML
        tariffs = get_tariffs()
        tree = ET.parse('tariffs.xml')
        root = tree.getroot()
        
        tariffs = {
            'electricity': float(root.find('electricity').text),
            'gas': float(root.find('gas').text),
            'water': float(root.find('water').text),
            'internet': float(root.find('internet').text),
            'musor': float(root.find('musor').text)            
        }
        
        # Получение последней записи для расчета разницы
        last_record = UtilityRecord.objects.last()
        
        data = self.cleaned_data
        
        # Расчет разницы и суммы
        if last_record:
            data['electricity_diff'] = data['electricity_reading'] - last_record.electricity_reading
            data['electricity_sum'] = data['electricity_diff'] * tariffs['electricity']
            
            data['gas_diff'] = data['gas_reading'] - last_record.gas_reading
            data['gas_sum'] = data['gas_diff'] * tariffs['gas']
            
            data['water_diff'] = data['water_reading'] - last_record.water_reading
            data['water_sum'] = data['water_diff'] * tariffs['water']
        
        return data
    

class TariffEditForm(forms.Form):
    electricity = forms.FloatField(
        label="Электричество (₽/кВт·ч)",
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '0.01'}))
    
    gas = forms.FloatField(
        label="Газ (₽/м³)",
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '0.01'}))
    
    water = forms.FloatField(
        label="Вода (₽/м³)",
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '0.01'}))
    
    internet = forms.FloatField(
        label="Интернет (₽)",
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '1.0'}))
    
    musor = forms.FloatField(
        label="Мусор (₽)",
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '0.01'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Загружаем текущие значения при инициализации формы
        self.fields['electricity'].initial = self._get_current_rate('electricity')
        self.fields['gas'].initial = self._get_current_rate('gas')
        self.fields['water'].initial = self._get_current_rate('water')
        self.fields['internet'].initial = self._get_current_rate('internet')
        self.fields['musor'].initial = self._get_current_rate('musor')

    def _get_current_rate(self, utility_type):
        """Получает текущий тариф из XML"""
        tree = ET.parse(os.path.join(settings.BASE_DIR, 'tariffs.xml'))
        return float(tree.find(utility_type).text)

    def save(self):
        """Сохраняет новые тарифы в XML"""
        tree = ET.parse(os.path.join(settings.BASE_DIR, 'tariffs.xml'))
        root = tree.getroot()
        
        root.find('electricity').text = str(self.cleaned_data['electricity'])
        root.find('gas').text = str(self.cleaned_data['gas'])
        root.find('water').text = str(self.cleaned_data['water'])
        root.find('internet').text = str(self.cleaned_data['internet'])
        root.find('musor').text = str(self.cleaned_data['musor'])
        
        tree.write(
            os.path.join(settings.BASE_DIR, 'tariffs.xml'),
            encoding='utf-8',
            xml_declaration=True
        )