from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse
from .models import Payment, Payer, Tariff

def payment_view(request):
    payers = Payer.objects.all()
    
    tariffs = Tariff.objects.first()
    if not tariffs:
        tariffs = Tariff.objects.create() 
    # Получаем текущего плательщика из POST или GET
    selected_payer_id = request.POST.get('payer') or request.GET.get('payer')
    
    # Пробуем преобразовать в int, если нет — оставляем None
    if selected_payer_id:
        try:
            selected_payer_id = int(selected_payer_id)
        except (TypeError, ValueError):
            selected_payer_id = None
    
    # Фильтруем платежи по выбранному плательщику
    payments = Payment.objects.all().order_by('-date')
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

    context = {
        'payers': payers,
        'selected_payer_id': selected_payer_id,  # важно: передаем в шаблон
        'payments': payments,
        'tariffs': tariffs,
    }
    return render(request, 'payments/payment_form.html', context)

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
