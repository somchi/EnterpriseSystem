from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .models import Product, Demands, Goods,Production, Customers, Sale
from django.views import generic 
from django.contrib import messages
import urllib.request
import csv
from django.utils.dateparse import parse_datetime
from django.db.models import Sum, Count
from django.core.urlresolvers import reverse_lazy
import xlwt
from Employee.excel import ExcelReport
from xlwt import Workbook, easyxf

class DemandList(generic.ListView):
    model = Demands
    paginate_by = 8

class CreateDemand(generic.CreateView):
    template_name = 'marketing/create_demand.html'
    fields =['product', 'quantity', 'customer','date_sold', 'product_price', 'amount_paid']
    model = Demands
    success_url = reverse_lazy('marketing:demand-list')

class CreateProduction(generic.CreateView):
    template_name = 'marketing/create_production.html'
    fields =['product', 'quantity_pro']
    model = Production
    success_url = reverse_lazy('marketing:production-list')

class ProductionList(generic.ListView):
    model = Production

class Inventory(generic.ListView):
    model = Product
    template_name = "marketing/inventory.html"

    def get_context_data(self, **kwargs):
        context = super(Inventory, self).get_context_data(**kwargs)
        product = get_list_or_404(Product, pk=True)
        #sum_total = Product.objects.all().values_list('id', flat=True)
        context['total'] = Goods.objects.filter(product_name_id=product).aggregate(Sum('quantity_produced')).get('quantity_produced__sum')
        return context

class CustomerList(generic.ListView):
    template_name = 'marketing/customer_list.html'
    model = Customers
    context_object = 'customer_list'
    paginate_by = 8

class DemandDetail(generic.DetailView):
    template_name = 'marketing/customer_detail.html'
    model = Customers
    paginate_by = 8

    def get_context_data(self, **kwargs):
        pk = Customers.objects.get(pk=self.kwargs['pk'])
        demands = Demands.objects.all().filter(customer=pk)
        context = super(DemandDetail, self).get_context_data(**kwargs)
        context['count'] = demands.count()
        return context

class SaleCreate(generic.CreateView):
    template_name = 'marketing/sale_form.html'
    fields =['customer',]
    model = Sale
    success_url = reverse_lazy('marketing:sale')

class AddCustomer(generic.CreateView):
    template_name = 'marketing/customer_form.html'
    fields =['customer_name', 'DOB', 'address', 'phone', 'gender', ]
    model = Customers
    success_url = reverse_lazy('marketing:create_customer')

class SaleList(generic.ListView):
    template_name = 'marketing/sales.html'
    model = Sale
    context_object = 'sale_list'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(SaleList, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context

class SaleDetailView(generic.DetailView):
    template_name = 'marketing/sale_detail.html'
    model = Sale

    def get_context_data(self, **kwargs):
        Objsale = Sale.objects.filter(pk=self.kwargs['pk'])
        #SaleItem = SaleDetail.objects.all().filter(sale=Objsale)
        context = super(SaleDetailView, self).get_context_data(**kwargs)
        #context['count'] = SaleItem.count()
        context['Sale'] = Objsale.count()
        #context['Items'] = SaleItem
        return context

class SalesSearch(generic.ListView):
    template_name = 'marketing/demand.html'
    model = Demands
    context_object_name = 'demands'

    def get(self, *args, **kwargs):
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')
        query = Demands.objects.all().filter(date_sold__range=(start, end))
        book = Workbook(encoding='utf8')
        sheet = book.add_sheet('report')

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_LEFT
        alignment.vert = xlwt.Alignment.VERT_TOP
        style = xlwt.XFStyle()
        style.alignment = alignment

        header_font = xlwt.Font()
        header_font.name = 'Trebuchet MS'
        header_font.height = 240
        header_font.width = 100
        header_font.color = 'black'
        header_font.bold = True

        header_style = xlwt.XFStyle()
        header_style.font = header_font

        data_font = xlwt.Font()
        data_font.height = 220
        data_font.name = 'Trebuchet MS'
        data_font.color = 'gray80'
        data_font.borders = 'bottom 3'
        data_font.width = 220

        data_style = xlwt.XFStyle()
        data_style.font = data_font
        header = ["Product Name", "Customer Name", "Date Sold", "Quantity", "Price of Product (N)", "Cost of Sales (N)",
                  "Amount Paid (N)", "Balance (N)", "Date Created"]
        for hcol, hcol_data in enumerate(header):
            sheet.write(0, hcol, hcol_data, header_style)
        quantity = Demands.objects.all().filter(date_sold__range=(start, end)).aggregate(Sum('quantity')).get('quantity__sum')
        expected = Demands.objects.all().filter(date_sold__range=(start, end)).aggregate(Sum('subtotal')).get('subtotal__sum')
        paid = Demands.objects.all().filter(date_sold__range=(start, end)).aggregate(Sum('amount_paid')).get('amount_paid__sum')
        unpaid = Demands.objects.all().filter(date_sold__range=(start, end)).aggregate(Sum('balance')).get('balance__sum')
        data = ([str(d.product), str(d.customer), d.date_sold.strftime('%Y-%m-%d') if d.date_sold else '', d.quantity,
                 d.product_price, d.subtotal, d.amount_paid, d.balance,
                 d.date_created.strftime('%Y-%m-%d') if d.date_created else ''] for d in query)
        for row, row_data in enumerate(data, start=1):  # start from row no.1
            for col, col_data in enumerate(row_data):
                sheet.write(row, col, col_data, data_style)
        analysis = [quantity, expected, paid, unpaid]
        head = ["Quantity ", "Total Sales Cost (N)", "Amount Collected (N)", "Unpaid (N)"]
        for hcol, hcol_data in enumerate(head):
            sheet.write(20, hcol, hcol_data, header_style)
        for arow, row_data in enumerate(analysis):
            sheet.write(21, arow, row_data, data_style)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=report.xls'
        book.save(response)
        return response



def export_sales(request):
    query = Demands.objects.all()
    clients = ((str(m.product), m.quantity, str(m.customer), m.date_sold.strftime('%Y-%m-%d') if m.date_sold else '',
                m.product_price, m.date_created.strftime('%Y-%m-%d') if m.date_created else '', m.amount_paid, m.subtotal ) for m in query)
    fields = ["product", "quantity", "customer", "date sold", "product price","date created",
              "amount paid", "subtotal"]

    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=sales.xls"
    report = ExcelReport(clients, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response









