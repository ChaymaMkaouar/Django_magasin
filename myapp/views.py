from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required 
@login_required



def index(request):
    return render(request,'base.html')

def help(request):
    return render(request,'help.html' )



