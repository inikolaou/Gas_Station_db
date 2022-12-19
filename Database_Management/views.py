from django.shortcuts import render
from Entities import Supplier, Employee, Contract

def supplier(request):
    names = Supplier.searchByName()
    return render(request, 'supplier.html', {'names': names})

def employee(request):
    names = Employee.searchByName()
    return render(request, 'employee.html', {'names': names})

def contract(request):
    contracts = Contract.retrieveAllColumns()
    return render(request, 'contract.html', {'contracts': contracts})

if __name__ == 'Database_Management.views':
    Supplier.createSupplierTable()
    Supplier.insertFromCsv("Datasets/supplier.csv")
    Employee.createEmployeeTable()
    Employee.insertFromCsv("Datasets/employee.csv")
    Contract.createContractTable()
    Contract.insertFromCsv("Datasets/contract.csv")