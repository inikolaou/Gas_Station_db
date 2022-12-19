from django.urls import path

from . import views

urlpatterns = [
    path('supplier/', views.supplier, name='supplier'),
    path('employee/', views.employee, name='employee')
]