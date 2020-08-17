from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, request
from django.views import generic
from .form import EmployeeForm, RequestForm, ComplainForm
from django.http import HttpResponse
from django.contrib import messages
from .excel import ExcelReport


def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            #maybe have a member absolute url, redirect to member absolute url
            messages.success(request, "Your account was created successfully")
            return redirect('employee:employees')
    else:
        form = EmployeeForm()
    return render(request, "employee/add_employee.html", {'form':form})

class Employees(generic.ListView):
    model = Employee

class EmployeeDetail(generic.DetailView):
    model = Employee

    def get_object(self):
        return self.request.user.employee

class Profile(generic.DetailView):
    model = Employee

class EmployeeUpdate(generic.UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_update_form.html'

    def get_object(self):
        return self.request.user.employee

def export_members(request):
    query = Employee.objects.all()
    clients = ((m.staff_id_number, m.user.first_name, m.user.last_name, m.get_title_display(), m.get_marital_status_display(),m.sex,  m.birth_date.strftime('%Y-%m-%d') if m.birth_date else '',
                m.phone, m.address, str(m.position), str(m.unit), m.hire_date, m.salary, str(m.employee_type), str(m.bank), m. bank_account_number,
                m.maiden_name, m.mothers_maiden_name, m.get_religion_display(),m.national_id_number, m.passport_number, m.permanent_address, str(m.state_of_residence), str(m.country),
                str(m.state_of_origin), str(m.lga)) for m in query)
    fields = ["staff id", "first name", "last name", "title", "marital status","sex", "birth date", "phone", "address", "position", "unit", "hire date", "salary", "employee type","bank", "account number",
              "maiden name", "mother's maiden name","religion", "national id number", "passport_number", "permanent address", "state of residence", "country", "state of origin", "lga"]

    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=employees.xls"
    report = ExcelReport(clients, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response

def make_request(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save(employee, request.user)
            messages.success(request, "You have successfully made a request")
            return redirect('index')
    else:
        form = RequestForm()
    return render(request, "employee/make_request.html", {'form': form})

def make_complain(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        form = ComplainForm(request.POST)
        if form.is_valid():
            form.save(employee, request.user)
            messages.success(request, "You have successfully made a complain")
            return redirect('index')
    else:
        form = ComplainForm()
    return render(request, "employee/make_complain.html", {'form': form})

class RequestList(generic.ListView):
    model = request

class RequestDetail(generic.DetailView):
    model = Employee

class EmployeeList(generic.ListView):
    model = Employee
    template_name = 'employee/chat.html'


