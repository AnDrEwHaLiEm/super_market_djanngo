from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import product_recipt, recipt, total_price_recipt
from product.models import product


def add_purchase_recipt(request):
    product_items = request.session['item']
    total_price = request.session['total_price']
    recipt_id = request.session['recipt_id']
    for key in product_items:
        sale_quantity = float(product_items[key]['quantity'])
        product_class = product()
        product_class._id = key
        product_class.update_product_quantity(sale_quantity)


    total_price_class = total_price_recipt()
    total_price_class._id = recipt_id
    total_price_class.total_price = total_price
    total_price_class.total_profits = 0
    total_price_class.update_recipt()

    return HttpResponseRedirect("http://127.0.0.1:8000/recipt/create_recipt?status=purchase")


def remove_purchase_item(request):
    product_id = request.GET.get('remove')
    items = request.session['item']
    total_price = request.session['total_price']
    recipt_id = request.session['recipt_id']

    product_recipt_class = product_recipt()
    product_recipt_class.product_id = product_id
    product_recipt_class.recipt_id = recipt_id
    product_recipt_class.delete_product_recipt()

    total_price = round(total_price-items[product_id]['total_price'],2)

    items.pop(product_id,False)
    request.session['total_price'] = total_price
    request.session['item'] = items
    return HttpResponseRedirect("main_purchase_recipt_page")


def get_supplier_products(request):
    request.session["supplier_id"] =  request.POST['supplier_id']
    supplier_id = request.session["supplier_id"]
    supplier_products = request.session["supplier_products"]
    if supplier_id in supplier_products :      
        context = {
            "supplier_products" :supplier_products[supplier_id], 
            "table_items" :request.session["item"], 
            "total_price" :request.session["total_price"], 
            "supplier_id" :supplier_id, 
        }
        return render(request,"create_purchase_recipt.html",context)
    else : 
        product_class = product()
        product_class.supplier = supplier_id
        product_items = product_class.get_product_info_by_supplier()
        if len(product_items):
            request.session["supplier_products"][supplier_id] = {}
            supplier_products = request.session["supplier_products"][supplier_id]
            for value in product_items : 
                supplier_products[value[0]] = {}                    
                supplier_products[value[0]]['p_name'] = value[1]                    
                supplier_products[value[0]]['unity'] = value[3]                    
                supplier_products[value[0]]['importPrice'] = value[2]
                supplier_products[value[0]]['supplier_id'] = supplier_id
            
            request.session["supplier_products"][supplier_id] = supplier_products
            context = {
                "supplier_products" :supplier_products, 
                "table_items" :request.session["item"], 
                "total_price" :request.session["total_price"], 
                "supplier_id" :supplier_id, 
            }
            return render(request,"create_purchase_recipt.html",context)                                          
        else :
            context = {
                "supplier_products" :{}, 
                "table_items" :request.session["item"], 
                "total_price" :request.session["total_price"], 
                "supplier_id" :'', 
                "Error" : "supplier Not exist or not supply any exist product",
            }
            return render(request,"create_purchase_recipt.html",context)   



def add_purchase_item(request):
    quantity = request.POST["product_quantity"]
    product_id = request.POST["product_id"]
    recipt_id = request.session['recipt_id']
    supplier_id = request.session['supplier_id']
    items = request.session['item']
    total_price = request.session['total_price']
    supplier_products = request.session["supplier_products"][supplier_id]
    product_info = supplier_products[product_id]
    error = ""
    item = {}
    recipt_product_class =  product_recipt()
    recipt_product_class.product_id = product_id
    recipt_product_class.recipt_id = recipt_id
    recipt_product_class.quantity = quantity
    if len(product_id)  and len(quantity):
        if product_id in items:
            item = request.session['item'][product_id]
            total_price = round(total_price-item['total_price'],2)
            item['quantity'] = quantity
            item['total_price'] = round(float(quantity) * product_info['importPrice'],2)
            recipt_product_class.update_quantity()
        else :
            recipt_product_class.price = product_info["importPrice"]
            recipt_product_class.insert_product_recipt()       
            request.session['item'][product_id] = {}
            item = request.session['item'][product_id]
            item["id"] = product_id
            item["supplier_id"] = supplier_id
            item["p_name"] = product_info['p_name']
            item["import_price"] = product_info["importPrice"]
            item["unity"] = product_info['unity']
            item["quantity"] = quantity
            item["total_price"] = round(float(quantity) *  product_info['importPrice'],2)
            
        total_price+= round(item["total_price"],2)
        request.session["item"][product_id]= item
        items = request.session['item']
        request.session['total_price'] = total_price  
    else:
        error = "You must chosse product  and quantity you Get"
    context = {
                "supplier_products" :supplier_products, 
                "table_items" :items, 
                "total_price" :total_price, 
                "supplier_id" :supplier_id,
                "Error" : error,
            }
    return render(request,"create_purchase_recipt.html",context)