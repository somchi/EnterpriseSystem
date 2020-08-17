from django.shortcuts import render, redirect, get_object_or_404
from .form import GoodsForm, ProductForm
from django.contrib import messages
from .models import Goods, Product
from django.views import generic
from Marketing.models import Demands
from django.db.models import Sum, Count
from django.forms import formset_factory

def create_goods(request):
    if request.method == "POST":
        form = GoodsForm(request.POST)
        if form.is_valid():
            form.save()
            #maybe have a member absolute url, redirect to member absolute url
            messages.success(request, "Your account was created successfully")
            return redirect('operation:products')
    else:
        form = GoodsForm()
    return render(request, "operation/create_goods.html", {'form':form})

def create_product(request):
    if request.method == "POST":
        form =ProductForm(request.POST)
        if form.is_valid():
            form.save()
            #maybe have a member absolute url, redirect to member absolute url
            messages.success(request, "Your account was created successfully")
            return redirect('operation:specification')
    else:
        form = ProductForm()
    return render(request, "operation/create_product.html", {'form':form})

class GoodsDetail(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        Objsale = Product.objects.get(pk=self.kwargs['pk'])
        context = super(GoodsDetail, self).get_context_data(**kwargs)
        goods = Goods.objects.all().filter(product_name_id=Objsale).aggregate(Sum('quantity_produced')).get('quantity_produced__sum')
        d = Demands.objects.all().filter(product_id=Objsale).dates('date_sold', 'day').aggregate(Sum('quantity')).get('quantity__sum')
        b = Demands.objects.filter(product_id=Objsale).values_list('quantity')
        a = Goods.objects.all().filter(product_name_id=Objsale).annotate()
        demand = Demands.objects.all().filter(product_id=Objsale).aggregate(Sum('quantity')).get('quantity__sum')
        context['d'] = d
        context['b'] = b
        context['demand'] = demand
        context['goods'] = goods
        context['a'] = a
        context['inventory'] = goods - demand
        return context

class ProductGoodsDetail(generic.DetailView):
    model = Product
    template_name = 'operation/product_detail'

class Inventory(generic.ListView):
    model = Product
    template_name = "operation/product_list.html"

    '''def get_context_data(self, **kwargs):
        context = super(Inventory, self).get_context_data(**kwargs)
        for i, j in enumerate(context):
            if j == context:
                goods = Goods.objects.all().filter(i).aggregate(Sum('quantity_produced')).get('quantity_produced__sum')
                demands = Demands.objects.all().aggregate(Sum('quantity')).get('quantity__sum')
                context['goods'] = goods
                context['demands']= demands
                context['count'] = goods-demands
                return context'''

class Specification(generic.ListView):
    model = Product
    template_name =  "operation/product_spec.html"

