from django.shortcuts import render
from Entities import Supplier, Employee, Contract, Signs, Service

def supplier(request):
    names = Supplier.searchByName()
    return render(request, 'supplier.html', {'names': names})

def employee(request):
    names = Employee.searchByName()
    return render(request, 'employee.html', {'names': names})

def contract(request):
    contracts = Contract.retrieveAllColumns()
    return render(request, 'contract.html', {'contracts': contracts})

def signs(request):
    signs = Signs.retrieveAllColumns()
    return render(request, 'signs.html', {'signs': signs})

def service(request):
    services = Service.retrieveAllColumns()
    return render(request, 'service.html', {'services': services})

if __name__ == 'Database_Management.views':
    Supplier.createSupplierTable()
    Employee.createEmployeeTable()
    Contract.createContractTable()
    Signs.createSignsTable()
    Service.createServiceTable()
    