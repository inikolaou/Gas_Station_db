from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('supplier/', views.supplier, name='supplier'),
    path('employee/', views.employee, name='employee'),
    path('employee/<str:ssn>/', views.employee_delete),
    path('contract/', views.contract, name='contract'),
    path('signs/', views.signs, name='signs'),
    path('services/', views.service, name='service'),
    path('is_assigned_to/', views.isAssignedTo, name='isAssignedTo'),
    path('products/', views.product, name='product'),
    path('tanks/', views.tank, name='tank'),
    path('pumps/', views.pump, name='pump'),
    path('customers/', views.customer, name='customer'),
    path('gas_stations/', views.gasStation, name='gasStation')
]