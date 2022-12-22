from django.shortcuts import render
from Entities import Supplier, Employee, Contract, Signs, Service, IsAssignedTo, Product, Tank, Pump, Customer

def index(request):
    return render(request, 'index.html')

def supplier(request):
    names = Supplier.searchByName()
    return render(request, 'supplier.html', {'names': names})

def employee(request):
    if request.method=="POST":
        ssn = request.POST.get('ssn', False)
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        birth_date = request.POST['birth-date']
        phone_number = request.POST['phone-number']
        longitude = request.POST['longitude']
        latitude = request.POST['latitude']
        role = request.POST['role']
        hours = request.POST['hours']
        super_ssn = request.POST['super-ssn']
        gs_longitude = request.POST['gs-longitude']
        gs_latitude = request.POST['gs-latitude']

        if "add_employee" in request.POST:
            try:
                Employee.insertInto(ssn, first_name, last_name, email, birth_date,
                    phone_number, longitude, latitude, role, hours, super_ssn,
                    gs_longitude, gs_latitude)
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Employee.update(ssn, first_name, last_name, email, birth_date,
                phone_number, longitude, latitude, role, hours, super_ssn,
                gs_longitude, gs_latitude)
            except Exception as e:
                print("View exception")
                print(e)
    employees = Employee.retrieveAllColumns()
    return render(request, 'employee.html', {'employees': employees})

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

def pump(request):
    pumps = Pump.retrieveAllColumns()
    return render(request, 'pump.html', {'pumps': pumps})

def customer(request):
    customers = Customer.retrieveAllColumns()
    return render(request, 'customer.html', {'customers': customers})

if __name__ == 'Database_Management.views':
    Supplier.createSupplierTable()
    Employee.createEmployeeTable()
    Contract.createContractTable()
    Signs.createSignsTable()
    Service.createServiceTable()
    IsAssignedTo.createIsAssignedToTable()
    Product.createProductTable()
    Tank.createTankTable()
    Pump.createPumpTable()
    Customer.createCustomerTable()
    