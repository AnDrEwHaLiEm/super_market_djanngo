import datetime
from django.db import models,connection
from product.models import product

class recipt(models.Model):
    _id:models.CharField(primary_key=True)
    recipt_date:models.DateField()

    def __init__(self) -> None:
        pass
    
    def create_recipt(self):
        c = connection.cursor()
        d = "INSERT INTO recipt (_id) VALUES('{}')".format(self._id)
        c.execute(d)
    
    def get_all():
        c = connection.cursor()
        c.execute("SELECT * FROM recipt")
        rows = c.fetchall()
        return rows

    def get_all_by_type(self,status):
        c = connection.cursor()
        c.execute("SELECT * from recipt WHERE _id in (SELECT _id FROM total_price_recipt WHERE r_Type = '"+status+"')")
        rows = c.fetchall()
        return rows

    def get_one(self):
        c = connection.cursor()
        d = "SELECT * FROM recipt WHERE _id = '{}'".format(self._id)
        c.execute(d)
        row = c.fetchall()
        return row


class total_price_recipt(models.Model):
    _id : models.ForeignKey(recipt,on_delete=models.CASCADE,primary_key=True)
    total_profits:models.DecimalField()
    total_price:models.DecimalField()
    r_Type:models.CharField(max_length=10)

    def __init__(self) -> None:
        pass

    def create_recipt(self):
        c = connection.cursor()
        d = "INSERT INTO total_price_recipt(_id,r_Type) VALUES('{}','{}')".format(self._id,self.r_Type)
        c.execute(d)
    
    def update_recipt(self):
        c = connection.cursor()
        d = "UPDATE total_price_recipt SET total_price = '{}',total_profits='{}' WHERE _id = '{}'".format(self.total_price,self.total_profits,self._id)
        c.execute(d)
    
    def get_all_recipt(self,type):
        c = connection.cursor()
        c.execute("SELECT * FROM total_price_recipt WHERE r_Type = '"+type+"'")
        rows = c.fetchall()
        return rows
    


    def get_one(self):
        c = connection.cursor()
        d = "SELECT * FROM total_price_recipt WHERE _id = '{}'".format(self._id)
        c.execute(d)
        row = c.fetchall()
        return row
    
    def get_empty_recipt(self):
        c = connection.cursor()
        c.execute("SELECT * FROM total_price_recipt WHERE total_price = '0'")
        rows = c.fetchall()
        return rows


class product_recipt(models.Model):
    product_id:models.ForeignKey(product,on_delete=models.CASCADE,primary_key=True)
    recipt_id:models.ForeignKey(recipt,on_delete=models.CASCADE,primary_key=True)
    quantity:models.DecimalField()
    price:models.DecimalField()
    def __init__(self) -> None:
        pass

    def insert_product_recipt(self):
        c = connection.cursor()
        d = "INSERT INTO product_recipt VALUES ('{}','{}','{}','{}')".format(self.product_id,self.recipt_id,self.quantity,self.price)
        c.execute(d)

    def update_quantity(self):
        c = connection.cursor()
        d = "UPDATE product_recipt SET quantity = '{}' WHERE product_id = '{}' AND recipt_id = '{}'".format(self.quantity,self.product_id,self.recipt_id)
        c.execute(d)

    def delete_product_recipt(self):
        c = connection.cursor()
        d = "DELETE FROM product_recipt WHERE product_id = '{}' AND recipt_id = '{}'".format(self.product_id,self.recipt_id)
        print(d)
        c.execute(d)
    
    def get_one_recipt_product(self):
        c = connection.cursor()
        d = "SELECT * FROM product_recipt WHERE recipt_id = '{}'".format(self.recipt_id)
        c.execute(d)
        rows = c.fetchall()
        return rows

        

        
