from django.shortcuts import render
from Entities import Supplier

print(__name__)
Supplier.createSupplierTable()
Supplier.insertFromCsv("Datasets/supplier.csv")

def supplier(request):
    data = Supplier.searchByName()
    return render(request, 'supplier.html', {'name': data})