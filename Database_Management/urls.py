from django.urls import path

from . import views

urlpatterns = [
    path('supplier/', views.supplier, name='supplier'),
    path('employee/', views.employee, name='employee'),
    path('contract/', views.contract, name='contract'),
    path('signs/', views.signs, name='signs'),
    path('services/', views.service, name='service'),
    path('is_assigned_to/', views.isAssignedTo, name='isAssignedTo'),
    path('products/', views.product, name='product'),
    path('tanks/', views.tank, name='tank'),
]