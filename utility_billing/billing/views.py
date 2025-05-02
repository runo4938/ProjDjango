# Create your views here.
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import UtilityForm
from .models import UtilityRecord
from django.utils.timezone import now
from .forms import TariffEditForm

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def utility_form(request):
    if request.method == 'POST':
        form = UtilityForm(request.POST)
        if form.is_valid():
            calculated_data = form.calculate()
            UtilityRecord.objects.create(**calculated_data)
            return redirect('utility_form')
    else:
        form = UtilityForm()
    
    records = UtilityRecord.objects.all().order_by('date')
    # Передаем текущую дату в шаблон
    current_date = now().date()  # Текущая дата без времени
    tariffs = form.tariffs
    return render(request, 'billing/form.html', {
        'form': form,
        'records': records,
        'current_date': current_date,  # Передаем текущую дату
        'tariffs':tariffs,
    })

def edit_tariffs(request):
    if request.method == 'POST':
        form = TariffEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('utility_form')
    else:
        form = TariffEditForm()
    
    return render(request, 'billing/edit_tariffs.html', {'form': form})


@require_POST
def delete_record(request, pk):
    record = get_object_or_404(UtilityRecord, pk=pk)
    record.delete()
    return redirect('utility_form')  # Возврат на страницу с формой

def my_view(request):
    # Добавляем уведомление
    messages.success(request, "Это успешное уведомление!")
    messages.error(request, "Произошла ошибка!")
    
    return render(request, 'your_template.html')

