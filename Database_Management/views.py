from django.shortcuts import render, redirect
from Entities import ConsistsOf, Contract, Customer, Employee, Entails, GasStation, Involves, IsAssignedTo, Offers, Product, Provides, Pump, Purchase, Service, Signs, Supplier, Supply, Tank

def index(request):
    return render(request, 'index.html')

def consistsOf(request):
    consistsOf = ConsistsOf.retrieveAllColumns()
    return render(request, 'consistsOf.html', {'consistsOf': consistsOf})

def contract(request):
    if request.method=="POST":
        id = request.POST.get('id', False)
        start_date = request.POST.get('start-date', False)
        end_date = request.POST.get('end-date', False)
        salary = request.POST.get('salary', False)

        if "add_contract" in request.POST:
            try:
                Contract.insertInto(id, start_date, end_date, salary)
                return redirect(contract)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_contract" in request.POST:
            try:
                contracts = Contract.searchBy(int(id), start_date, end_date, float(salary))
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Contract.update(int(id), start_date, end_date, float(salary))
                return redirect(contract)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        contracts = Contract.retrieveAllColumns()
    return render(request, 'contract.html', {'contracts': contracts})

def contract_delete(request, id):
    Contract.delete(id)
    return redirect(contract)

def customer(request):
    if request.method=="POST":
        email = request.POST.get('email', False)
        first_name = request.POST.get('first-name', False)
        last_name = request.POST.get('last-name', False)
        birth_date = request.POST.get('birth-date', False)
        phone_number = request.POST.get('phone-number', False)
        longitude = request.POST.get('longitude', False)
        latitude = request.POST.get('latitude', False)
        remaining_points = request.POST.get('remaining-points', False)

        if "add_customer" in request.POST:
            try:
                Customer.insertInto(email, first_name, last_name, birth_date,
                phone_number, longitude, latitude, remaining_points)
                return redirect(customer)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_customer" in request.POST:
            try:
                customers = Customer.searchBy(email, phone_number, int(remaining_points))
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Customer.update(email, first_name, last_name, birth_date, phone_number,
                                longitude, latitude, remaining_points)
                return redirect(customer)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        customers = Customer.retrieveAllColumns()
    return render(request, 'customer.html', {'customers': customers})

def customer_delete(request, email):
    Customer.delete(email)
    return redirect(customer)

def employee(request):
    if request.method=="POST":
        ssn = request.POST.get('ssn', False)
        first_name = request.POST.get('first-name', False)
        last_name = request.POST.get('last-name', False)
        birth_date = request.POST.get('birth-date', False)
        phone_number = request.POST.get('phone-number', False)
        email = request.POST.get('email', False)
        longitude = request.POST.get('longitude', False)
        latitude = request.POST.get('latitude', False)
        role = request.POST.get('role', False)
        hours = request.POST.get('hours', False)
        super_ssn = request.POST.get('super-ssn', False)
        gs_longitude = request.POST.get('gs-longitude', False)
        gs_latitude = request.POST.get('gs-latitude', False)

        if "add_employee" in request.POST:
            try:
                Employee.insertInto(ssn, first_name, last_name, birth_date, phone_number,
                    email, longitude, latitude, role, hours, super_ssn,
                    gs_longitude, gs_latitude)
                return redirect(employee)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_employee" in request.POST:
            try:
                employees = Employee.searchBy(ssn, role, super_ssn, gs_longitude, gs_latitude)
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Employee.update(ssn, first_name, last_name, email, birth_date,
                phone_number, longitude, latitude, role, hours, super_ssn,
                gs_longitude, gs_latitude)
                return redirect(employee)
            except Exception as e:
                print("View exception")
                print(e)
    else:
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
    if request.method=="POST":
        id = request.POST.get('id', False)
        name = request.POST.get('name', False)
        type = request.POST.get('type', False)
        price = request.POST.get('price', False)
        corresponding_points = request.POST.get('corresponding-points', False)

        if "add_product" in request.POST:
            try:
                Product.insertInto(id, name, type, price, int(corresponding_points))
                return redirect(product)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_product" in request.POST:
            try:
                products = Product.searchBy(int(id), type, float(price), int(corresponding_points))
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Product.update(int(id), name, type, float(price), int(corresponding_points))
                return redirect(product)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        products = Product.retrieveAllColumns()
    return render(request, 'product.html', {'products': products})

def product_delete(request, id):
    Product.delete(id)
    return redirect(product)

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

def sign(request):
    if request.method=="POST":
        essn = request.POST.get('essn', False)
        contract_id = request.POST.get('contract-id', False)
        previous_contract_id = request.POST.get('previous-contract-id', False)

        if "add_sign" in request.POST:
            try:
                Signs.insertInto(essn, int(contract_id))
                return redirect(sign)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_sign" in request.POST:
            try:
                signs = Signs.searchBy(essn, int(contract_id))
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Signs.update(essn, int(contract_id), int(previous_contract_id))
                return redirect(sign)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        signs = Signs.retrieveAllColumns()
    return render(request, 'signs.html', {'signs': signs})

def sign_delete(request, essn_contract):
    Signs.delete(essn_contract)
    return redirect(sign)

def supplier(request):
    if request.method=="POST":
        email = request.POST.get('email', False)
        first_name = request.POST.get('first-name', False)
        last_name = request.POST.get('last-name', False)
        phone_number = request.POST.get('phone-number', False)
        longitude = request.POST.get('longitude', False)
        latitude = request.POST.get('latitude', False)

        if "add_supplier" in request.POST:
            try:
                Supplier.insertInto(email, first_name, last_name,
                phone_number, longitude, latitude)
                return redirect(supplier)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_supplier" in request.POST:
            try:
                suppliers = Supplier.searchBy(
                    email, phone_number, longitude, latitude)
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Supplier.update(email, first_name, last_name, phone_number,
                                longitude, latitude)
                return redirect(supplier)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        suppliers = Supplier.retrieveAllColumns()
    return render(request, 'supplier.html', {'suppliers': suppliers})

def supplier_delete(request, email):
    Supplier.delete(email)
    return redirect(supplier)

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
    