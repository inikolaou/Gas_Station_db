from email_validator import validate_email, EmailNotValidError
from datetime import datetime
from django.shortcuts import render, redirect
from Entities import ConsistsOf, Contract, Customer, Employee, Entails, GasStation, Involves, IsAssignedTo, Offers, Product, Provides, Pump, Purchase, Service, Signs, Supplier, Supply, Tank


def index(request):
    return render(request, 'index.html')


def balanceSheet(request):
    revenue = Purchase.allPurchaseinfo()
    supplies_cost = Purchase.allSuppliesinfo()
    revenue_of_products = Purchase.groupByGSCoordsAllProducts()
    revenue_of_services = Purchase.groupByGSCoordsAllServices()

    all_product_analysis = Purchase.productAnalysis()
    all_service_analysis = Purchase.serviceAnalysis()

    context = {"revenue": revenue, "revenue_of_products": revenue_of_products,
               "revenue_of_services": revenue_of_services, "supplies_cost": supplies_cost, "all_product_analysis": all_product_analysis, "all_service_analysis": all_service_analysis}
    return render(request, 'balanceSheet.html', context)


def consistOf(request):
    supply_id_fault = False
    prod_id_fault = False
    cost_fault = False
    quantity_fault = False

    if request.method == "POST":
        supply_id = request.POST.get('supply-id', False)
        prod_id = request.POST.get('prod-id', False)
        cost = request.POST.get('cost', False)
        quantity = request.POST.get('quantity', False)
        previous_prod_id = request.POST.get('previous-prod-id', False)

        error_occured = False

        if (supply_id != False):
            supply_id = supply_id.strip()
            if (not supply_id.isdigit()):
                supply_id_fault = "Please write a positive integer for Supply ID"
                error_occured = True
            else:
                supply_id = int(supply_id)

        if (prod_id != False):
            prod_id = prod_id.strip()
            if (not prod_id.isdigit()):
                prod_id_fault = "Please write a positive integer for Product ID"
                error_occured = True
            else:
                prod_id = int(prod_id)

        if (cost != False):
            cost = cost.strip()
            if (not cost.replace('.', '', 1).isdigit()):
                cost_fault = "Please write a float number between 0 and 100000 with 2 decimal places for cost"
                error_occured = True
            else:
                cost = float(cost)
                if (cost > 99999.99 or cost < 0):
                    cost_fault = "Please write a float number between 0 and 100000 with 2 decimal places for cost"
                    error_occured = True
                else:
                    numbers = str(cost).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 2):
                        cost_fault = "Please write a float number between 0 and 100000 with 2 decimal places for cost"
                        error_occured = True

        if (quantity != False):
            quantity = quantity.strip()
            if (not quantity.replace('.', '', 1).isdigit()):
                quantity_fault = "Please write a float number between 0 and 15000 (Capacity of Tanks) with 3 decimal places for quantity"
                error_occured = True
            else:
                quantity = float(quantity)
                if (quantity > 15000 or quantity < 0):
                    quantity_fault = "Please write a float number between 0 and 15000 (Capacity of Tanks) with 3 decimal places for quantity"
                    error_occured = True
                else:
                    numbers = str(quantity).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 3):
                        quantity_fault = "Please write a float number between 0 and 15000 (Capacity of Tanks) with 3 decimal places for quantity"
                        error_occured = True

        if (not error_occured):
            if "add_consists_of" in request.POST:
                try:
                    ConsistsOf.insertInto(int(supply_id), int(
                        prod_id), float(cost), float(quantity))
                    return redirect(consistOf)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_consists_of" in request.POST:
                try:
                    consistsOf = ConsistsOf.searchBy(
                        int(supply_id), int(prod_id), float(cost), float(quantity))
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    ConsistsOf.update(int(supply_id), int(prod_id), float(
                        cost), float(quantity), int(previous_prod_id))
                    return redirect(consistOf)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            consistsOf = ConsistsOf.retrieveAllColumns()
    else:
        consistsOf = ConsistsOf.retrieveAllColumns()
    return render(request, 'consistsOf.html', {'consistsOf': consistsOf, 'supply_id_fault': supply_id_fault, 'prod_id_fault': prod_id_fault, 'cost_fault': cost_fault, 'quantity_fault': quantity_fault})


def consistsOf_delete(request, supply_prod):
    ConsistsOf.delete(supply_prod)
    return redirect(consistOf)


def contract(request):
    id_fault = False
    start_date_fault = False
    end_date_fault = False
    salary_fault = False

    if request.method == "POST":
        id = request.POST.get('id', False)
        start_date = request.POST.get('start-date', False)
        end_date = request.POST.get('end-date', False)
        salary = request.POST.get('salary', False)

        error_occured = False

        if (id != False):
            id = id.strip()
            if (not id.isdigit()):
                id_fault = "Please write a positive integer for id"
                error_occured = True
            else:
                all_contracts = Contract.allContractIds()
                id = int(id)
                check_contract = (id, )
                if (id < 0):
                    id_fault = "Please write a positive integer for id"
                    error_occured = True
                # check if contract id already exists when trying to add new contract
                if (check_contract in all_contracts and "add_contract" in request.POST):
                    id_fault = "Please write a valid id. Contract id already exists"
                    error_occured = True

        if (start_date != False):
            start_date = start_date.strip()
            start_date = start_date.split('-')
            start_date = '/'.join(start_date[::-1])
            if (not start_date.replace('/', '', 2).isdigit()):
                start_date_fault = "Please write a valid Start Date"
                error_occured = True

        if (end_date != False):
            end_date = end_date.strip()
            end_date = end_date.split('-')
            end_date = '/'.join(end_date[::-1])
            if (not end_date.replace('/', '', 2).isdigit()):
                end_date_fault = "Please write a valid end date"
                error_occured = True
            elif (start_date != False):
                s_date = start_date.split('/')
                s_date = datetime(int(s_date[2]), int(
                    s_date[1]), int(s_date[0]))

                e_date = end_date.split('/')
                e_date = datetime(int(e_date[2]), int(
                    e_date[1]), int(e_date[0]))

                if (e_date.date() < datetime.today().date()):
                    end_date_fault = "End date should be greater than today"
                    error_occured = True
                elif (s_date.date() > e_date.date()):
                    end_date_fault = "End date should be greater than start date"
                    error_occured = True

        if (salary != False):
            salary = salary.strip()
            if (not salary.replace('.', '', 1).isdigit()):
                salary_fault = "Please write a float number between 0 and 100000 with 2 decimal places for salary"
                error_occured = True
            else:
                salary = float(salary)
                if (salary > 99999.99 or salary < 0):
                    salary_fault = "Please write a float number between 0 and 100000 with 2 decimal places for salary"
                    error_occured = True
                else:
                    numbers = str(salary).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 2):
                        salary_fault = "Please write a float number between 0 and 100000 with 2 decimal places for salary"
                        error_occured = True

        if (not error_occured):
            if "add_contract" in request.POST:
                try:
                    Contract.insertInto(id, start_date, end_date, salary)
                    return redirect(contract)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_contract" in request.POST:
                try:
                    contracts = Contract.searchBy(
                        id, start_date, end_date, salary)
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Contract.update(id, start_date, end_date, salary)
                    return redirect(contract)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            contracts = Contract.retrieveAllColumns()
    else:
        contracts = Contract.retrieveAllColumns()

    all_contracts = Contract.retrieveAllColumns()
    return render(request, 'contract.html', {'contracts': contracts, 'number_of_contracts': len(all_contracts), 'id_fault': id_fault, 'start_date_fault': start_date_fault, 'end_date_fault': end_date_fault, 'salary_fault': salary_fault})


def contract_delete(request, id):
    Contract.delete(id)
    return redirect(contract)


def customer(request):
    email_fault = False
    first_name_fault = False
    last_name_fault = False
    birth_date_fault = False
    phone_number_fault = False
    longitude_fault = False
    latitude_fault = False
    remaining_points_fault = False

    if request.method == "POST":
        email = request.POST.get('email', False)
        first_name = request.POST.get('first-name', False)
        last_name = request.POST.get('last-name', False)
        birth_date = request.POST.get('birth-date', False)
        phone_number = request.POST.get('phone-number', False)
        longitude = request.POST.get('longitude', False)
        latitude = request.POST.get('latitude', False)
        remaining_points = request.POST.get('remaining-points', False)

        error_occured = False

        if (first_name != False):
            first_name = first_name.strip()
            if (not first_name.isalpha()):
                first_name_fault = "Please write a valid first name"
                error_occured = True
            else:
                first_name = first_name.capitalize()

        if (email != False):
            email = email.strip()
            try:
                validation = validate_email(email)
                email = validation.email
                # check if the email belongs to another customer
                if (not error_occured):
                    all_customer_emails = Customer.allCustomerEmails()
                    check_customer_emails = (email, )
                    all_customer_names = Customer.allCustomerNames()
                    first_name = first_name.strip()
                    check_customer_names = (first_name, )
                    if ((check_customer_emails in all_customer_emails) and (check_customer_names not in all_customer_names) and ("add_customer" in request.POST)):
                        email_fault = "Please write a valid email. This email belongs to another customer"
                    error_occured = True
            except EmailNotValidError as e:
                email_fault = str(e)
                error_occured = True

        if (last_name != False):
            last_name = last_name.strip()
            if (not last_name.isalpha()):
                last_name_fault = "Please write a valid last name"
                error_occured = True
            else:
                last_name = last_name.capitalize()

        if (birth_date != False):
            birth_date = birth_date.strip()
            birth_date = birth_date.split('-')
            birth_date = '/'.join(birth_date[::-1])
            if (not birth_date.replace('/', '', 2).isdigit()):
                birth_date_fault = "Please write a valid Birth Date (older than 18)"
                error_occured = True
            b_date = birth_date.split('/')
            b_date = datetime(int(b_date[2]), int(b_date[1]), int(b_date[0]))

            today = str(datetime.today().date())
            today = today.split('-')
            today = '/'.join(today[::-1])
            today = today.split('/')
            valid_date = datetime(
                int(today[2])-8, int(today[1]), int(today[0]))

            if (b_date.date() > valid_date.date()):
                birth_date_fault = "Please write a valid Birth Date (older than 18)"
                error_occured = True

        if (phone_number != False):
            phone_number = phone_number.strip()
            if (not phone_number.isdigit()):
                phone_number_fault = "Please write a integer between 6900000000 and 6999999999 for Phone Number"
                error_occured = True
            else:
                all_phone_numbers = Customer.allCustomerPhoneNumbers()
                phone_number = int(phone_number)
                check_phone_number = (phone_number, )
                # check if phone number already exists when trying to add new customer
                if (check_phone_number in all_phone_numbers and "add_customer" in request.POST):
                    phone_number_fault = "Please write a positive integer for Phone Number. Phone Number already exists"
                    error_occured = True
                if (phone_number > 6999999999 or phone_number < 6900000000):
                    phone_number_fault = "Please write a integer between 6900000000 and 6999999999 for Phone Number"
                    error_occured = True

        if (longitude != False):
            longitude = longitude.strip()
            if (not longitude.replace('.', '', 1).isdigit()):
                longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                error_occured = True
            else:
                longitude = float(longitude)
                if (longitude > 99.999999 or longitude < 0):
                    longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                    error_occured = True
                else:
                    numbers = str(longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                        error_occured = True

        if (latitude != False):
            latitude = latitude.strip()
            if (not latitude.replace('.', '', 1).isdigit()):
                latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                error_occured = True
            else:
                latitude = float(latitude)
                if (latitude > 999.999999 or latitude < 0):
                    latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                    error_occured = True
                else:
                    numbers = str(latitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                        error_occured = True

        if (remaining_points != False):
            remaining_points = remaining_points.strip()
            if (not remaining_points.isdigit()):
                remaining_points_fault = "Please write a integer between 0 and 990 for Remaining Points"
                error_occured = True
            else:
                remaining_points = int(remaining_points)
                if (remaining_points > 990 or remaining_points < 0):
                    remaining_points_fault = "Please write a integer between 0 and 990 for Remaining Points"
                    error_occured = True

        if (not error_occured):
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
                    customers = Customer.searchBy(
                        email, phone_number, int(remaining_points))
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
    else:
        customers = Customer.retrieveAllColumns()
    return render(request, 'customer.html', {'customers': customers, 'first_name_fault': first_name_fault, 'last_name_fault': last_name_fault, 'email_fault': email_fault, 'birth_date_fault': birth_date_fault, 'phone_number_fault': phone_number_fault, 'longitude_fault': longitude_fault, 'latitude_fault': latitude_fault, 'remaining_points_fault': remaining_points_fault})


def customer_delete(request, email):
    Customer.delete(email)
    return redirect(customer)


def employee(request):
    ssn_fault = False
    first_name_fault = False
    last_name_fault = False
    birth_date_fault = False
    phone_number_fault = False
    email_fault = False
    longitude_fault = False
    latitude_fault = False
    role_fault = False
    hours_fault = False
    super_ssn_fault = False
    gs_longitude_fault = False
    gs_latitude_fault = False

    if request.method == "POST":
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

        error_occured = False

        if (ssn != False):
            ssn = ssn.strip()
            ssn_check = ssn.split('-')
            if (not ''.join(ssn_check).isdigit() or len(ssn_check[0]) != 3 or len(ssn_check[1]) != 2 or len(ssn_check[2]) != 4):
                ssn_fault = "Please write a valid ssn with this format 'xxx-xx-xxxx'"
                error_occured = True
            else:
                all_ssn = Employee.allSsn()
                # only by this way we can compare values with sqlite response
                ssn_check = (ssn, )
                # only when we try to add an employee we check to see if the specified id already exists
                if ((ssn_check in all_ssn) and ("add_employee" in request.POST)):
                    ssn_fault = "Ssn already exists"
                    error_occured = True

        if (first_name != False):
            first_name = first_name.strip()
            if (not first_name.isalpha()):
                first_name_fault = "Please write a valid first name"
                error_occured = True
            else:
                first_name = first_name.capitalize()

        if (last_name != False):
            last_name = last_name.strip()
            if (not last_name.isalpha()):
                last_name_fault = "Please write a valid last name"
                error_occured = True
            else:
                last_name = last_name.capitalize()

        if (birth_date != False):
            birth_date = birth_date.strip()
            birth_date = birth_date.split('-')
            birth_date = '/'.join(birth_date[::-1])
            if (not birth_date.replace('/', '', 2).isdigit()):
                birth_date_fault = "Please write a valid Birth Date (older than 18)"
                error_occured = True
            b_date = birth_date.split('/')
            b_date = datetime(int(b_date[2]), int(b_date[1]), int(b_date[0]))

            today = str(datetime.today().date())
            today = today.split('-')
            today = '/'.join(today[::-1])
            today = today.split('/')
            valid_date = datetime(
                int(today[2])-8, int(today[1]), int(today[0]))

            if (b_date.date() > valid_date.date()):
                birth_date_fault = "Please write a valid Birth Date (older than 18)"
                error_occured = True

        if (phone_number != False):
            phone_number = phone_number.strip()
            if (not phone_number.isdigit()):
                phone_number_fault = "Please write a integer between 6900000000 and 6999999999 for Phone Number"
                error_occured = True
            else:
                all_phone_numbers = Employee.allPhoneNumbers()
                phone_number = int(phone_number)
                check_phone_number = (phone_number, )
                if (check_phone_number in all_phone_numbers and "add_employee" in request.POST):
                    phone_number_fault = "Please write a positive integer for Phone Number. Phone Number already exists"
                    error_occured = True
                if (phone_number > 6999999999 or phone_number < 6900000000):
                    phone_number_fault = "Please write a integer between 6900000000 and 6999999999 for Phone Number"
                    error_occured = True

        if (email != False):
            email = email.strip()
            try:
                validation = validate_email(email)
                email = validation.email
            except EmailNotValidError as e:
                email_fault = str(e)
                error_occured = True

        if (longitude != False):
            longitude = longitude.strip()
            if (not longitude.replace('.', '', 1).isdigit()):
                longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                error_occured = True
            else:
                longitude = float(longitude)
                if (longitude > 99.999999 or longitude < 0):
                    longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                    error_occured = True
                else:
                    numbers = str(longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                        error_occured = True

        if (latitude != False):
            latitude = latitude.strip()
            if (not latitude.replace('.', '', 1).isdigit()):
                latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                error_occured = True
            else:
                latitude = float(latitude)
                if (latitude > 999.999999 or latitude < 0):
                    latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                    error_occured = True
                else:
                    numbers = str(latitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                        error_occured = True

        if (role != False):
            role = role.strip()
            if (not role.replace(' ', '', 1).isalpha()):
                role_fault = "Please write a valid role"
                error_occured = True
            else:
                all_roles = Employee.allRoles()
                role_check = (role, )
                # when trying to add or update employee we don't want a role other than the ones already specified to be added
                if ("search_employee" not in request.POST):
                    if (role_check not in all_roles):
                        role_fault = "Please write a valid role"
                        error_occured = True

        if (hours != False):
            hours = hours.strip()
            if (not hours.isdigit()):
                hours_fault = "Please write a integer between 0 and 168(All 7 days, all 24 hours) for hours"
                error_occured = True
            else:
                hours = int(hours)
                if (hours > 168 or hours < 1):
                    hours_fault = "Please write a integer between 0 and 168(All 7 days, all 24 hours) for hours"
                    error_occured = True

        if (super_ssn != False):
            super_ssn = super_ssn.strip()
            super_ssn_check = super_ssn.split('-')
            all_mgr_ssn = Employee.allMgrSsn()
            if (super_ssn != 'NULL'):
                if (not ''.join(super_ssn_check).isdigit() or len(super_ssn_check[0]) != 3 or len(super_ssn_check[1]) != 2 or len(super_ssn_check[2]) != 4):
                    ssn_fault = "Please write a valid super ssn with this format: xxx-xx-xxxx"
                    error_occured = True
                else:
                    super_ssn_check = (super_ssn, )
                    if ((super_ssn_check not in all_mgr_ssn) and ("search_employee" not in request.POST)):
                        super_ssn_fault = "Please write a valid super ssn. This manager does not exist"
                        error_occured = True
                    elif ((role == 'Manager') and ("search_employee" not in request.POST)):
                        super_ssn_fault = "A manager cannot be assigned to another manager"
                        error_occured = True
            else:
                if (role != 'Manager'):
                    super_ssn_fault = "Please write a valid super ssn. An employee must have a Manager"
                    error_occured = True

        if (gs_longitude != False):
            gs_longitude = gs_longitude.strip()
            if (gs_longitude != ''):
                if ((role == 'Manager') and ("add_employee" in request.POST)):
                    gs_longitude_fault = "If you are trying to add a Manager the GS Longitude should be NULL"
                    error_occured = True
                elif (not gs_longitude.replace('.', '', 1).isdigit()):
                    gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                    error_occured = True
                else:
                    gs_longitude = float(gs_longitude)
                    if (gs_longitude > 99.999999 or gs_longitude < 0):
                        gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                        error_occured = True
                    else:
                        numbers = str(gs_longitude).split('.')
                        decimal_part = numbers[1]
                        if (len(decimal_part) > 6):
                            gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                            error_occured = True
            else:
                if ((role != 'Manager') and (super_ssn != 'NULL') and ("search_employee" not in request.POST)):
                    gs_longitude_fault = "Gas station longitude cannot have NULL value if the employee is not a manager"
                    error_occured = True
                else:
                    gs_longitude = None

        if (gs_latitude != False):
            gs_latitude = gs_latitude.strip()
            if (gs_latitude != ''):
                if ((role == 'Manager') and ("add_employee" in request.POST)):
                    gs_latitude_fault = "If you are trying to add a Manager the GS Latitude should be NULL"
                    error_occured = True
                elif (not gs_latitude.replace('.', '', 1).isdigit()):
                    gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                    error_occured = True
                else:
                    gs_latitude = float(gs_latitude)
                    if (gs_latitude > 999.999999 or gs_latitude < 0):
                        gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                        error_occured = True
                    else:
                        numbers = str(gs_latitude).split('.')
                        decimal_part = numbers[1]
                        gs_longitude_latitude_check = (
                            gs_longitude, gs_latitude)
                        all_gs_longitudes_latitudes = GasStation.allGSLongitudesLatitudes()
                        if (len(decimal_part) > 6):
                            gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                            error_occured = True
                        elif ((gs_longitude_latitude_check not in all_gs_longitudes_latitudes) and ("search_employee" not in request.POST)):
                            gs_longitude_fault = "Specify an existing gas station longitude"
                            gs_latitude_fault = "Specify an existing gas station latitude"
                            error_occured = True
                        else:
                            # gs should be full-service to have attendants
                            if (role == "Fuel Attendant" or role == "Gas Attendant"):
                                gs_longitude_latitude_with_attendants = Employee.getGSLongitudeLatitudeAttendants()
                                if ((gs_longitude_latitude_check not in gs_longitude_latitude_with_attendants) and ("search_employee" not in request.POST)):
                                    gs_longitude_fault = "Please specify a longitude for a gas station that is full service"
                                    gs_latitude_fault = "Please specify a latitude for a gas station that is full service"
                                    error_occured = True
                            # gs shouldn't be self-service and should have minimarket and shouldn't have already one cashier
                            elif (role == "Cashier"):
                                # all gs that are self-service and don't have minimarkets
                                gs_longitude_latitude_with_no_minimarket_self_service = GasStation.getGSLongitudeLatitudeNoMinimarketSelf()
                                if ((gs_longitude_latitude_check in gs_longitude_latitude_with_no_minimarket_self_service) and ("search_employee" not in request.POST)):
                                    gs_longitude_fault = "Please specify a longitude for a gas station that is full service and has minimarket"
                                    gs_latitude_fault = "Please specify a latitude for a gas station that is full service and has minimarket"
                                    error_occured = True
                                if (Employee.hasCashier(gs_longitude, gs_latitude)):
                                    gs_longitude_fault = "Please specify a longitude for a gas station that does not already have a cashier"
                                    gs_latitude_fault = "Please specify a latitude for a gas station that does not already have a cashier"
                                    error_occured = True
            else:
                if ((role != 'Manager') and (super_ssn != 'NULL') and ("search_employee" not in request.POST)):
                    gs_latitude_fault = "Gas station latitude cannot have NULL value if the employee is not a manager"
                    error_occured = True
                else:
                    gs_latitude = None

        if (not error_occured):
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
                    employees = Employee.searchBy(
                        ssn, role, super_ssn, gs_longitude, gs_latitude)
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
    else:
        employees = Employee.retrieveAllColumns()
    return render(request, 'employee.html', {'employees': employees, 'ssn_fault': ssn_fault, 'first_name_fault': first_name_fault, 'last_name_fault': last_name_fault, 'birth_date_fault': birth_date_fault, 'phone_number_fault': phone_number_fault, 'email_fault': email_fault, 'longitude_fault': longitude_fault, 'latitude_fault': latitude_fault, 'role_fault': role_fault, 'hours_fault': hours_fault, 'super_ssn_fault': super_ssn_fault, 'gs_longitude_fault': gs_longitude_fault, 'gs_latitude_fault': gs_latitude_fault})


def employee_delete(request, ssn):
    Employee.delete(ssn)
    return redirect(employee)


def entail(request):
    serv_id_fault = False
    pur_id_fault = False

    if request.method == "POST":
        serv_id = request.POST.get('serv-id', False)
        pur_id = request.POST.get('pur-id', False)
        previous_serv_id = request.POST.get('previous-serv-id', False)

        error_occured = False

        if (serv_id != False):
            serv_id = serv_id.strip()
            if (not serv_id.isdigit()):
                serv_id_fault = "Please write a positive integer for Service ID"
                error_occured = True
            else:
                serv_id = int(serv_id)

        if (pur_id != False):
            pur_id = pur_id.strip()
            if (not pur_id.isdigit()):
                pur_id_fault = "Please write a positive integer for Purchase ID"
                error_occured = True
            else:
                pur_id = int(pur_id)

        if (not error_occured):
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
                    Entails.update(int(serv_id), int(
                        pur_id), int(previous_serv_id))
                    return redirect(entail)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            entails = Entails.retrieveAllColumns()
    else:
        entails = Entails.retrieveAllColumns()
    return render(request, 'entails.html', {'entails': entails, 'serv_id_fault': serv_id_fault, 'pur_id_fault': pur_id_fault})


def entails_delete(request, serv_pur):
    Entails.delete(serv_pur)
    return redirect(entail)


def gasStation(request):
    longitude_fault = False
    latitude_fault = False
    type_of_service_fault = False
    start_date_fault = False
    minimarket_fault = False
    mgr_ssn_fault = False

    if request.method == "POST":
        longitude = request.POST.get('longitude', False)
        latitude = request.POST.get('latitude', False)
        type_of_service = request.POST.get('type-of-service', False)
        start_date = request.POST.get('start-date', False)
        minimarket = request.POST.get('minimarket', False)
        mgr_ssn = request.POST.get('mgr-ssn', False)

        error_occured = False

        if (longitude != False):
            longitude = longitude.strip()
            if (not longitude.replace('.', '', 1).isdigit()):
                longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                error_occured = True
            else:
                longitude = float(longitude)
                if (longitude > 99.999999 or longitude < 0):
                    longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                    error_occured = True
                else:
                    numbers = str(longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                        error_occured = True

        if (latitude != False):
            latitude = latitude.strip()
            if (not latitude.replace('.', '', 1).isdigit()):
                latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                error_occured = True
            else:
                latitude = float(latitude)
                if (latitude > 999.999999 or latitude < 0):
                    latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                    error_occured = True
                else:
                    numbers = str(latitude).split('.')
                    decimal_part = numbers[1]
                    longitude_latitude_check = (
                        longitude, latitude)
                    all_longitudes_latitudes = GasStation.allGSLongitudesLatitudes()
                    if (len(decimal_part) > 6):
                        latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                        error_occured = True
                    elif ((longitude_latitude_check in all_longitudes_latitudes) and ("search_employee" not in request.POST)):
                        longitude_fault = "Specify a new gas station longitude"
                        latitude_fault = "Specify a new gas station latitude"
                        error_occured = True

        if (type_of_service != False):
            type_of_service = type_of_service.strip()
            if (not type_of_service.replace(' ', '', 1).isalpha()):
                type_of_service_fault = "Please write a valid type of service"
                error_occured = True
            else:
                all_types_of_service = GasStation.allTypesOfService()
                type_of_service_check = (type_of_service, )
                if ((type_of_service_check not in all_types_of_service) and "search_gas_station" not in request.POST):
                    type_of_service_fault = "Please write a valid type of service"
                    error_occured = True

        if (start_date != False):
            start_date = start_date.strip()
            start_date = start_date.split('-')
            start_date = '/'.join(start_date[::-1])
            if (not start_date.replace('/', '', 2).isdigit()):
                start_date_fault = "Please write a valid Start Date"
                error_occured = True
            s_date = start_date.split('/')
            s_date = datetime(int(s_date[2]), int(s_date[1]), int(s_date[0]))

            if (s_date.date() > datetime.today().date()):
                start_date_fault = "Start Date should be earlier than today"
                error_occured = True

        if (minimarket != False):
            minimarket = minimarket.strip()
            if (not minimarket.isdigit()):
                minimarket_fault = "Please write a integer between 0(false) and 1(true) for the existence of a Minimarket"
                error_occured = True
            else:
                minimarket = int(minimarket)
                if (minimarket > 1 or minimarket < 0):
                    minimarket_fault = "Please write a integer between 0(false) and 1(true) for the existence of a Minimarket"
                    error_occured = True

        if (mgr_ssn != False):
            mgr_ssn = mgr_ssn.strip()
            mgr_ssn_check = mgr_ssn.split('-')
            all_mgr_ssn = Employee.allMgrSsn()
            if (not ''.join(mgr_ssn_check).isdigit() or len(mgr_ssn_check[0]) != 3 or len(mgr_ssn_check[1]) != 2 or len(mgr_ssn_check[2]) != 4):
                mgr_ssn_fault = "Please write a valid manager ssn with this format: xxx-xx-xxxx"
                error_occured = True
            else:
                mgr_ssn_check = (mgr_ssn, )
                new_mgr_ssn = Employee.newMgrSsns()
                if ((mgr_ssn_check not in all_mgr_ssn)):
                    mgr_ssn_fault = "Please write a valid manager ssn. This employee does not exist"
                    error_occured = True
                else:
                    if (len(new_mgr_ssn) == 0):
                        mgr_ssn_fault = "Please create a manager ssn. This employee does not exist"
                        error_occured = True

        if (not error_occured):
            if "add_gas_station" in request.POST:
                try:
                    GasStation.insertInto(longitude, latitude, type_of_service, start_date,
                                          minimarket, mgr_ssn)
                    Employee.updateManagerGSCoords(
                        mgr_ssn, longitude, latitude)
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
    else:
        gasStations = GasStation.retrieveAllColumns()
    return render(request, 'gasStation.html', {'gasStations': gasStations, 'longitude_fault': longitude_fault, 'latitude_fault': latitude_fault, 'type_of_service_fault': type_of_service_fault, 'start_date_fault': start_date_fault, 'minimarket_fault': minimarket_fault, 'mgr_ssn_fault': mgr_ssn_fault})


def gasStation_delete(request, longitude_latitude):
    GasStation.delete(longitude_latitude)
    return redirect(gasStation)


def involve(request):
    prod_id_fault = False
    pur_id_fault = False
    quantity_fault = False

    if request.method == "POST":
        prod_id = request.POST.get('prod-id', False)
        pur_id = request.POST.get('pur-id', False)
        quantity = request.POST.get('quantity', False)
        previous_prod_id = request.POST.get('previous-prod-id', False)

        error_occured = False

        if (prod_id != False):
            prod_id = prod_id.strip()
            if (not prod_id.isdigit()):
                prod_id_fault = "Please write a positive integer for Product ID"
                error_occured = True
            else:
                prod_id = int(prod_id)

        if (pur_id != False):
            pur_id = pur_id.strip()
            if (not pur_id.isdigit()):
                pur_id_fault = "Please write a positive integer for Purchase ID"
                error_occured = True
            else:
                pur_id = int(pur_id)

        if (quantity != False):
            quantity = quantity.strip()
            if (not quantity.replace('.', '', 1).isdigit()):
                quantity_fault = "Please write a float number between 0 and 15000 (Capacity of Tanks) with 3 decimal places for quantity"
                error_occured = True
            else:
                quantity = float(quantity)
                if (quantity > 15000 or quantity < 0):
                    quantity_fault = "Please write a float number between 0 and 15000 (Capacity of Tanks) with 3 decimal places for quantity"
                    error_occured = True
                else:
                    numbers = str(quantity).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 3):
                        quantity_fault = "Please write a float number between 0 and 15000 (Capacity of Tanks) with 3 decimal places for quantity"
                        error_occured = True

        if (not error_occured):
            if "add_involves" in request.POST:
                try:
                    Involves.insertInto(
                        int(prod_id), int(pur_id), float(quantity))
                    return redirect(involve)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_involves" in request.POST:
                try:
                    involves = Involves.searchBy(
                        int(prod_id), int(pur_id), float(quantity))
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Involves.update(int(prod_id), int(pur_id), float(
                        quantity), int(previous_prod_id))
                    return redirect(involve)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            involves = Involves.retrieveAllColumns()
    else:
        involves = Involves.retrieveAllColumns()
    return render(request, 'involves.html', {'involves': involves, 'prod_id_fault': prod_id_fault, 'pur_id_fault': pur_id_fault, 'quantity_fault': quantity_fault})


def involves_delete(request, prod_pur):
    Involves.delete(prod_pur)
    return redirect(involve)


def isAssignedTo(request):
    essn_fault = False
    service_id_fault = False

    if request.method == "POST":
        essn = request.POST.get('essn', False)
        service_id = request.POST.get('service-id', False)
        previous_service_id = request.POST.get('previous-service-id', False)

        error_occured = False

        if (essn != False):
            essn = essn.strip()
            essn_check = ''.join(essn.split('-'))
            all_ssn = Employee.allSsn()
            if (essn == 'NULL'):
                pass
            elif (not essn_check.isdigit() or len(essn) != 9):
                essn_fault = "Please write a valid ssn with 9 digits with this format 'xxx-xx-xxxx'"
                error_occured = True
            elif (essn not in all_ssn):
                essn_fault = "Please write a valid ssn. This employee does not exist"
                error_occured = True

        if (service_id != False):
            service_id = service_id.strip()
            if (not service_id.isdigit()):
                service_id = "Please write a positive integer for Service ID"
                error_occured = True
            else:
                service_id = int(service_id)

        if (not error_occured):
            if "add_assignment" in request.POST:
                try:
                    IsAssignedTo.insertInto(essn, int(service_id))
                    return redirect(isAssignedTo)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_assignment" in request.POST:
                try:
                    assignments = IsAssignedTo.searchBy(essn, int(service_id))
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    IsAssignedTo.update(essn, int(service_id),
                                        int(previous_service_id))
                    return redirect(isAssignedTo)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            assignments = IsAssignedTo.retrieveAllColumns()
    else:
        assignments = IsAssignedTo.retrieveAllColumns()
    return render(request, 'isAssignedTo.html', {'assignments': assignments, 'essn_fault': essn_fault, 'service_id_fault': service_id_fault})


def isAssignedTo_delete(request, essn_servid):
    IsAssignedTo.delete(essn_servid)
    return redirect(isAssignedTo)


def offer(request):
    prod_id_fault = False
    gs_longitude_fault = False
    gs_latitude_fault = False
    quantity_fault = False

    if request.method == "POST":
        prod_id = request.POST.get('prod-id', False)
        previous_prod_id = request.POST.get('previous-prod-id', False)
        gs_longitude = request.POST.get('gs-longitude', False)
        gs_latitude = request.POST.get('gs-latitude', False)
        quantity = request.POST.get('quantity', False)

        error_occured = False

        if (prod_id != False):
            prod_id = prod_id.strip()
            if (not prod_id.isdigit()):
                prod_id_fault = "Please write a positive integer for Product ID"
                error_occured = True
            else:
                prod_id = int(prod_id)

        if (gs_longitude != False):
            gs_longitude = gs_longitude.strip()
            if (not gs_longitude.replace('.', '', 1).isdigit()):
                gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                error_occured = True
            else:
                gs_longitude = float(gs_longitude)
                if (gs_longitude > 99.999999 or gs_longitude < 0):
                    gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                    error_occured = True
                else:
                    numbers = str(gs_longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                        error_occured = True

        if (gs_latitude != False):
            gs_latitude = gs_latitude.strip()
            if (not gs_latitude.replace('.', '', 1).isdigit()):
                gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                error_occured = True
            else:
                gs_latitude = float(gs_latitude)
                if (gs_latitude > 999.999999 or gs_latitude < 0):
                    gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                    error_occured = True
                else:
                    numbers = str(gs_latitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                        error_occured = True

        if (quantity != False):
            quantity = quantity.strip()
            if (not quantity.replace('.', '', 1).isdigit()):
                quantity_fault = "Please write a float number between 0 and 15000 (Capacity of Tanks) with 3 decimal places for quantity"
                error_occured = True
            else:
                quantity = float(quantity)
                if (quantity > 15000 or quantity < 0):
                    quantity_fault = "Please write a float number between 0 and 15000 (Capacity of Tanks) with 3 decimal places for quantity"
                    error_occured = True
                else:
                    numbers = str(quantity).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 3):
                        quantity_fault = "Please write a float number between 0 and 15000 (Capacity of Tanks) with 3 decimal places for quantity"
                        error_occured = True

        if (not error_occured):
            if "add_offers" in request.POST:
                try:
                    Offers.insertInto(int(prod_id), float(
                        gs_longitude), float(gs_latitude), float(quantity))
                    return redirect(offer)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_offers" in request.POST:
                try:
                    offers = Offers.searchBy(int(prod_id), float(
                        gs_longitude), float(gs_latitude), float(quantity))
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Offers.update(int(prod_id), int(previous_prod_id), float(gs_longitude),
                                  float(gs_latitude), float(quantity))
                    return redirect(offer)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            offers = Offers.retrieveAllColumns()
    else:
        offers = Offers.retrieveAllColumns()
    return render(request, 'offers.html', {'offers': offers, 'prod_id_fault': prod_id_fault, 'gs_longitude_fault': gs_longitude_fault, 'gs_latitude_fault': gs_latitude_fault, 'quantity_fault': quantity_fault})


def offer_delete(request, prodid_longitude_latitude):
    Offers.delete(prodid_longitude_latitude)
    return redirect(offer)


def product(request):
    id_fault = False
    name_fault = False
    type_of_product_fault = False
    price_fault = False
    corresponding_points_fault = False

    if request.method == "POST":
        id = request.POST.get('id', False)
        name = request.POST.get('name', False)
        type_of_product = request.POST.get('type', False)
        price = request.POST.get('price', False)
        corresponding_points = request.POST.get('corresponding-points', False)

        error_occured = False

        if (id != False):
            id = id.strip()
            if (not id.isdigit()):
                id_fault = "Please write a positive integer for id"
                error_occured = True
            else:
                all_products = Product.allProductIds()
                id = int(id)
                check_product = (id, )
                if (id < 0):
                    id_fault = "Please write a positive integer for id"
                    error_occured = True
                # check if product id already exists when trying to add new product
                if (check_product in all_products and "add_product" in request.POST):
                    id_fault = "Please write a positive integer for id. Product id already exists"
                    error_occured = True

        if (name != False):
            name = name.strip()
            if (not name.isalpha()):
                name_fault = "Please write a valid product name"
                error_occured = True
            else:
                all_product_names = Product.allProductNames()
                if (name in all_product_names and "add_product" in request.POST):
                    name_fault = "Please write a valid product. Product name already exists"
                    error_occured = True
                name = name.capitalize()

        if (type_of_product != False):
            type_of_product = type_of_product.strip()
            all_types_of_product = Product.allTypesOfProduct()
            if (type_of_product not in all_types_of_product and "search_product" not in request.POST):
                type_of_product_fault = "Please write a valid type of product. The types are Fuel, Special Products and Minimarket Products"
                error_occured = True

        if (price != False):
            price = price.strip()
            if (not price.replace('.', '', 1).isdigit()):
                price_fault = "Please write a float number between 0 and 10000 with 2 decimal places for price"
                error_occured = True
            else:
                price = float(price)
                if (price > 9999.99 or price < 0):
                    price_fault = "Please write a float number between 0 and 10000 with 2 decimal places for price"
                    error_occured = True
                else:
                    numbers = str(price).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 2):
                        price_fault = "Please write a float number between 0 and 10000 with 2 decimal places for price"
                        error_occured = True

        if (corresponding_points != False):
            corresponding_points = corresponding_points.strip()
            if (not corresponding_points.isdigit()):
                corresponding_points_fault = "Please write a integer between 0 and 990 for Corresponding Points"
                error_occured = True
            else:
                corresponding_points = int(corresponding_points)
                if (corresponding_points > 990 or corresponding_points < 0):
                    corresponding_points_fault = "Please write a integer between 0 and 990 for Corresponding Points"
                    error_occured = True

        if (not error_occured):
            if "add_product" in request.POST:
                try:
                    Product.insertInto(id, name, type, price,
                                       int(corresponding_points))
                    return redirect(product)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_product" in request.POST:
                try:
                    products = Product.searchBy(
                        int(id), type, float(price), int(corresponding_points))
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Product.update(int(id), name, type, float(
                        price), int(corresponding_points))
                    return redirect(product)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            products = Product.retrieveAllColumns()
    else:
        products = Product.retrieveAllColumns()
    all_products = Product.retrieveAllColumns()
    return render(request, 'product.html', {'products': products, 'number_of_products': len(all_products), 'id_fault': id_fault, 'name_fault': name_fault, 'type_of_product_fault': type_of_product_fault, 'price_fault': price_fault, 'corresponding_points_fault': corresponding_points_fault})


def product_delete(request, id):
    Product.delete(id)
    return redirect(product)


def provide(request):
    serv_id_fault = False
    gs_longitude_fault = False
    gs_latitude_fault = False

    if request.method == "POST":
        serv_id = request.POST.get('serv-id', False)
        gs_longitude = request.POST.get('gs-longitude', False)
        gs_latitude = request.POST.get('gs-latitude', False)
        previous_serv_id = request.POST.get('previous-serv-id', False)

        error_occured = False

        if (serv_id != False):
            serv_id = serv_id.strip()
            if (not serv_id.isdigit()):
                serv_id_fault = "Please write a positive integer for Service ID"
                error_occured = True
            else:
                serv_id = int(serv_id)

        if (gs_longitude != False):
            gs_longitude = gs_longitude.strip()
            if (not gs_longitude.replace('.', '', 1).isdigit()):
                gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                error_occured = True
            else:
                gs_longitude = float(gs_longitude)
                if (gs_longitude > 99.999999 or gs_longitude < 0):
                    gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                    error_occured = True
                else:
                    numbers = str(gs_longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                        error_occured = True

        if (gs_latitude != False):
            gs_latitude = gs_latitude.strip()
            if (not gs_latitude.replace('.', '', 1).isdigit()):
                gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                error_occured = True
            else:
                gs_latitude = float(gs_latitude)
                if (gs_latitude > 999.999999 or gs_latitude < 0):
                    gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                    error_occured = True
                else:
                    numbers = str(gs_latitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                        error_occured = True

        if (not error_occured):
            if "add_provides" in request.POST:
                try:
                    Provides.insertInto(
                        int(serv_id), gs_longitude, gs_latitude)
                    return redirect(provide)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_provides" in request.POST:
                try:
                    provides = Provides.searchBy(
                        int(serv_id), gs_longitude, gs_latitude)
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Provides.update(int(serv_id), gs_longitude,
                                    gs_latitude, int(previous_serv_id))
                    return redirect(provide)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            provides = Provides.retrieveAllColumns()
    else:
        provides = Provides.retrieveAllColumns()
    return render(request, 'provides.html', {'provides': provides, 'serv_id_fault': serv_id_fault, 'gs_longitude_fault': gs_longitude_fault, 'gs_latitude_fault': gs_latitude_fault})


def provides_delete(request, serv_gslong_lat):
    Provides.delete(serv_gslong_lat)
    return redirect(provide)


def pump(request):
    id_fault = False
    tank_id_fault = False
    tank_gs_longitude_fault = False
    tank_gs_latitude_fault = False
    current_state_fault = False
    last_check_up_fault = False
    nozzle_last_check_up_fault = False
    product_quantity_fault = False

    if request.method == "POST":
        id = request.POST.get('pump-id', False)
        tank_id = request.POST.get('tank-id', False)
        tank_gs_longitude = request.POST.get('tank-gs-longitude', False)
        tank_gs_latitude = request.POST.get('tank-gs-latitude', False)
        current_state = request.POST.get('current-state', False)
        last_check_up = request.POST.get('last-check-up', False)
        nozzle_last_check_up = request.POST.get('nozzle-last-check-up', False)
        product_quantity = request.POST.get('product-quantity', False)

        error_occured = False

        if (id != False):
            id = id.strip()
            if (not id.isdigit()):
                id_fault = "Please write a positive integer for id"
                error_occured = True
            else:
                all_pumps = Pump.allPumpIds()
                id = int(id)
                check_pump = (id, )
                if (id < 0):
                    id_fault = "Please write a positive integer for id"
                    error_occured = True
                if (check_pump in all_pumps and "add_pump" in request.POST):
                    id_fault = "Please write a valid id. Pump id already exists"
                    error_occured = True

        if (tank_id != False):
            tank_id = tank_id.strip()
            if (not tank_id.isdigit()):
                tank_id_fault = "Please write a positive integer for Tank ID"
                error_occured = True
            else:
                tank_id = int(tank_id)

        if (tank_gs_longitude != False):
            tank_gs_longitude = tank_gs_longitude.strip()
            if (not tank_gs_longitude.replace('.', '', 1).isdigit()):
                tank_gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for the Gas Station Longitude of the Tank"
                error_occured = True
            else:
                tank_gs_longitude = float(tank_gs_longitude)
                if (tank_gs_longitude > 99.999999 or tank_gs_longitude < 0):
                    tank_gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for the Gas Station Longitude of the Tank"
                    error_occured = True
                else:
                    numbers = str(tank_gs_longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        tank_gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for the Gas Station Longitude of the Tank"
                        error_occured = True

        if (tank_gs_latitude != False):
            tank_gs_latitude = tank_gs_latitude.strip()
            if (not tank_gs_latitude.replace('.', '', 1).isdigit()):
                tank_gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for the Gas Station Latitude of the Tank"
                error_occured = True
            else:
                tank_gs_latitude = float(tank_gs_latitude)
                if (tank_gs_latitude > 999.999999 or tank_gs_latitude < 0):
                    tank_gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for the Gas Station Latitude of the Tank"
                    error_occured = True
                else:
                    numbers = str(tank_gs_latitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        tank_gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for the Gas Station Latitude of the Tank"
                        error_occured = True

        if (current_state != False):
            current_state = current_state.strip()
            if (not current_state.isdigit()):
                current_state_fault = "Please write a integer between 0(not used) and 1(used) for the current state of the pump"
                error_occured = True
            else:
                current_state = int(current_state)
                if (current_state > 1 or current_state < 0):
                    current_state_fault = "Please write a integer between 0(not used) and 1(used) for the current state of the pump"
                    error_occured = True

        if (last_check_up != False):
            last_check_up = last_check_up.strip()
            last_check_up = last_check_up.split('-')
            last_check_up = '/'.join(last_check_up[::-1])
            if (not last_check_up.replace('/', '', 2).isdigit()):
                last_check_up_fault = "Please write a valid date for the last check up of the pump"
                error_occured = True
            lcu_date = last_check_up.split('/')
            lcu_date = datetime(int(lcu_date[2]), int(
                lcu_date[1]), int(lcu_date[0]))

            if (lcu_date.date() > datetime.today().date()):
                last_check_up_fault = "Last Check Up for the pump should be before today"
                error_occured = True

        if (nozzle_last_check_up != False):
            nozzle_last_check_up = nozzle_last_check_up.strip()
            nozzle_last_check_up = nozzle_last_check_up.split('-')
            nozzle_last_check_up = '/'.join(nozzle_last_check_up[::-1])
            if (not nozzle_last_check_up.replace('/', '', 2).isdigit()):
                nozzle_last_check_up_fault = "Please write a valid date for the last check up of the pump nozzle"
                error_occured = True
            nlcu_date = nozzle_last_check_up.split('/')
            nlcu_date = datetime(int(nlcu_date[2]), int(
                nlcu_date[1]), int(nlcu_date[0]))

            if (nlcu_date.date() > datetime.today().date()):
                nozzle_last_check_up_fault = "Last Check Up for the pump nozzle should be before today"
                error_occured = True

        if (product_quantity != False):
            product_quantity = product_quantity.strip()
            if (not product_quantity.replace('.', '', 1).isdigit()):
                product_quantity_fault = "Please write a float number between 0 and 5000 (1/3 of Tank Capacity) with 3 decimal places for Product Quantity"
                error_occured = True
            else:
                product_quantity = float(product_quantity)
                if (product_quantity > 5000 or product_quantity < 0):
                    product_quantity_fault = "Please write a float number between 0 and 5000 (1/3 of Tank Capacity) with 3 decimal places for Product Quantity"
                    error_occured = True
                else:
                    numbers = str(product_quantity).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 3):
                        product_quantity_fault = "Please write a float number between 0 and 5000 (1/3 of Tank Capacity) with 3 decimal places for Product Quantity"
                        error_occured = True

        if (not error_occured):
            if "add_pump" in request.POST:
                try:
                    Pump.insertInto(int(id), int(tank_id), float(tank_gs_longitude), float(tank_gs_latitude), int(current_state),
                                    last_check_up, nozzle_last_check_up, float(product_quantity))
                    return redirect(pump)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_pump" in request.POST:
                try:
                    pumps = Pump.searchBy(int(id), int(tank_id), float(tank_gs_longitude), float(tank_gs_latitude), int(current_state),
                                          last_check_up, nozzle_last_check_up, float(product_quantity))
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Pump.update(int(id), int(tank_id), float(tank_gs_longitude), float(tank_gs_latitude), int(current_state),
                                last_check_up, nozzle_last_check_up, float(product_quantity))
                    return redirect(pump)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            pumps = Pump.retrieveAllColumns()
    else:
        pumps = Pump.retrieveAllColumns()
    all_pumps = Pump.retrieveAllColumns()
    return render(request, 'pump.html', {'pumps': pumps, 'number_of_pumps': len(all_pumps),  'id_fault': id_fault, 'tank_id_fault': tank_id_fault, 'tank_gs_longitude_fault': tank_gs_longitude_fault, 'tank_gs_latitude_fault': tank_gs_latitude_fault, 'current_state_fault': current_state_fault, 'current_state_fault': current_state_fault, 'last_check_up_fault': last_check_up_fault, 'nozzle_last_check_up_fault': nozzle_last_check_up_fault, 'product_quantity_fault': product_quantity_fault})


def pump_delete(request, id_tankId_tankLongitude_tankLatitude):
    Pump.delete(id_tankId_tankLongitude_tankLatitude)
    return redirect(pump)


def purchase(request):
    id_fault = False
    purchase_date_fault = False
    type_of_payment_fault = False
    customer_email_fault = False
    gs_longitude_fault = False
    gs_latitude_fault = False
    pump_id_fault = False
    tank_id_fault = False

    if request.method == "POST":
        id = request.POST.get('purchase-id', False)
        purchase_date = request.POST.get('purchase-date', False)
        type_of_payment = request.POST.get('type-of-payment', False)
        customer_email = request.POST.get('customer-email', False)
        gs_longitude = request.POST.get('gs-longitude', False)
        gs_latitude = request.POST.get('gs-latitude', False)
        pump_id = request.POST.get('pump-id', False)
        tank_id = request.POST.get('tank-id', False)

        error_occured = False

        if (id != False):
            id = id.strip()
            if (not id.isdigit()):
                id_fault = "Please write a positive integer for id"
                error_occured = True
            else:
                id = int(id)
                if (id < 0):
                    id_fault = "Please write a positive integer for id"
                    error_occured = True
                else:
                    all_purchases = Purchase.allPurchaseIds()
                    check_purchase = (id, )
                    if ((check_purchase in all_purchases) and ("add_purchase" in request.POST)):
                        id_fault = "Please write a valid id. Purchase id already exists"
                        error_occured = True

        if (purchase_date != False):
            purchase_date = purchase_date.strip()
            purchase_date = purchase_date.split('-')
            purchase_date = '/'.join(purchase_date[::-1])
            if (not purchase_date.replace('/', '', 2).isdigit()):
                purchase_date_fault = "Please write a valid Purchase Date"
                error_occured = True
            s_date = purchase_date.split('/')
            s_date = datetime(int(s_date[2]), int(s_date[1]), int(s_date[0]))

            if (s_date.date() > datetime.today().date()):
                purchase_date_fault = "Purchase Date should be before today"
                error_occured = True

        if (type_of_payment != False):
            type_of_payment = type_of_payment.strip()
            if (not type_of_payment.replace(' ', '', 1).isalpha()):
                type_of_payment_fault = "Please write a valid type of payment. The types are Cash, Debit Card and Credit Card"
                error_occured = True
            else:
                all_type_of_payments = Purchase.allTypeOfPayments()
                type_of_payment_check = (type_of_payment, )
                if ((type_of_payment_check not in all_type_of_payments) and ("search_purchase" not in request.POST)):
                    type_of_payment_fault = "Please write a valid type of payment. The types are Cash, Debit Card and Credit Card"
                    error_occured = True

        if (customer_email != False):
            customer_email = customer_email.strip()
            if (customer_email == ''):
                customer_email = None
            else:
                all_customer_emails = Customer.allCustomerEmails()
                customer_email_check = (customer_email, )
                if ((customer_email_check not in all_customer_emails) and ("search_purchase" not in request.POST)):
                    customer_email_fault = "Please specify an existing customer email."
                    error_occured = True

        if (gs_longitude != False):
            gs_longitude = gs_longitude.strip()
            if (not gs_longitude.replace('.', '', 1).isdigit()):
                gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                error_occured = True
            else:
                gs_longitude = float(gs_longitude)
                if (gs_longitude > 99.999999 or gs_longitude < 0):
                    gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                    error_occured = True
                else:
                    numbers = str(gs_longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                        error_occured = True

        if (gs_latitude != False):
            gs_latitude = gs_latitude.strip()
            if (not gs_latitude.replace('.', '', 1).isdigit()):
                gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                error_occured = True
            else:
                gs_latitude = float(gs_latitude)
                if (gs_latitude > 999.999999 or gs_latitude < 0):
                    gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                    error_occured = True
                else:
                    numbers = str(gs_latitude).split('.')
                    decimal_part = numbers[1]
                    gs_longitude_latitude_check = (
                        gs_longitude, gs_latitude)
                    all_gs_longitudes_latitudes = GasStation.allGSLongitudesLatitudes()
                    if (len(decimal_part) > 6):
                        gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                        error_occured = True
                    elif ((gs_longitude_latitude_check not in all_gs_longitudes_latitudes) and ("search_purchase" not in request.POST)):
                        gs_longitude_fault = "Specify an existing gas station longitude"
                        gs_latitude_fault = "Specify an existing gas station latitude"
                        error_occured = True

        if (tank_id != False):
            tank_id = tank_id.strip()
            if (tank_id == ''):
                tank_id = None
            else:
                if (not tank_id.isdigit()):
                    tank_id_fault = "Please write a positive integer for Tank ID"
                    error_occured = True
                else:
                    if (not error_occured):
                        all_tank_ids_gs_coords = Tank.allTankIdsGsCoords(
                            gs_longitude, gs_latitude)
                        tank_id = int(tank_id)
                        check_tank_id = (tank_id, )
                        if ((check_tank_id in all_tank_ids_gs_coords) and ("add_purchase" in request.POST)):
                            tank_id_fault = "Please write an existing tank id with the corresponding gas station coordinates"
                            error_occured = True

        if (pump_id != False):
            pump_id = pump_id.strip()
            if (pump_id == ''):
                pump_id = None
            else:
                if (not pump_id.isdigit()):
                    pump_id_fault = "Please write a positive integer for Pump ID"
                    error_occured = True
                else:
                    if (not error_occured):
                        all_pump_ids_tank_gs_coords = Pump.allPumpIdsTankGsCoords(
                            tank_id, gs_longitude, gs_latitude)
                        pump_id = int(pump_id)
                        check_pump_id = (pump_id, )
                        if ((check_pump_id in all_pump_ids_tank_gs_coords) and ("add_purchase" in request.POST)):
                            pump_id_fault = "Please write an existing pump id with the corresponding tank id and gas station coordinates"
                            error_occured = True

        if (not error_occured):
            if "add_purchase" in request.POST:
                try:
                    Purchase.insertInto(int(id), purchase_date, type_of_payment, customer_email,
                                        float(gs_longitude), float(gs_latitude), pump_id, tank_id)
                    return redirect(purchase)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_purchase" in request.POST:
                try:
                    purchases = Purchase.searchBy(int(id), purchase_date, type_of_payment, customer_email,
                                                  float(gs_longitude), float(gs_latitude), pump_id, tank_id)
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Purchase.update(int(id), purchase_date, type_of_payment, customer_email,
                                    float(gs_longitude), float(gs_latitude), pump_id, tank_id)
                    return redirect(purchase)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            purchases = Purchase.retrieveAllColumns()
    else:
        purchases = Purchase.retrieveAllColumns()
    all_purchases = Purchase.retrieveAllColumns()
    return render(request, 'purchase.html', {'purchases': purchases, 'number_of_purchases': len(all_purchases),  'id_fault': id_fault, 'purchase_date_fault': purchase_date_fault, 'type_of_payment_fault': type_of_payment_fault, 'customer_email_fault': customer_email_fault, 'gs_longitude_fault': gs_longitude_fault, 'gs_latitude_fault': gs_latitude_fault, 'pump_id_fault': pump_id_fault, 'tank_id_fault': tank_id_fault})


def purchase_delete(request, id):
    Purchase.delete(id)
    return redirect(purchase)


def service(request):
    id_fault = False
    name_fault = False
    price_fault = False
    corresponding_points_fault = False

    if request.method == "POST":
        id = request.POST.get('id', False)
        name = request.POST.get('name', False)
        price = request.POST.get('price', False)
        corresponding_points = request.POST.get('corresponding-points', False)

        error_occured = False

        if (id != False):
            id = id.strip()
            if (not id.isdigit()):
                id_fault = "Please write a positive integer for id"
                error_occured = True
            else:
                all_services = Service.allServiceIds()
                id = int(id)
                check_service = (id, )
                if (id < 0):
                    id_fault = "Please write a positive integer for id"
                    error_occured = True
                if (check_service in all_services and "add_service" in request.POST):
                    id_fault = "Please write a positive integer for id. Service id already exists"
                    error_occured = True

        if (name != False):
            name = name.strip()
            if (not name.isalpha()):
                name_fault = "Please write a valid first name"
                error_occured = True
            else:
                name = name.capitalize()

        if (price != False):
            price = price.strip()
            if (not price.replace('.', '', 1).isdigit()):
                price_fault = "Please write a float number between 0 and 10000 with 2 decimal places for price"
                error_occured = True
            else:
                price = float(price)
                if (price > 9999.99 or price < 0):
                    price_fault = "Please write a float number between 0 and 10000 with 2 decimal places for price"
                    error_occured = True
                else:
                    numbers = str(price).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 2):
                        price_fault = "Please write a float number between 0 and 10000 with 2 decimal places for price"
                        error_occured = True

        if (corresponding_points != False):
            corresponding_points = corresponding_points.strip()
            if (not corresponding_points.isdigit()):
                corresponding_points_fault = "Please write a integer between 0 and 990 for Corresponding Points"
                error_occured = True
            else:
                corresponding_points = int(corresponding_points)
                if (corresponding_points > 990 or corresponding_points < 0):
                    corresponding_points_fault = "Please write a integer between 0 and 990 for Corresponding Points"
                    error_occured = True

        if (not error_occured):
            if "add_service" in request.POST:
                try:
                    Service.insertInto(
                        id, name, price, int(corresponding_points))
                    return redirect(service)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_service" in request.POST:
                try:
                    services = Service.searchBy(
                        int(id), float(price), int(corresponding_points))
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Service.update(int(id), name, float(
                        price), int(corresponding_points))
                    return redirect(service)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            services = Service.retrieveAllColumns()
    else:
        services = Service.retrieveAllColumns()
    all_services = Service.retrieveAllColumns()
    return render(request, 'service.html', {'services': services, 'number_of_services': len(all_services), 'id_fault': id_fault, 'name_fault': name_fault, 'price_fault': price_fault, 'corresponding_points_fault': corresponding_points_fault})


def service_delete(request, id):
    Service.delete(id)
    return redirect(service)


def sign(request):
    essn_fault = False
    contract_id_fault = False

    if request.method == "POST":
        essn = request.POST.get('essn', False)
        contract_id = request.POST.get('contract-id', False)
        previous_contract_id = request.POST.get('previous-contract-id', False)

        error_occured = False

        if (essn != False):
            essn = essn.strip()
            essn_check = ''.join(essn.split('-'))
            all_ssn = Employee.allSsn()
            if (not essn_check.isdigit() or len(essn_check) != 9):
                essn_fault = "Please write a valid ssn with 9 digits with this format 'xxx-xx-xxxx'"
                error_occured = True
            elif (essn not in all_ssn):
                essn_fault = "Please write a valid ssn. This employee does not exist"
                error_occured = True

        if (contract_id != False):
            contract_id = contract_id.strip()
            all_contract_id = Contract.allContracts()
            if (not contract_id.isdigit()):
                contract_id_fault = "Please write a positive integer for Contact ID"
                error_occured = True
            elif (contract_id not in all_contract_id and "search_contract" not in request.POST):
                contract_id_fault = "Please write a contract id. Contract id does not exist"
                error_occured = True
            else:
                contract_id = int(contract_id)

        if (not error_occured):
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
                    Signs.update(essn, int(contract_id),
                                 int(previous_contract_id))
                    return redirect(sign)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            signs = Signs.retrieveAllColumns()
    else:
        signs = Signs.retrieveAllColumns()
    return render(request, 'signs.html', {'signs': signs, 'essn_fault': essn_fault, 'contract_id_fault': contract_id_fault})


def sign_delete(request, essn_contract):
    Signs.delete(essn_contract)
    return redirect(sign)


def supplier(request):
    email_fault = False
    first_name_fault = False
    last_name_fault = False
    phone_number_fault = False
    longitude_fault = False
    latitude_fault = False

    if request.method == "POST":
        email = request.POST.get('email', False)
        first_name = request.POST.get('first-name', False)
        last_name = request.POST.get('last-name', False)
        phone_number = request.POST.get('phone-number', False)
        longitude = request.POST.get('longitude', False)
        latitude = request.POST.get('latitude', False)

        error_occured = False

        if (first_name != False):
            first_name = first_name.strip()
            if (not first_name.isalpha()):
                first_name_fault = "Please write a valid first name"
                error_occured = True
            else:
                first_name = first_name.capitalize()

        if (email != False):
            email = email.strip()
            try:
                validation = validate_email(email)
                email = validation.email
                # check if the email belongs to another supplier
                if (not error_occured):
                    all_supplier_emails = Supplier.allSupplierEmails()
                    check_supplier_emails = (email, )
                    all_supplier_names = Supplier.allSupplierNames()
                    first_name = first_name.strip()
                    check_supplier_names = (first_name, )
                    if ((check_supplier_emails in all_supplier_emails) and (check_supplier_names not in all_supplier_names) and ("add_supplier" in request.POST)):
                        email_fault = "Please write a valid email. This email belongs to another supplier"
                    error_occured = True
            except EmailNotValidError as e:
                email_fault = str(e)
                error_occured = True

        if (last_name != False):
            last_name = last_name.strip()
            if (not last_name.isalpha()):
                last_name_fault = "Please write a valid last name"
                error_occured = True
            else:
                last_name = last_name.capitalize()

        if (phone_number != False):
            phone_number = phone_number.strip()
            if (not phone_number.isdigit()):
                phone_number_fault = "Please write a integer between 6900000000 and 6999999999 for Phone Number"
                error_occured = True
            else:
                all_phone_numbers = Supplier.allPhoneNumbers()
                phone_number = int(phone_number)
                check_phone_number = (phone_number, )
                if (check_phone_number in all_phone_numbers and "add_supplier" in request.POST):
                    phone_number_fault = "Please write a positive integer for Phone Number. Phone Number already exists"
                    error_occured = True
                if (phone_number > 6999999999 or phone_number < 6900000000):
                    phone_number_fault = "Please write a integer between 6900000000 and 6999999999 for Phone Number"
                    error_occured = True

        if (longitude != False):
            longitude = longitude.strip()
            if (not longitude.replace('.', '', 1).isdigit()):
                longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                error_occured = True
            else:
                longitude = float(longitude)
                if (longitude > 99.999999 or longitude < 0):
                    longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                    error_occured = True
                else:
                    numbers = str(longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for Longitude"
                        error_occured = True

        if (latitude != False):
            latitude = latitude.strip()
            if (not latitude.replace('.', '', 1).isdigit()):
                latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                error_occured = True
            else:
                latitude = float(latitude)
                if (latitude > 999.999999 or latitude < 0):
                    latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                    error_occured = True
                else:
                    numbers = str(latitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for Latitude"
                        error_occured = True

        if (not error_occured):
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
    else:
        suppliers = Supplier.retrieveAllColumns()
    return render(request, 'supplier.html', {'suppliers': suppliers, 'email_fault': email_fault, 'first_name_fault': first_name_fault, 'last_name_fault': last_name_fault, 'phone_number_fault': phone_number_fault, 'longitude_fault': longitude_fault, 'latitude_fault': latitude_fault})


def supplier_delete(request, email):
    Supplier.delete(email)
    return redirect(supplier)


def supply(request):
    id_fault = False
    expected_arrival_date_fault = False
    real_arrival_date_fault = False
    sup_email_fault = False
    gs_longitude_fault = False
    gs_latitude_fault = False

    if request.method == "POST":
        id = request.POST.get('id', False)
        expected_arrival_date = request.POST.get(
            'expected-arrival-date', False)
        real_arrival_date = request.POST.get('real-arrival-date', False)
        sup_email = request.POST.get('sup-email', False)
        gs_longitude = request.POST.get('gs-longitude', False)
        gs_latitude = request.POST.get('gs-latitude', False)

        error_occured = False

        if (id != False):
            id = id.strip()
            if (not id.isdigit()):
                id_fault = "Please write a positive integer for id"
                error_occured = True
            else:
                all_supplies = Supply.allSupplyIds()
                id = int(id)
                check_supply = (id, )
                if (id < 0):
                    id_fault = "Please write a positive integer for id"
                    error_occured = True
                # check if supply id already exists when trying to add new supply
                if (check_supply in all_supplies and "add_supply" in request.POST):
                    id_fault = "Please write a valid id. Supply id already exists"
                    error_occured = True

        if (sup_email != False):
            sup_email = sup_email.strip()
            try:
                validation = validate_email(sup_email)
                sup_email = validation.sup_email
            except EmailNotValidError as e:
                sup_email_fault = str(e)
                error_occured = True

        if (expected_arrival_date != False):
            expected_arrival_date = expected_arrival_date.strip()
            expected_arrival_date = expected_arrival_date.split('-')
            expected_arrival_date = '/'.join(expected_arrival_date[::-1])
            if (not expected_arrival_date.replace('/', '', 2).isdigit()):
                expected_arrival_date_fault = "Please write a valid Expected Arrival Date"
                error_occured = True

        if (real_arrival_date != False):
            real_arrival_date = real_arrival_date.strip()
            real_arrival_date = real_arrival_date.split('-')
            real_arrival_date = '/'.join(real_arrival_date[::-1])
            if (not real_arrival_date.replace('/', '', 2).isdigit()):
                real_arrival_date_fault = "Please write a valid Real Arrival Date"
                error_occured = True
            elif (expected_arrival_date != False):
                ead_date = expected_arrival_date.split('/')
                ead_date = datetime(int(ead_date[2]), int(
                    ead_date[1]), int(ead_date[0]))

                rad_date = real_arrival_date.split('/')
                rad_date = datetime(int(rad_date[2]), int(
                    rad_date[1]), int(rad_date[0]))

                if (ead_date.date() > rad_date.date()):
                    real_arrival_date_fault = "Real Arrival Date should be greater than or equal to Expected Arrival Date"
                    error_occured = True

        if (gs_longitude != False):
            gs_longitude = gs_longitude.strip()
            if (not gs_longitude.replace('.', '', 1).isdigit()):
                gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                error_occured = True
            else:
                gs_longitude = float(gs_longitude)
                if (gs_longitude > 99.999999 or gs_longitude < 0):
                    gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                    error_occured = True
                else:
                    numbers = str(gs_longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                        error_occured = True

        if (gs_latitude != False):
            gs_latitude = gs_latitude.strip()
            if (not gs_latitude.replace('.', '', 1).isdigit()):
                gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                error_occured = True
            else:
                gs_latitude = float(gs_latitude)
                if (gs_latitude > 999.999999 or gs_latitude < 0):
                    gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                    error_occured = True
                else:
                    numbers = str(gs_latitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                        error_occured = True

        if (not error_occured):
            if "add_supply" in request.POST:
                try:
                    Supply.insertInto(int(id), expected_arrival_date,
                                      real_arrival_date, sup_email, gs_longitude, gs_latitude)
                    return redirect(supply)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_supply" in request.POST:
                try:
                    supplies = Supply.searchBy(int(
                        id), expected_arrival_date, real_arrival_date, sup_email, gs_longitude, gs_latitude)
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Supply.update(int(id), expected_arrival_date,
                                  real_arrival_date, sup_email, gs_longitude, gs_latitude)
                    return redirect(supply)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            supplies = Supply.retrieveAllColumns()
    else:
        supplies = Supply.retrieveAllColumns()
    all_supplies = Supply.retrieveAllColumns()
    return render(request, 'supply.html', {'supplies': supplies, 'number_of_supplies': len(all_supplies), 'id_fault': id_fault, 'expected_arrival_date_fault': expected_arrival_date_fault, 'real_arrival_date_fault': real_arrival_date_fault, 'sup_email_fault': sup_email_fault, 'gs_longitude_fault': gs_longitude_fault, 'gs_latitude_fault': gs_latitude_fault})


def supply_delete(request, id):
    Supply.delete(id)
    return redirect(supply)


def tank(request):
    id_fault = False
    last_check_up_fault = False
    capacity_fault = False
    quantity_fault = False
    prod_id_fault = False
    gs_longitude_fault = False
    gs_latitude_fault = False

    if request.method == "POST":
        id = request.POST.get('id', False)
        last_check_up = request.POST.get('last-check-up', False)
        capacity = request.POST.get('capacity', False)
        quantity = request.POST.get('quantity', False)
        prod_id = request.POST.get('prod-id', False)
        gs_longitude = request.POST.get('gs-longitude', False)
        gs_latitude = request.POST.get('gs-latitude', False)

        error_occured = False

        if (id != False):
            id = id.strip()
            if (not id.isdigit()):
                id_fault = "Please write a positive integer for id"
                error_occured = True
            else:
                all_tanks = Tank.allTankIds()
                id = int(id)
                check_tank = (id, )
                if (id < 0):
                    id_fault = "Please write a positive integer for id"
                    error_occured = True
                # check if tank id already exists when trying to add new tank
                if (check_tank in all_tanks and "add_tank" in request.POST):
                    id_fault = "Please write a valid id. Tank id already exists"
                    error_occured = True

        if (gs_longitude != False):
            gs_longitude = gs_longitude.strip()
            if (not gs_longitude.replace('.', '', 1).isdigit()):
                gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                error_occured = True
            else:
                gs_longitude = float(gs_longitude)
                if (gs_longitude > 99.999999 or gs_longitude < 0):
                    gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                    error_occured = True
                else:
                    numbers = str(gs_longitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        gs_longitude_fault = "Please write a float number between 00.000000 and 99.999999 with 6 decimal places for GS Longitude"
                        error_occured = True

        if (gs_latitude != False):
            gs_latitude = gs_latitude.strip()
            if (not gs_latitude.replace('.', '', 1).isdigit()):
                gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                error_occured = True
            else:
                gs_latitude = float(gs_latitude)
                if (gs_latitude > 999.999999 or gs_latitude < 0):
                    gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                    error_occured = True
                else:
                    numbers = str(gs_latitude).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 6):
                        gs_latitude_fault = "Please write a float number between 000.000000 and 999.999999 with 6 decimal places for GS Latitude"
                        error_occured = True

        if (last_check_up != False):
            last_check_up = last_check_up.strip()
            last_check_up = last_check_up.split('-')
            last_check_up = '/'.join(last_check_up[::-1])
            if (not last_check_up.replace('/', '', 2).isdigit()):
                last_check_up_fault = "Please write a valid Start Date"
                error_occured = True
            lcu_date = last_check_up.split('/')
            lcu_date = datetime(int(lcu_date[2]), int(
                lcu_date[1]), int(lcu_date[0]))

            if (lcu_date.date() > datetime.today().date()):
                end_date_fault = "Start Date should be lesser than today"
                error_occured = True

        if (capacity != False):
            capacity = capacity.strip()
            if (not capacity.replace('.', '', 1).isdigit()):
                capacity_fault = "The capacity is 15000.000 for all the tanks in the Gas Station"
                error_occured = True
            else:
                capacity = float(capacity)
                if (capacity != 15000):
                    capacity_fault = "The capacity is 15000.000 for all the tanks in the Gas Station"
                    error_occured = True
                else:
                    numbers = str(capacity).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 3):
                        capacity_fault = "The capacity is 15000.000 for all the tanks in the Gas Station"
                        error_occured = True

        if (quantity != False):
            quantity = quantity.strip()
            if (not quantity.replace('.', '', 1).isdigit()):
                quantity_fault = "Please write a float number between 0 and 15000 (Tank Capacity) with 3 decimal places for quantity"
                error_occured = True
            else:
                quantity = float(quantity)
                if (quantity > 15000 or quantity < 0):
                    quantity_fault = "Please write a float number between 0 and 15000 (Tank Capacity) with 3 decimal places for quantity"
                    error_occured = True
                else:
                    numbers = str(quantity).split('.')
                    decimal_part = numbers[1]
                    if (len(decimal_part) > 3):
                        quantity_fault = "Please write a float number between 0 and 15000 (Tank Capacity) with 3 decimal places for quantity"
                        error_occured = True

        if (prod_id != False):
            prod_id = prod_id.strip()
            if (not prod_id.isdigit()):
                prod_id_fault = "Please write a positive integer for Product ID"
                error_occured = True
            else:
                prod_id = int(prod_id)

        if (not error_occured):
            if "add_tank" in request.POST:
                try:
                    Tank.insertInto(int(id), last_check_up, float(capacity), float(
                        quantity), int(prod_id), float(gs_longitude), float(gs_latitude))
                    return redirect(tank)
                except Exception as e:
                    print("View exception")
                    print(e)
            elif "search_tank" in request.POST:
                try:
                    tanks = Tank.searchBy(int(id), last_check_up, float(capacity), float(
                        quantity), int(prod_id), float(gs_longitude), float(gs_latitude))
                except Exception as e:
                    print("View exception")
                    print(e)
            else:
                try:
                    Tank.update(int(id), last_check_up, float(capacity), float(
                        quantity), int(prod_id), float(gs_longitude), float(gs_latitude))
                    return redirect(tank)
                except Exception as e:
                    print("View exception")
                    print(e)
        else:
            tanks = Tank.retrieveAllColumns()
    else:
        tanks = Tank.retrieveAllColumns()
    all_tanks = Tank.retrieveAllColumns()
    return render(request, 'tank.html', {'tanks': tanks, 'number_of_tanks': len(all_tanks), 'id_fault': id_fault, 'last_check_up_fault': last_check_up_fault, 'capacity_fault': capacity_fault, 'quantity_fault': quantity_fault, 'prod_id_fault': prod_id_fault, 'gs_longitude_fault': gs_longitude_fault, 'gs_latitude_fault': gs_latitude_fault})


def tank_delete(request, id_longitude_latitude):
    Tank.delete(id_longitude_latitude)
    return redirect(tank)


if __name__ == 'Database_Management.views':
    Contract.createContractTable()
    Customer.createCustomerTable()
    Supplier.createSupplierTable()
    Product.createProductTable()
    Service.createServiceTable()

    GasStation.createGasStationTable()
    Employee.createEmployeeTable()

    Tank.createTankTable()
    Pump.createPumpTable()

    Signs.createSignsTable()
    Supply.createSupplyTable()

    Purchase.createPurchaseTable()
    Involves.createInvolvesTable()
    Entails.createEntailsTable()

    ConsistsOf.createConsistsOfTable()
    IsAssignedTo.createIsAssignedToTable()
    Offers.createOffersTable()
    Provides.createProvidesTable()
