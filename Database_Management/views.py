from django.shortcuts import render, redirect
from Entities import ConsistsOf, Contract, Customer, Employee, Entails, GasStation, Involves, IsAssignedTo, Offers, Product, Provides, Pump, Purchase, Service, Signs, Supplier, Supply, Tank

def index(request):
    return render(request, 'index.html')

def consistsOf(request):
    consistsOf = ConsistsOf.retrieveAllColumns()
    return render(request, 'consistsOf.html', {'consistsOf': consistsOf})

def contract(request):
    contracts = Contract.retrieveAllColumns()
    return render(request, 'contract.html', {'contracts': contracts})

def customer(request):
    customers = Customer.retrieveAllColumns()
    return render(request, 'customer.html', {'customers': customers})

def employee(request):
    if request.method=="POST":
        ssn = request.POST.get('ssn', False)
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        birth_date = request.POST['birth-date']
        phone_number = request.POST['phone-number']
        email = request.POST['email']
        longitude = request.POST['longitude']
        latitude = request.POST['latitude']
        role = request.POST['role']
        hours = request.POST['hours']
        super_ssn = request.POST['super-ssn']
        gs_longitude = request.POST['gs-longitude']
        gs_latitude = request.POST['gs-latitude']

        if "add_employee" in request.POST:
            try:
                Employee.insertInto(ssn, first_name, last_name, birth_date, phone_number,
                    email, longitude, latitude, role, hours, super_ssn,
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

def employee_delete(request, ssn):
    Employee.delete(ssn)
    return redirect(employee)

def entails(request):
    entails = Entails.retrieveAllColumns()
    return render(request, 'entails.html', {'entails': entails})

def gasStation(request):
    gasStations = GasStation.retrieveAllColumns()
    return render(request, 'gasStation.html', {'gasStations': gasStations})

def involves(request):
    involves = Involves.retrieveAllColumns()
    return render(request, 'involves.html', {'involves': involves})

def isAssignedTo(request):
    assignments = IsAssignedTo.retrieveAllColumns()
    return render(request, 'isAssignedTo.html', {'assignments': assignments})

def offers(request):
    offers = Offers.retrieveAllColumns()
    return render(request, 'offers.html', {'offers': offers})

def product(request):
    products = Product.retrieveAllColumns()
    return render(request, 'product.html', {'products': products})

def provides(request):
    provides = Provides.retrieveAllColumns()
    return render(request, 'provides.html', {'provides': provides})

def pump(request):
    pumps = Pump.retrieveAllColumns()
    return render(request, 'pump.html', {'pumps': pumps})

def purchase(request):
    purchases = Purchase.retrieveAllColumns()
    return render(request, 'purchase.html', {'purchases': purchases})

def service(request):
    services = Service.retrieveAllColumns()
    return render(request, 'service.html', {'services': services})

def signs(request):
    signs = Signs.retrieveAllColumns()
    return render(request, 'signs.html', {'signs': signs})

def supplier(request):
    names = Supplier.searchByName()
    return render(request, 'supplier.html', {'names': names})

def supply(request):
    supplies = Supply.retrieveAllColumns()
    return render(request, 'supply.html', {'supplies': supplies})

def tank(request):
    tanks = Tank.retrieveAllColumns()
    return render(request, 'tank.html', {'tanks': tanks})

if __name__ == 'Database_Management.views':
    ConsistsOf.createConsistsOfTable()
    Contract.createContractTable()
    Customer.createCustomerTable()
    Employee.createEmployeeTable()
    Entails.createEntailsTable()
    GasStation.createGasStationTable()
    Involves.createInvolvesTable()
    IsAssignedTo.createIsAssignedToTable()
    Offers.createOffersTable()
    Product.createProductTable()
    Provides.createProvidesTable()
    Pump.createPumpTable()
    Purchase.createPurchaseTable()
    Service.createServiceTable()
    Signs.createSignsTable()
    Supplier.createSupplierTable()
    Supply.createSupplyTable()
    Tank.createTankTable()
    