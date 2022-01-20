from django.contrib import admin
from django.urls import path
from mainPage import views
from supplier import views as supplier_views
from product import views as product_views
from recipt import views as recipt_views
from outcome import views as outcome_views

urlpatterns = [
    path("", views.main_page),
    path("supplier/create_supplier", supplier_views.create_supplier_form),
    path("supplier/insert_update_supplier", supplier_views.insert_update_supplier),
    path("supplier/get_All_supplier", supplier_views.show_all_supplier),
    path("supplier/get_One_supplier", supplier_views.show_One_supplier),
    path("supplier/operation_supplier", supplier_views.operation_supplier),
    path("product/create_product", product_views.create_product_form),
    path("product/insert_update_product", product_views.insert_update_product),
    path("product/get_All_product", product_views.show_all_product),
    path("product/get_One_product", product_views.show_One_product),
    path("product/operation_product", product_views.operation_product),
    path("recipt/create_recipt", recipt_views.create_recipt),
    path("recipt/main_sale_recipt_page", recipt_views.chose_sale_operation),
    path("recipt/main_purchase_recipt_page", recipt_views.chose_purchase_operation),
    path("recipt/get_all_recipt",recipt_views.get_all_recipt),
    path("recipt/get_one_recipt",recipt_views.get_one_recipt),
    path("outcom/get_All_out_com",outcome_views.get_all_out_come),
]
