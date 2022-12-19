from django.urls import path

from . import views

urlpatterns = [
    path('supplier/', views.supplier, name='supplier'),
    path('employee/', views.employee, name='employee'),
    path('contract/', views.contract, name='contract'),
    path('signs/', views.signs, name='signs'),
]