from django.contrib import admin
from django.urls import path
from billing.views import utility_form
from billing.views import delete_record
from billing.views import edit_tariffs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', utility_form, name='utility_form'),
    path('delete/<int:pk>/', delete_record, name='delete_record'),
    path('edit-tariffs/', edit_tariffs, name='edit_tariffs'),
]