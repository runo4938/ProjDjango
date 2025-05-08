from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_view, name='payment_form'),
    path('edit-tariffs/', views.edit_tariffs, name='edit_tariffs'),
]