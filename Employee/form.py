from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from .models import Employee, request, complain
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = Employee
        exclude = ('user', )
        widgets = {
            'staff_id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Staff ID'}),
            'title':forms.Select(attrs={'class': 'form-control'}),
            'sex':forms.Select(attrs={'class': 'form-control'}),
            'address':forms.Textarea(attrs={'class':'form-control'}),
            'marital_status':forms.Select(attrs={'class': 'form-control'}),
            'religion':forms.Select(attrs={'class': 'form-control'}),
            'position':forms.Select(attrs={'class': 'form-control'}),
            'unit':forms.Select(attrs={'class': 'form-control'}),
            'employee_type':forms.Select(attrs={'class': 'form-control'}),
            'hire_date':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Date Hired'}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone No'}),
            'state_of_origin':forms.Select(attrs={'class':'form-control'}),
            'maiden_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Maiden Name'}),
            'mothers_maiden_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Mother's Maiden Name"}),
            'state_of_residence':forms.Select(attrs={'class':'form-control'}),
            'lga':forms.Select(attrs={'class':'form-control'}),
            'country':forms.Select(attrs={'class':'form-control'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control datepicker'}),

            }

    def save(self):
        employee = super(EmployeeForm, self).save(commit=False)
        user = User(
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            username=self.cleaned_data['staff_id_number'],
            password = 's0m3DEfau!T'
            )
        user.save()
        employee.user = user
        employee.save()
        return employee

class AuthenticationFormWithPlaceholder(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'MEMBER ID'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))


class PasswordChangeFormWithPlaceholder(PasswordChangeForm):
    old_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'New Password'}))


class PasswordResetFormWithPlaceholder(PasswordResetForm):
    email = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Email'}))

class PasswordSetFormWithPlaceholder(SetPasswordForm):
    new_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder': 'New Password'}))
    confirm_new_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm New Password'}))

class RequestForm(forms.ModelForm):
    class Meta:
        model = request
        exclude = ('employee', 'created_by', )

    def save(self, employee, user):
        requests = super(RequestForm, self).save(commit=False)
        requests.employee = employee
        requests.created_by = user
        requests.save()

class ComplainForm(forms.ModelForm):
    class Meta:
        model = request
        exclude = ('employee', 'created_by', )

    def save(self, employee, user):
        complains = super(ComplainForm, self).save(commit=False)
        complains.employee = employee
        complains.created_by = user
        complains.save()