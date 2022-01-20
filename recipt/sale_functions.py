from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import product_recipt, recipt, total_price_recipt
from product.models import product


def add_sale_recipt(request):
    product_items = request.session['item']
    total_price = request.session['total_price']
    total_profit = request.session['total_profit'] 
    recipt_id = request.session['recipt_id']
    for key in product_items:
        sale_quantity = round(-1 * float(product_items[key]['quantity']),2)
        product_class = product()
        product_class._id = key
        product_class.update_product_quantity(sale_quantity)

    total_price_class = total_price_recipt()
    total_price_class._id = recipt_id
    total_price_class.total_price = total_price
    total_price_class.total_profits = total_profit
    total_price_class.update_recipt()

    return HttpResponseRedirect("http://127.0.0.1:8000/recipt/create_recipt?status=sale")


def remove_sale_item(request):
    product_id = request.GET.get('remove')
    items = request.session['item']
    total_price = request.session['total_price']
    total_profit = request.session['total_profit']
    recipt_id = request.session['recipt_id']

    product_recipt_class = product_recipt()
    product_recipt_class.product_id = product_id
    product_recipt_class.recipt_id = recipt_id
    product_recipt_class.delete_product_recipt()

    total_price = round(total_price-items[product_id]['total_price'],2)
    total_profit = round(total_profit - items[product_id]['total_profit'],2)

    items.pop(product_id,False)
    request.session['total_profit'] = total_profit
    request.session['total_price'] = total_price
    request.session['item'] = items
    return HttpResponseRedirect("main_sale_recipt_page")


def add_sale_item(request):
    recipt_id = request.session['recipt_id']
    items = request.session['item']
    total_price = request.session['total_price']
    total_profit = request.session['total_profit']
    product_id = request.POST["product_id"]
    quantity = request.POST["product_quantity"]
    error = ""
    item = {}
    product_class = product()
    recipt_product_class =  product_recipt()
    product_class._id = product_id
    recipt_product_class.product_id = product_id
    recipt_product_class.recipt_id = recipt_id
    recipt_product_class.quantity = quantity
    if len(product_id)  and len(quantity):
        product_info = product_class.get_product_info()
        if len(product_info):
            if product_info[0][4] >= float(quantity):
                if product_id in items:
                    item = request.session['item'][product_id]
                    total_profit = round(total_profit - item['total_profit'],2)
                    total_price = round(total_price-item['total_price'],2)
                    item['quantity'] = quantity
                    item['total_price'] = round(float(quantity) * product_info[0][2],2)
                    item['total_profit'] =  round(item['total_price'] -(float(quantity) * product_info[0][6]),2)
                    recipt_product_class.update_quantity()
                else :
                    recipt_product_class.price = product_info[0][2]
                    recipt_product_class.insert_product_recipt()       
                    request.session['item'][product_id] = {}
                    item = request.session['item'][product_id]
                    item["id"] = product_id    
                    item["p_name"] = product_info[0][1]
                    item["price"] = product_info[0][2]
                    item["unity"] = product_info[0][7]
                    item["importPrice"] = product_info[0][6]
                    item["quantity"] = quantity
                    item["total_price"] = round(float(quantity) * product_info[0][2],2)
                    item["total_profit"] = round(item['total_price'] - (float(quantity) * product_info[0][6]),2)
                
                total_price+= round(item["total_price"],2)
                total_profit+= round(item["total_profit"],2)
                request.session["item"][product_id]= item
                items = request.session['item']
                request.session['total_price'] = total_price
                request.session['total_profit'] = total_profit   
            else:
                error = "quantity less than you want"
        else:
            error = "product Not exist"
    else:
        error = "You must enter product id and quantity you need"
    context = {
        "table_items":items,
        "total_price":total_price,
        "Error":error,            
    }
    return render(request,"create_sale_recipt.html",context)