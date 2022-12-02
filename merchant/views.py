from django.shortcuts import render,redirect
from merchant.models import Client,TyreTypes,Tyres,Orders,order_items
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# Create your views here.
@login_required(login_url='/login/')
def AllClients(req):
    if req.method == "GET":
        context={
            'clients':Client.objects.all(),
            'tyrecategories':TyreTypes.objects.all(),
            'Tyres':Tyres.objects.all(),
            'pending_count':Orders.objects.filter(status = "Order Placed").count()
        }
        return render (req,'merchant/allclients.html',context=context)
    else:
        return redirect('/library/Request/')

@login_required(login_url='/login/')
def AddClient(request):
    if request.method == "POST":
        name= request.POST.get('name','')
        email= request.POST.get('email','')
        phone_no = request.POST.get('phone_no','')
        if request.POST.get('ea','') == "Add":
            #Generate password randomly
            password= User.objects.make_random_password(length=8) 

            a=User.objects.create_user(name,phone_no,password)
            a.save()
            faculty= Client(name=name,email=email,phone=phone_no,password=password,ordercount=0,orderamount_received=0,orderamount_remaining=0)
            faculty.save()

            # Receiver email
            to=email
            # body and subject of mail 
            body="Hey %s ! \n \n Password for your Ce-Department Library account is %s \n"%(name,password)
            #Composing email and  sending mail
            email=EmailMessage('CE-Department',body,to=[to])
            email.send()
        return redirect('/merchant/clients/')

@login_required(login_url='/login/')
def AddTyreCategory(request):
    if request.method == "POST":
        tyrecategory= request.POST.get('tyrecategory','')
        tyrecategory_model= TyreTypes(type_name=tyrecategory)
        tyrecategory_model.save()
        return redirect('/merchant/clients/')

@login_required(login_url='/login/')
def AddTyre(request):
    if request.method == "POST":
        tyrecategory= request.POST.get('tyretype','')
        size= request.POST.get('size','')
        amount= request.POST.get('amount','')
        tyre_model= Tyres(type=tyrecategory,size=size,amount=amount)
        tyre_model.save()
        return redirect('/merchant/clients/')
    else:
        context={
            'tyretypes':TyreTypes.objects.all(),
            'pending_count':Orders.objects.filter(status = "Order Placed").count()
        }
        return render (request,'merchant/addtyre.html',context=context)

@login_required(login_url='/login/')
def EditOrder(request,id):
    if request.method == "POST":
        print(request.POST.getlist('mode',''))
        print(request.POST.getlist('debit',''))
        mode = ""
        if request.POST.getlist('cash',[''])[0] != 'cash':
            mode = "CASH"
        if request.POST.getlist('debit',[''])[0] != 'debit':
            mode = "DEBIT"
        order = Orders.objects.get(id=id)
        orderitems = order_items.objects.filter(order_id=order)
        alltyres = Tyres.objects.all()
        isanytyresaved = 0
        final_amount = order.order_amount
        amount = 0.0
        print(final_amount)
        for tyre in alltyres:
            quantity = int(request.POST.get(str(tyre.id),-1))
            orderitem = orderitems.get(item=tyre)
            print(quantity)
            print(orderitem.quantity)
            if orderitem is None and quantity != 0 and quantity > 0:
                print("qauntity changed from 0")
                amount = tyre.amount*int(quantity)
                final_amount += amount
                orderitem = order_items(order_id=order,quantity=quantity,amount=amount,item=tyre)
                orderitem.save()
                isanytyresaved = 1
                print(final_amount)
            elif orderitem is not None and quantity > orderitem.quantity and quantity > 0:
                print("qauntity changed from original >")
                #amount_to_minus = tyre.amount*int(orderitem.quantity)
                amount = tyre.amount*(int(quantity) - int(orderitem.quantity) )
                final_amount += amount
                orderitem.quantity = quantity
                orderitem.amount = amount
                #orderitem = order_items(order_id=order,quantity=quantity,amount=amount,item=tyre)
                orderitem.save()
                isanytyresaved = 1
                print(final_amount)
            elif orderitem is not None and quantity < orderitem.quantity and quantity > 0:
                print("qauntity changed from original <")
                amount = tyre.amount*int(quantity)
                final_amount -= tyre.amount*(int(orderitem.quantity) - int(quantity))
                #amount = tyre.amount*int(quantity)
                #total_amount += amount
                orderitem.quantity = quantity
                orderitem.amount = amount
                #orderitem = order_items(order_id=order,quantity=quantity,amount=amount,item=tyre)
                orderitem.save()
                isanytyresaved = 1
                print(final_amount)
            elif orderitem is not None and quantity == 0:
                print("qauntity changed to 0")
                final_amount -= tyre.amount*int(orderitem.quantity)
                orderitem.delete()
                isanytyresaved = 1
                print(final_amount)
        # if isanytyresaved == 1:
        print(final_amount)
        order.status = "Order Confirmed"
        order.order_amount = final_amount
        order.order_type = mode
        order.save() 
        return redirect('/merchant/clients/')
    else:
        order = Orders.objects.get(id=id,status="Order Placed")
        orderitems = order_items.objects.filter(order_id=order)
        otheritems = Tyres.objects.exclude(id__in=orderitems.values_list('item', flat=True))
        mode = (order.order_type if order.order_type is not None else "")
        l = []
        # data = {}
        for orderitem in orderitems:
            # print(orderitem)
            data = {}
            data["quantity"] = orderitem.quantity
            data["amount"] = orderitem.item.amount
            data["item"] = orderitem.item
            l.append(data)
            # print(data)
        for orderitem in otheritems:
            # print(orderitem)
            data = {}
            data["quantity"] = 0
            data["amount"] = orderitem.amount
            data["item"] = orderitem
            l.append(data)
            # print(l)
        print(l)
        context={
            'items':l,
            'id':id,
            'pending_count':Orders.objects.filter(status = "Order Placed").count(),
            'mode' : mode
        }
        return render (request,'merchant/editorder.html',context=context)

@login_required(login_url='/login/')
def UpdateOrder(request,id):
    if request.method == "POST":
        status = request.POST.get('status','')
        amount = float(request.POST.get('amount',''))
        order = Orders.objects.get(id=id)
        order.status = status
        order.amount_paid += amount
        order.save()
        return redirect('/merchant/clients/')

@login_required(login_url='/login/')
def OrderToUpdate(request):
    list = ["Order Confirmed","Partially paid"]
    allorders = Orders.objects.filter(status__in = list)
    # orderids = list(Orders.objects.all().values_list('id',flat=True))
    # orderitems = order_items.objects.filter(order_id_id__in=orderids)
    context={
        'orders':allorders,
        'pending_count':Orders.objects.filter(status = "Order Placed").count()
    }
    return render (request,'merchant/acceptedorders.html',context=context)

@login_required(login_url='/login/')
def OrdersCompleted(request):
    list = ["Paid - Completed"]
    allorders = Orders.objects.exclude(status__in = list)
    # orderids = list(Orders.objects.all().values_list('id',flat=True))
    # orderitems = order_items.objects.filter(order_id_id__in=orderids)
    context={
        'orders':allorders,
        'pending_count':Orders.objects.filter(status = "Order Placed").count()
    }
    return render (request,'merchant/ordercompleted.html',context=context)

@login_required(login_url='/login/')
def AllOrders(request):
    if request.method == "POST":
        tyrecategory= request.POST.get('tyretype','')
        size= request.POST.get('size','')
        amount= request.POST.get('amount','')
        tyre_model= Tyres(type=tyrecategory,size=size,amount=amount)
        tyre_model.save()
        return redirect('/merchant/orders/')
    else:
        context={
            'orders':Orders.objects.filter(status = "Order Placed"),
            'pending_count':Orders.objects.filter(status = "Order Placed").count()
        }
        return render (request,'merchant/orders.html',context=context)

@login_required(login_url='/login/')
def AllOrderswithoutfilter(request):
    if request.method == "POST":
        tyrecategory= request.POST.get('tyretype','')
        size= request.POST.get('size','')
        amount= request.POST.get('amount','')
        tyre_model= Tyres(type=tyrecategory,size=size,amount=amount)
        tyre_model.save()
        return redirect('/merchant/orders/')
    else:
        context={
            'orders':Orders.objects.all().order_by("-order_date"),
            'pending_count':Orders.objects.filter(status = "Order Placed").count()
        }
        return render (request,'merchant/allorders.html',context=context)


