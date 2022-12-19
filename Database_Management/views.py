from django.shortcuts import render
from Entities import Supplier, Employee, Contract, Signs, Service, IsAssignedTo, Product, Tank

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

def isAssignedTo(request):
    assignments = IsAssignedTo.retrieveAllColumns()
    return render(request, 'isAssignedTo.html', {'assignments': assignments})

def product(request):
    products = Product.retrieveAllColumns()
    return render(request, 'product.html', {'products': products})

def tank(request):
    tanks = Tank.retrieveAllColumns()
    return render(request, 'tank.html', {'tanks': tanks})

if __name__ == 'Database_Management.views':
    Supplier.createSupplierTable()
    Employee.createEmployeeTable()
    Contract.createContractTable()
    Signs.createSignsTable()
    Service.createServiceTable()
    IsAssignedTo.createIsAssignedToTable()
    Product.createProductTable()
    Tank.createTankTable()
    