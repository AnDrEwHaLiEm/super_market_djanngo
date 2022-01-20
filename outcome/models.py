from ast import mod
from django.db import models,connection

class outCome(models.Model):
    purchases:models.DecimalField()
    sales:models.DecimalField()
    total_profits:models.DecimalField()
    outcome_month:models.CharField(primary_key=True)
    
    def __init__(self) -> None:
        pass

    def get_all_outCome(self):
        c = connection.cursor()
        c.execute("SELECT * FROM outCome")
        rows = c.fetchall()
        return rows
