from django.urls import path

from .views import delete_record
from . import views

urlpatterns = [
    path('', views.payment_view, name='payment_form'),
    path('edit-tariffs/', views.edit_tariffs, name='edit_tariffs'),
    path('delete/<int:pk>/', delete_record, name='delete_record'),
]