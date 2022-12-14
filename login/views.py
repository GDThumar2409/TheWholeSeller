from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.views.generic import TemplateView
from django.db import IntegrityError
import traceback
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.
def mylogin(request):

    if(request.user.is_anonymous):
        return render(request,'login/index.html')
    return HttpResponseRedirect("/merchant/clients/")


def authenticate(request):
    try:
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        a=User.objects.get(username=username)
        x=auth.authenticate(username=username,password=password)

        if x is not None:
            auth.login(request,x)
            request.session['username']=username
            print(request.session['username'])
            if username == "admin":
                return HttpResponseRedirect("/merchant/clients/")
            else:
                return HttpResponseRedirect("/client/orders/")
        else:
             r="Invalid Username or Password"
             return render(request,'login/index.html',{"error":r})
    except:
        r="Invalid Username or Password"
        return render(request,'login/index.html',{"error":r})



def logout(request):
    auth.logout(request)
    request.session['username']=None
    return HttpResponseRedirect('/login/')



def createadmin(request):
    a=User.objects.create_user("admin","admin@gmail.com","admin")
    a.save()
    return HttpResponse("added")
