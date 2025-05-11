from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_view, name='payment_form'),
    path('edit-tariffs/', views.edit_tariffs, name='edit_tariffs'),
    path('filter-records/', views.filter_records, name='filter_records'),
    path('delete-record-ajax/', views.delete_record_ajax, name='delete_record_ajax'),
]