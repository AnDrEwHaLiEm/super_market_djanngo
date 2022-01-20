from django.db import models,connection

from supplier.models import suppliers


class product(models.Model):
    _id: models.CharField(primary_key=True)
    p_name: models.CharField(max_length=20)
    price: models.DecimalField()
    p_type: models.CharField(max_length=20)
    quantityInMarket: models.DecimalField()
    quantityInStore: models.DecimalField()
    importPrice: models.DecimalField()
    unity: models.CharField(max_length=10)
    PackagePecies: models.DecimalField()
    supplier: models.ForeignKey(suppliers, on_delete=models.CASCADE)
    def __init__(self) -> None:
       pass

    def insert_into_product(self):
        c=connection.cursor()
        c.execute("CALL insert_product('"+self._id+"','"+self.p_name+"','"+self.price+"','"+self.p_type+"','"+self.importPrice+"','"+self.unity+"','"+self.PackagePecies+"','"+self.supplier+"')")
        
    def update_product(self):
        c=connection.cursor()
        c.execute("CALL update_product('"+self._id+"','"+self.p_name+"','"+self.price+"','"+self.p_type+"','"+self.quantityInMarket+"','"+self.quantityInStore+"','"+self.importPrice+"','"+self.unity+"','"+self.PackagePecies+"','"+self.supplier+"')")
    
    def delete_product(self):
        c=connection.cursor()
        c.execute("DELETE FROM product WHERE _id = "+self._id)
    
    def get_products_info(self):
        c=connection.cursor()
        c.execute("SELECT * FROM product")
        rows = c.fetchall()
        return rows
    
    def update_product_quantity(self,sale):
        c = connection.cursor()
        d = "CALL update_quantity_in_market('{}','{}')".format(self._id,sale)
        c.execute(d)
    
    def get_product_info_by_supplier(self):
        c = connection.cursor()
        d="SELECT _id,p_name,importPrice,unity FROM product WHERE supplier_id = {}".format(self.supplier)
        c.execute(d)
        rows = c.fetchall()
        return rows
    
    def get_product_name_supplier_unity(self):
        c = connection.cursor()
        d="SELECT p_name,unity,supplier_id FROM product WHERE _id = {}".format(self._id)
        c.execute(d)
        rows = c.fetchall()
        return rows
        
    def get_product_info(self):
        c=connection.cursor()
        c.execute("SELECT * FROM product WHERE _id = "+self._id)
        rows = c.fetchall()
        return rows


