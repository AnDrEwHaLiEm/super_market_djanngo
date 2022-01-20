from django.db import connection, models

# Create your models here.


class suppliers(models.Model):
    supplier_id: models.CharField(primary_key=True)
    s_name: models.CharField(max_length=10)
    s_email: models.EmailField()

    def __init__(self) -> None:
        pass

    def insert_into_supplier(self):
        c=connection.cursor()
        c.execute("CALL insert_supplier('"+ self.supplier_id+ "','"+ self.s_name+ "','"+ self.s_email+ "')")
    
    def update_supplier(self):
        c=connection.cursor()
        c.execute("CALL update_supplier('"+ self.supplier_id+ "','"+ self.s_name+ "','"+ self.s_email+ "')")

    def delete_supplier(self):
        c=connection.cursor()
        c.execute("DELETE FROM suppliers WHERE supplier_id ="+self.supplier_id)

    def get_suppliers_info(self):
        c=connection.cursor()
        c.execute("SELECT * FROM suppliers")
        rows = c.fetchall()
        return rows

    def get_supplier_info(self):
        c=connection.cursor()
        c.execute("SELECT * FROM suppliers WHERE supplier_id = '" + self.supplier_id + "'")
        rows = c.fetchall()
        return rows


class supplier_phone(models.Model):
    _id: models.ForeignKey(suppliers, on_delete=models.CASCADE, primary_key=True)
    phone: models.CharField(primary_key=True)
    def __init__(self) -> None:
        pass

    def delete_supplier_phones(self):
        c = connection.cursor()
        c.execute("DELETE FROM  supplier_phone WHERE _id = "+self._id)
    
    def delete_phone(self,old_phone):
        c=connection.cursor()
        c.execute("DELETE FROM supplier_phone WHERE _id = "+self._id+" and phone = '"+old_phone+"'")

    def insert_into_supplier_phone(self):
        c=connection.cursor()
        c.execute("CALL insert_supplier_phone('"+ self._id+ "','"+ self.phone+ "')")
    
    def update_supplier_phone(self,old_phone):
        c=connection.cursor()
        c.execute("CALL update_supplier_phone('"+self._id+ "','"+ old_phone+"','"+self.phone+"')")

    def get_supplier_phones(self):   
        c=connection.cursor()
        c.execute("SELECT * FROM supplier_phone WHERE _id = '" + self._id+ "'")
        rows = c.fetchall()
        return rows
