from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consists_of/', views.consistsOf, name='consistsOf'),
    path('contract/', views.contract, name='contract'),
    path('customers/', views.customer, name='customer'),
    path('employee/', views.employee, name='employee'),
    path('employee/<str:ssn>/', views.employee_delete),
    path('entails/', views.entails, name='entails'),
    path('gas_stations/', views.gasStation, name='gasStation'),
    path('involves/', views.involves, name='involves'),
    path('is_assigned_to/', views.isAssignedTo, name='isAssignedTo'),
    path('offers/', views.offers, name='offers'),
    path('products/', views.product, name='product'),
    path('provides/', views.provides, name='provides'),
    path('pumps/', views.pump, name='pump'),
    path('purchases/', views.purchase, name='purchase'),
    path('services/', views.service, name='service'),
    path('signs/', views.signs, name='signs'),
    path('supplier/', views.supplier, name='supplier'),
    path('supplies/', views.supply, name='supply'),
    path('tanks/', views.tank, name='tank')
]