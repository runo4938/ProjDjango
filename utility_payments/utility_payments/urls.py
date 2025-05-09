from django.contrib import admin
from django.urls import path, include
from payments.views import delete_record

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('payments.urls')),
    path('delete/<int:pk>/', delete_record, name='delete_record'),
]