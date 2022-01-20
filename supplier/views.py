from django.shortcuts import render
from .models import suppliers, supplier_phone


def create_supplier_form(request):
    s_id = ""
    status = "text"
    Query = "insert"
    supplier_name = ""
    supplier_email = ""
    supplier_phones = ["", "", ""]
    context = {
        "supplier_id": s_id,
        "supplier_name": supplier_name,
        "supplier_email": supplier_email,
        "supplier_phones": supplier_phones,
        "status": status,
        "Query": Query,
        "range": range(0),
    }
    return render(request, "create_update_supplier.html", context)


def insert_update_supplier(request):
    try:
        process_type = request.POST.get("submit")
        s_name = request.POST.get("supplier_name") or 0
        s_email = request.POST.get("supplier_email") or 0
        s_id = request.POST.get("supllier_id") or 0
        id_exist = False
        phone_list = request.POST.getlist("supplier_phone")
        required = []
        s_phone = []
        for value in request.POST.getlist("supplier_phone"):
            if not value:
                continue
            else:
                s_phone.append(value)
        if s_name and s_email and s_id and s_phone:
            supplier_object = suppliers()
            supplier_phone_object = supplier_phone()
            supplier_phone_array = []
            supplier_phone_object._id = supplier_object.supplier_id = s_id
            supplier_object.s_name = s_name
            supplier_object.s_email = s_email
            required.append("FALSE")
            for i in range(len(phone_list)):
                phone_object = supplier_phone()
                phone_object._id = s_id
                phone_object.phone = phone_list[i]
                supplier_phone_array.append(phone_object)

            if process_type == "insert":
                supplier_info = supplier_object.get_supplier_info()
                if supplier_info:
                    id_exist = True
                else:
                    supplier_object.insert_into_supplier()
                    for index in range(len(supplier_phone_array)):
                        if not supplier_phone_array[index].phone:
                            continue
                        supplier_phone_array[index].insert_into_supplier_phone()
            else:
                supplier_object.update_supplier()
                supplier_old_phones = supplier_phone_object.get_supplier_phones()
                index = 0
                for value in supplier_old_phones:
                    if index >= len(supplier_phone_array):
                        break
                    if not supplier_phone_array[index].phone:
                        supplier_phone_array[index].delete_phone(value[1])
                    else:
                        supplier_phone_array[index].update_supplier_phone(value[1])
                    index += 1
                while index < len(supplier_phone_array):
                    if supplier_phone_array[index].phone:
                        supplier_phone_array[index].insert_into_supplier_phone()
                    index += 1
        else:
            if s_name == 0:
                required.append("Name")
            if s_email == 0:
                required.append("Email")
            if s_id == 0:
                required.append("ID")
            if len(s_phone):
                required.append("you can't enter less than one phone number")

        context = {
            "process_type": process_type,
            "required": required,
            "id_exist": id_exist,
            "s_id": s_id,
        }
        return render(request, "massage.html", context)
    except:
        context = {
            "error": "Back To Home",
        }
        return render(request, "massage.html", context)


def show_all_supplier(request):
    suppliers_object = suppliers()
    suppliers_information = suppliers_object.get_suppliers_info()
    context = {
        "suppliers_information": suppliers_information,
    }
    return render(request, "get_all_suppliers.html", context)


def show_One_supplier(request):
    try:
        s_id = request.GET.get("id")
        suppliers_object = suppliers()
        supplier_phone_object = supplier_phone()
        suppliers_object.supplier_id = s_id
        supplier_phone_object._id = s_id
        suppliers_information = suppliers_object.get_supplier_info()
        supplier_phone_information = supplier_phone_object.get_supplier_phones()
        context = {
            "value": suppliers_information[0],
            "phone_value": supplier_phone_information,
        }
        return render(request, "get_One_supplier.html", context)
    except:
        context = {
            "error": "Back To Home",
        }
        return render(request, "massage.html", context)


def operation_supplier(request):
    try:
        status = request.POST.get("submit")
        s_id = request.POST.get("id")
        supplier_class = suppliers()
        supplier_phone_class = supplier_phone()
        supplier_phone_class._id = supplier_class.supplier_id = s_id
        if status == "update":
            row = supplier_class.get_supplier_info()
            status = "hidden"
            Query = "update"
            supplier_name = row[0][1]
            supplier_email = row[0][2]
            supplier_phones = supplier_phone_class.get_supplier_phones()
            context = {
                "supplier_id": s_id,
                "supplier_name": supplier_name,
                "supplier_email": supplier_email,
                "supplier_phones": supplier_phones,
                "status": status,
                "Query": Query,
                "range": range(len(supplier_phones), 3),
            }
            return render(request, "create_update_supplier.html", context)
        elif status == "delete":
            supplier_phone_class.delete_supplier_phones()
            supplier_class.delete_supplier()
            return show_all_supplier(request)
    except:
        context = {
            "error": "Back To Home",
        }
        return render(request, "massage.html", context)
