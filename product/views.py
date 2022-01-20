from http.client import HTTPResponse
from django.shortcuts import render

from .models import product
from supplier.models import suppliers, supplier_phone


def create_product_form(request):
    # create item and set it by ""
    product_id = ""
    product_name = ""
    product_price = ""
    product_type = ""
    product_quantityInMarket = ""
    product_quantityInStore = ""
    product_importPrice = ""
    product_unity = ""
    product_PackagePecies = ""
    product_supplier = ""
    status_id = "text"
    status_quantity = "hidden"
    Query = "insert"
    context = {
        "product_id": product_id,
        "product_name": product_name,
        "product_price": product_price,
        "product_type": product_type,
        "product_quantityInMarket": product_quantityInMarket,
        "product_quantityInStore": product_quantityInStore,
        "product_importPrice": product_importPrice,
        "product_unity": product_unity,
        "product_PackagePecies": product_PackagePecies,
        "product_supplier": product_supplier,
        "status_id": status_id,
        "status_quantity": status_quantity,
        "Query": Query,
    }
    return render(request, "create_update_product.html", context)


def insert_update_product(request):
    try:
        process_type = request.POST.get("submit")
        required = []
        supplier_exist = True
        product_exist = False
        for key in request.POST:
            value = request.POST.get(key)
            if not value and value != 0:
                required.append(value)
        if len(required) == 0:
            product_class = product()
            supplier_class = suppliers()
            product_class._id = request.POST.get("product_id")
            product_class.p_name = request.POST.get("product_name")
            product_class.price = request.POST.get("product_price")
            product_class.p_type = request.POST.get("product_type")
            product_class.quantityInMarket = request.POST.get(
                "product_quantityInMarket"
            )
            product_class.quantityInStore = request.POST.get("product_quantityInStore")
            product_class.importPrice = request.POST.get("product_importPrice")
            product_class.unity = request.POST.get("product_unity")
            product_class.PackagePecies = request.POST.get("product_PackagePecies")
            product_class.supplier = request.POST.get("product_supplier")
            supplier_class.supplier_id = product_class.supplier
            supplier_information = supplier_class.get_supplier_info()
            if len(supplier_information) == 1:
                if process_type == "insert":
                    if len(product_class.get_product_info()) > 0:
                        product_exist = True
                    else:
                        product_class.insert_into_product()
                else:
                    product_class.update_product()
            else:
                supplier_exist = False

        context = {
            "required": required,
            "required_statues": len(required),
            "supplier_exist": supplier_exist,
            "product_exist": product_exist,
            "process_type": process_type,
            "product_id": product_class._id,
        }
        return render(request, "massage_product.html", context)
    except:
        context = {
            "error": "Back To Home",
        }
        return render(request, "massage_product.html", context)


def show_all_product(request):
    product_class = product()
    products_information = product_class.get_products_info()
    context = {
        "products_information": products_information,
    }
    return render(request, "get_all_products.html", context)


def show_One_product(request):
    try:
        product_id = request.GET.get("id")
        product_class = product()
        supplier_class = suppliers()
        supplier_phone_class = supplier_phone()
        product_class._id = product_id
        product_information = product_class.get_product_info()
        supplier_id = product_information[0][9]
        supplier_class.supplier_id = supplier_phone_class._id = supplier_id
        suppliers_information = supplier_class.get_supplier_info()
        supplier_phone_information = supplier_phone_class.get_supplier_phones()
        context = {
            "product": product_information[0],
            "supplier": suppliers_information[0],
            "phone_value": supplier_phone_information,
        }
        return render(request, "get_One_product.html", context)
    except:
        context = {
            "error": "Back To Home",
        }
        return render(request, "massage_product.html", context)


def operation_product(request):
    try:
        status = request.POST.get("submit")
        product_id = request.POST.get("id")
        product_class = product()
        product_class._id = product_id
        if status == "update":
            row = product_class.get_product_info()
            product_name = row[0][1]
            product_price = row[0][2]
            product_type = row[0][3]
            product_quantityInMarket = row[0][4]
            product_quantityInStore = row[0][5]
            product_importPrice = row[0][6]
            product_unity = row[0][7]
            product_PackagePecies = row[0][8]
            product_supplier = row[0][9]
            status_id = "hidden"
            status_quantity = "number"
            Query = "update"
            context = {
                "product_id": product_id,
                "product_name": product_name,
                "product_price": product_price,
                "product_type": product_type,
                "product_quantityInMarket": product_quantityInMarket,
                "product_quantityInStore": product_quantityInStore,
                "product_importPrice": product_importPrice,
                "product_unity": product_unity,
                "product_PackagePecies": product_PackagePecies,
                "product_supplier": product_supplier,
                "status_id": status_id,
                "status_quantity": status_quantity,
                "Query": Query,
            }
            return render(request, "create_update_product.html", context)
        elif status == "delete":
            product_class.delete_product()
            return show_all_product(request)
    except:
        context = {
            "error": "Back To Home",
        }
        return render(request, "massage_product.html", context)
