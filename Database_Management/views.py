from django.shortcuts import render, redirect
from Entities import ConsistsOf, Contract, Customer, Employee, Entails, GasStation, Involves, IsAssignedTo, Offers, Product, Provides, Pump, Purchase, Service, Signs, Supplier, Supply, Tank

def index(request):
    return render(request, 'index.html')

def consistOf(request):
    if request.method=="POST":
        supply_id = request.POST.get('supply-id', False)
        prod_id = request.POST.get('prod-id', False)
        cost = request.POST.get('cost', False)
        quantity = request.POST.get('quantity', False)
        previous_prod_id = request.POST.get('previous-prod-id', False)

        if "add_consists_of" in request.POST:
            try:
                ConsistsOf.insertInto(int(supply_id), int(prod_id), float(cost), float(quantity))
                return redirect(consistOf)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_consists_of" in request.POST:
            try:
                consistsOf = ConsistsOf.searchBy(int(supply_id), int(prod_id), float(cost), float(quantity))
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                ConsistsOf.update(int(supply_id), int(prod_id), float(cost), float(quantity), int(previous_prod_id))
                return redirect(consistOf)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        consistsOf = ConsistsOf.retrieveAllColumns()
    return render(request, 'consistsOf.html', {'consistsOf': consistsOf})

def consistsOf_delete(request, supply_prod):
    ConsistsOf.delete(supply_prod)
    return redirect(consistOf)

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

def entail(request):
    if request.method=="POST":
        serv_id = request.POST.get('serv-id', False)
        pur_id = request.POST.get('pur-id', False)
        previous_serv_id = request.POST.get('previous-serv-id', False)

        if "add_entails" in request.POST:
            try:
                Entails.insertInto(int(serv_id), int(pur_id))
                return redirect(entail)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_entails" in request.POST:
            try:
                entails = Entails.searchBy(int(serv_id), int(pur_id))
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Entails.update(int(serv_id), int(pur_id), int(previous_serv_id))
                return redirect(entail)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        entails = Entails.retrieveAllColumns()
    return render(request, 'entails.html', {'entails': entails})

def entails_delete(request, serv_pur):
    Entails.delete(serv_pur)
    return redirect(entail)

def gasStation(request):
    if request.method=="POST":
        longitude = request.POST.get('longitude', False)
        latitude = request.POST.get('latitude', False)
        type_of_service = request.POST.get('type-of-service', False)
        start_date = request.POST.get('start-date', False)
        minimarket = request.POST.get('minimarket', False)
        mgr_ssn = request.POST.get('mgr-ssn', False)

        if "add_gas_station" in request.POST:
            try:
                GasStation.insertInto(longitude, latitude, type_of_service, start_date,
                                      minimarket, mgr_ssn)
                return redirect(gasStation)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_gas_station" in request.POST:
            try:
                gasStations = GasStation.searchBy(longitude, latitude, type_of_service,
                                      minimarket, mgr_ssn)
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                GasStation.update(longitude, latitude, type_of_service, start_date,
                                minimarket, mgr_ssn)
                return redirect(gasStation)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        gasStations = GasStation.retrieveAllColumns()
    return render(request, 'gasStation.html', {'gasStations': gasStations})

def gasStation_delete(request, longitude_latitude):
    GasStation.delete(longitude_latitude)
    return redirect(gasStation)

def involve(request):
    if request.method=="POST":
        prod_id = request.POST.get('prod-id', False)
        pur_id = request.POST.get('pur-id', False)
        quantity = request.POST.get('quantity', False)
        previous_prod_id = request.POST.get('previous-prod-id', False)

        if "add_involves" in request.POST:
            try:
                Involves.insertInto(int(prod_id), int(pur_id), float(quantity))
                return redirect(involve)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_involves" in request.POST:
            try:
                involves = Involves.searchBy(int(prod_id), int(pur_id), float(quantity))
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Involves.update(int(prod_id), int(pur_id), float(quantity), int(previous_prod_id))
                return redirect(involve)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        involves = Involves.retrieveAllColumns()
    return render(request, 'involves.html', {'involves': involves})

def involves_delete(request, prod_pur):
    Involves.delete(prod_pur)
    return redirect(involve)

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

def provide(request):
    if request.method=="POST":
        serv_id = request.POST.get('serv-id', False)
        gs_longitude = request.POST.get('gs-longitude', False)
        gs_latitude = request.POST.get('gs-latitude', False)
        previous_serv_id = request.POST.get('previous-serv-id', False)

        if "add_provides" in request.POST:
            try:
                Provides.insertInto(int(serv_id), gs_longitude, gs_latitude)
                return redirect(provide)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_provides" in request.POST:
            try:
                provides = Provides.searchBy(int(serv_id), gs_longitude, gs_latitude)
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Provides.update(int(serv_id), gs_longitude, gs_latitude, int(previous_serv_id))
                return redirect(provide)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        provides = Provides.retrieveAllColumns()
    return render(request, 'provides.html', {'provides': provides})

def provides_delete(request, serv_gslong_lat):
    Provides.delete(serv_gslong_lat)
    return redirect(provide)

def pump(request):
    pumps = Pump.retrieveAllColumns()
    return render(request, 'pump.html', {'pumps': pumps})

def purchase(request):
    purchases = Purchase.retrieveAllColumns()
    return render(request, 'purchase.html', {'purchases': purchases})

def service(request):
    if request.method=="POST":
        id = request.POST.get('id', False)
        name = request.POST.get('name', False)
        price = request.POST.get('price', False)
        corresponding_points = request.POST.get('corresponding-points', False)

        if "add_service" in request.POST:
            try:
                Service.insertInto(id, name, price, int(corresponding_points))
                return redirect(service)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_service" in request.POST:
            try:
                services = Service.searchBy(int(id), float(price), int(corresponding_points))
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Service.update(int(id), name, float(price), int(corresponding_points))
                return redirect(service)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        services = Service.retrieveAllColumns()
    return render(request, 'service.html', {'services': services})

def service_delete(request, id):
    Service.delete(id)
    return redirect(service)

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
    if request.method=="POST":
        id = request.POST.get('id', False)
        expected_arrival_date = request.POST.get('expected-arrival-date', False)
        real_arrival_date = request.POST.get('real-arrival-date', False)
        sup_email = request.POST.get('sup-email', False)
        gs_longitude = request.POST.get('gs-longitude', False)
        gs_latitude = request.POST.get('gs-latitude', False)

        if "add_supply" in request.POST:
            try:
                Supply.insertInto(int(id), expected_arrival_date, real_arrival_date, sup_email, gs_longitude, gs_latitude)
                return redirect(supply)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_supply" in request.POST:
            try:
                supplies = Supply.searchBy(int(id), expected_arrival_date, real_arrival_date, sup_email, gs_longitude, gs_latitude)
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Supply.update(int(id), expected_arrival_date, real_arrival_date, sup_email, gs_longitude, gs_latitude)
                return redirect(supply)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        supplies = Supply.retrieveAllColumns()
    return render(request, 'supply.html', {'supplies': supplies})

def supply_delete(request, id):
    Supply.delete(id)
    return redirect(supply)

def tank(request):
    if request.method=="POST":
        tank_id = request.POST.get('id', False)
        last_check_up = request.POST.get('last-check-up', False)
        capacity = request.POST.get('capacity', False)
        quantity = request.POST.get('quantity', False)
        prod_id = request.POST.get('prod-id', False)
        gs_longitude = request.POST.get('gs-longitude', False)
        gs_latitude = request.POST.get('gs-latitude', False)

        if "add_tank" in request.POST:
            try:
                Tank.insertInto(int(tank_id), last_check_up, float(capacity), float(quantity), int(prod_id), float(gs_longitude), float(gs_latitude))
                return redirect(tank)
            except Exception as e:
                print("View exception")
                print(e)
        elif "search_tank" in request.POST:
            try:
                tanks = Tank.searchBy(int(tank_id), last_check_up, float(capacity), float(quantity), int(prod_id), float(gs_longitude), float(gs_latitude))
            except Exception as e:
                print("View exception")
                print(e)
        else:
            try:
                Tank.update(int(tank_id), last_check_up, float(capacity), float(quantity), int(prod_id), float(gs_longitude), float(gs_latitude))
                return redirect(tank)
            except Exception as e:
                print("View exception")
                print(e)
    else:
        tanks = Tank.retrieveAllColumns()
    return render(request, 'tank.html', {'tanks': tanks})

def tank_delete(request, id_longitude_latitude):
    Tank.delete(id_longitude_latitude)
    return redirect(tank)

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
    