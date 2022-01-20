from django.shortcuts import render
from .models import outCome


def get_all_out_come(request):
    out_come = outCome()
    show_all_out_come = out_come.get_all_outCome()
    Error = False
    context={}
    if len(show_all_out_come) == 0 :
        Error = True
    
    context={
        "out_come" : show_all_out_come,
        "Error" : Error,
    }
    return render(request,"get_all_outcome.html",context)

