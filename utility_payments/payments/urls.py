from django.urls import path

from .views import delete_record
from . import views

urlpatterns = [
    path('', views.payment_view, name='payment_form'),
    path('edit-tariffs/', views.edit_tariffs, name='edit_tariffs'),
    path('delete/<int:pk>/', delete_record, name='delete_record'),
    path('filter-records/', views.filter_records, name='filter_records'),
    path('delete-record-ajax/', views.delete_record_ajax, name='delete_record_ajax'),
]