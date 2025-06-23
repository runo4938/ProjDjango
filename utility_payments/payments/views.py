from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse
from .models import Payment, Payer, Tariff
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth

def payment_view(request):
    # Получаем payer_id из сессии или запроса
    payer_id = request.POST.get('payer') or request.GET.get('payer') or request.session.get('selected_payer_id')
    
    account_numbers = {
        1: {
            'electricity': '12453822',
            'gas': '126014010974',
            'water': '141147000000186',
            'trash': '1525661',

        },
        2: {
            'electricity': '14753822',
            'gas': '1200080529',
            'water': '141147000000206',
            'trash': 'Пенсионер',
        },
    
    }
    
    if payer_id:
        try:
            payer_id = int(payer_id)  
            
            # Сохраняем в сессию
            request.session['selected_payer_id'] = payer_id
        except (TypeError, ValueError):
            payer_id = None
    else:
        # Если нет в запросе и сессии - сбрасываем
        request.session.pop('selected_payer_id', 'itsme')
    # Остальной код остается без изменений...

    payers = Payer.objects.all()
    
    tariffs = Tariff.objects.first()
    if not tariffs:
        tariffs = Tariff.objects.create() 
    # Получаем текущего плательщика из POST или GET
    selected_payer_id = request.POST.get('payer') or request.GET.get('payer') or request.session.get('selected_payer_id')
   
   
    
    # Пробуем преобразовать в int, если нет — оставляем None
    if selected_payer_id:
        try:
            selected_payer_id = int(selected_payer_id)
        except (TypeError, ValueError):
            selected_payer_id = None 
    
    # Фильтруем платежи по выбранному плательщику
    payments = Payment.objects.all().order_by('date')
    if selected_payer_id:
        payments = payments.filter(payer_id=selected_payer_id)

    if request.method == 'POST' and 'calculate' in request.POST:
        payer_id = request.POST.get('payer')
        payer = Payer.objects.get(id=payer_id)

        electricity_curr = int(request.POST.get('electricity_curr', 0))
        gas_curr = int(request.POST.get('gas_curr', 0))
        water_curr = int(request.POST.get('water_curr', 0))
        internet_cost = float(request.POST.get('internet_cost', 0))
        trash_cost = float(request.POST.get('trash_cost', 0))
    

        Payment.objects.create(
            payer=payer,
            electricity_curr=electricity_curr,
            gas_curr=gas_curr,
            water_curr=water_curr,
            internet_cost=internet_cost,
            trash_cost=trash_cost,
        )

        # Перенаправляем обратно с параметром ?payer=...
        url = reverse('payment_form') + f'?payer={payer_id}'
        return HttpResponseRedirect(url)

    
    current_date = now().date()  # Текущая дата без времени
    current_accounts = account_numbers.get(int(selected_payer_id)) if selected_payer_id else account_numbers.get(1, {})
    context = {
        'payers': payers,
        'selected_payer_id': int(selected_payer_id) if selected_payer_id else None,  # важно: передаем в шаблон
        'payments': payments,
        'tariffs': tariffs,
        'current_date':current_date,
        'current_accounts': current_accounts,  # Передаем номера счетов в шаблон
       
    }
    return render(request, 'payments/payment_form.html', context,)
                                                          

from .forms import TariffForm

def edit_tariffs(request):
    tariff = Tariff.get_solo()

    if request.method == 'POST':
        form = TariffForm(request.POST, instance=tariff)
        if form.is_valid():
            form.save()
            return redirect('payment_form')

    else:
        form = TariffForm(instance=tariff)

    return render(request, 'payments/edit_tariffs.html', {
        'form': form,
        'tariff': tariff
    })


def filter_records(request):
    payer_id = request.GET.get('payer')
    request.session['selected_payer_id'] = payer_id
    payments = Payment.objects.all().order_by('date')
    if payer_id:
        payments = payments.filter(payer_id=payer_id)
    context = {
        'payments': payments,
        'current_date': now().date(),
    }
    html = render(request, 'payments/_records_table.html', context).content.decode('utf-8')
    return JsonResponse({'table_html': html})


from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Payment

@require_POST
def delete_record_ajax(request):
    record_id = request.POST.get('record_id')
    payer_id = request.POST.get('payer')
    Payment.objects.filter(id=record_id).delete()
    # После удаления возвращаем обновлённую таблицу
    from django.utils.timezone import now
    payments = Payment.objects.all().order_by('date')
    if payer_id:
        payments = payments.filter(payer_id=payer_id)
    context = {
        'payments': payments,
        'current_date': now().date(),
    }
    html = render(request, 'payments/_records_table.html', context).content.decode('utf-8')
    return JsonResponse({'table_html': html})

from django.db.models import Sum, F, Window
from django.db.models.functions import Lag, TruncMonth

def utility_chart(request):
    # Получаем всех плательщиков и их данные
    payer_id = request.session.get('selected_payer_id')
    payers = Payer.objects.all()
    
    if payer_id:
        payers = payers.filter(id=payer_id)  # Фильтруем только выбранного плательщика
    
    # payers = Payer.objects.all()
    datasets = []

    for payer in payers:
        # Фильтруем платежи по текущему плательщику
        payments = Payment.objects.filter(payer=payer).order_by('date')

        if not payments.exists():
            continue  # Пропускаем плательщиков без данных

        # Группируем по месяцам и вычисляем разницы
        months = []
        electricity = []
        gas = []
        water = []

        prev_electricity = None
        prev_gas = None
        prev_water = None

        for payment in payments:
            month = payment.date.strftime("%Y-%m")
            months.append(month)

            # Вычисляем разницу с предыдущим показанием
            if prev_electricity is not None:
                electricity.append(payment.electricity_diff)
                gas.append(payment.gas_diff)
                water.append(payment.water_diff)
            else:
                electricity.append(0)
                gas.append(0)
                water.append(0)

            prev_electricity = payment.electricity_curr
            prev_gas = payment.gas_curr
            prev_water = payment.water_curr

        # Добавляем данные плательщика в общий набор
        datasets.append({
            'payer': payer.name,
            'months': months,
            'electricity': electricity,
            'gas': gas,
            'water': water,
        })

    context = {
        'datasets': datasets,
    }
    return render(request, 'payments/utility_chart.html', context)

def get_account_numbers(request):
    payer_id = request.GET.get('payer_id')
    
    # Словарь с номерами счетов (можно вынести в отдельный файл или БД)
    account_numbers = {
        1: {
            'electricity': '12453822 Электричество',
            'gas': '126014010974 Газ',
            'water': '141147000000186 Вода',
            'trash': '1525661 Мусор',
        },
        2: {
            'electricity': '14753822 Электричество',
            'gas': '1200080529 Газ',
            'water': '141147000000206 Вода',
            'trash': 'Пенсионер',
        },
    
    }
   
    current_accounts = account_numbers.get(int(payer_id), {}) if payer_id else {}
    print(current_accounts)
    return JsonResponse(current_accounts)