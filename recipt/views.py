from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse

from .sale_functions import *
from .purchase_functions import *
from .models import recipt, total_price_recipt


def delete_all_empty_recipt():
    total_price_recipt_class = total_price_recipt()
    rows = total_price_recipt_class.get_empty_recipt()
    for value in rows:
        c = connection.cursor()
        c.execute("CALL delete_all_recipt('" + value[0] + "');")


def create_recipt(request):
    try:
        delete_all_empty_recipt()
        status = request.GET.get("status")
        total_price_recipt_class = total_price_recipt()
        recipt_class = recipt()
        last_recipt_id = recipt.get_all()
        new_recipt_id = len(last_recipt_id) + 19000
        total_price_recipt_class._id = new_recipt_id
        recipt_class._id = new_recipt_id
        total_price_recipt_class.r_Type = status
        recipt_class.create_recipt()
        total_price_recipt_class.create_recipt()
        request.session["recipt_id"] = new_recipt_id
        request.session["supplier_products"] = {}
        request.session["item"] = {}
        request.session["total_price"] = 0
        request.session['total_profit']= 0
        request.session["supplier_id"] = ''
        if status == "sale":
            context = {
                "item" :request.session["item"],
                "total_price" : request.session['total_price']
            }
            return render(request,"create_sale_recipt.html",context)
        else:
            context = {
                "supplier_products" :request.session["supplier_products"], 
                "table_items" :request.session["item"], 
                "total_price" :request.session["total_price"], 
                "supplier_id" :request.session["supplier_id"], 
            }
            return render(request,"create_purchase_recipt.html",context)
    except:
        return HttpResponse(status)


def chose_purchase_operation(request):
  try:
        status = request.POST.get("submit")
        get_remove = request.GET.get("remove")
        supplier_id = request.session['supplier_id']
        if get_remove :
            return remove_purchase_item(request)
        if status == "go":
            return get_supplier_products(request)
        elif status == "add_item":
            return add_purchase_item(request)
        elif status == "add_recipt":
            return add_purchase_recipt(request)
        else:
            context = {
                "supplier_products" :request.session["supplier_products"][supplier_id], 
                "table_items" :request.session["item"], 
                "total_price" :request.session["total_price"], 
                "supplier_id" :request.session["supplier_id"],
            }
            return render(request,"create_purchase_recipt.html",context)
  except:
        return HttpResponse("ERROR")



def chose_sale_operation(request):
    try:
        status = request.POST.get("submit")
        get_remove = request.GET.get("remove")
        items = request.session["item"]
        total_price = request.session["total_price"]
        if get_remove :
            return remove_sale_item(request)
        elif status == "add_item":
            return add_sale_item(request)
        elif status == "add_recipt":
            return add_sale_recipt(request)
        else:
            context = {
                "table_items":items,
                "total_price":total_price,
            }
            return render(request,"create_sale_recipt.html",context)
    except:
        return HttpResponse("ERROR")



def get_all_recipt(request):
    delete_all_empty_recipt()
    status = request.GET.get("status")
    recipt_price_class = total_price_recipt()
    recipt_class = recipt()
    recipt_price = recipt_price_class.get_all_recipt(status)
    recipt_date = recipt_class.get_all_by_type(status)
    all_recipt = zip(recipt_price,recipt_date)
    context = {   
        "recipt": all_recipt,
        "status":status,
    }
    return render(request, "get_all_recipt.html", context)


def get_one_recipt(request):
    recipt_id = request.GET.get('id')
    recipt_price_class = total_price_recipt()
    recipt_class = recipt()
    recipt_product_class = product_recipt()
    recipt_class._id = recipt_price_class._id = recipt_product_class.recipt_id = recipt_id
    recipt_date_info = recipt_class.get_one()
    recipt_price_info = recipt_price_class.get_one()
    recipt_product_info = recipt_product_class.get_one_recipt_product()
    product_main_info = []
    for value in recipt_product_info:
        product_info = product()
        product_info._id = value[0]
        row = product_info.get_product_name_supplier_unity()
        row = row[0]
        row = row + (value[2],value[3],round(value[2]*value[3],2),)
        product_main_info.append(row)
        print(product_main_info)
    context = {
        "recipt_id":recipt_id,
        "recipt_date":recipt_date_info[0][1],
        "status":recipt_price_info[0][3],
        "product":product_main_info,
        "total_price":recipt_price_info[0][2],
        "total_profit":recipt_price_info[0][1],
    }
    return render(request,"get_One_recipt.html",context)










    
