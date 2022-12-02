from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from merchant.models import Orders,Tyres,Client,order_items
from datetime import date

# Create your views here.
@login_required(login_url='/login/')
def AllOrders(request):
    if request.method == "GET":
        allorders = Orders.objects.filter(Client__name=request.session['username'])
        # orderids = list(Orders.objects.all().values_list('id',flat=True))
        # orderitems = order_items.objects.filter(order_id_id__in=orderids)
        context={
            'orders':allorders,
            # 'orderitems': orderitems
        }
        return render(request,'client/orders.html',context=context)

@login_required(login_url='/login/')
def NewOrder(request):
    if request.method == "POST":
        alltyres = Tyres.objects.all()
        print(request.session['username'])
        client = Client.objects.get(name=request.session['username'])
        order = Orders(Client=client,order_date=date.today(),status="Order Placed",order_amount=0.0)
        order.save()
        order = Orders.objects.get(id=order.id)
        isanytyresaved = 0
        total_amount = 0.0
        for tyre in alltyres:
            quantity = request.POST.get(str(tyre.id),0)
            print(tyre.id)
            print(quantity)
            if quantity is not None and quantity != 0 and quantity != "":
                amount = tyre.amount*int(quantity)
                total_amount += amount
                orderitem = order_items(order_id=order,quantity=quantity,amount=amount,item=tyre)
                orderitem.save()
                isanytyresaved = 1
        if isanytyresaved == 1:
            order.order_amount = total_amount
            order.save()
        else:
            order.delete()
        return redirect('/client/orders/')
    else:
        alltyres = Tyres.objects.all()
        context={
            'tyres':alltyres
            # 'orderitems': orderitems
        }
        return render(request,'client/neworder.html',context=context)
