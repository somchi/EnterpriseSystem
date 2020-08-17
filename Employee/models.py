from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

EMPLOYEE_TITLES = (
    (1, 'Mr'),
    (2, 'Mrs'),
    (3, 'Miss'),
    (4, 'Dr'),
    (5, 'Prof'),
    (6, 'Mallam'),
    (7, 'Chief'),
    (8, 'Alhaji'),
    (9, 'Alhaja'),
    (10, 'J.P.'),
)

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

RELIGION_CHOICES = (
    (1, 'Christianity'),
    (2, 'Islam'),
    (300, 'Others'),
)

BLOOD_GROUP_CHOICES = (
    ('A', 'A'),
    ('AB', 'AB'),
    ('B', 'B'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)

GENOTYPE_CHOICES = (
    ('AA', 'AA'),
    ('AS', 'AS'),
    ('SS', 'SS'),
)

MARITAL_STATUS_CHOICES = (
    ('S', 'Single'),
    ('M', 'Married'),
    ('W', 'Widowed'),
    ('D', 'Divorced'),
)


class EmployeeType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, related_name='employee')
    staff_id_number = models.CharField(max_length=30, unique=True, blank=True)
    photo = models.ImageField(upload_to='employees/photo/', blank=True)
    title = models.PositiveIntegerField(choices=EMPLOYEE_TITLES, blank=True, null=True)
    marital_status = models.CharField(max_length=50, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='F')
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    position = models.ForeignKey(Position, related_name='employees')
    unit = models.ForeignKey(Unit, related_name='employees')
    hire_date = models.DateField()
    salary = models.DecimalField(verbose_name='Gross pay', max_digits=14, decimal_places=2, blank=True, null=True)
    employee_type = models.ForeignKey(EmployeeType, blank=True, null=True)
    bank = models.ForeignKey(Bank, blank=True, null=True)
    monthly_pay = models.CharField(max_length=10, blank=True)
    bank_account_number = models.CharField(max_length=20, blank=True)
    maiden_name = models.CharField(max_length=50, blank=True)
    mothers_maiden_name = models.CharField(max_length=50, blank=True)
    religion = models.PositiveSmallIntegerField(choices=RELIGION_CHOICES, blank=True)
    blood_group = models.CharField(max_length=2, choices=BLOOD_GROUP_CHOICES, blank=True)
    genotype = models.CharField(max_length=2, choices=GENOTYPE_CHOICES, blank=True)
    national_id_number = models.CharField(max_length=50, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    permanent_address = models.TextField(blank=True)
    state_of_residence = models.ForeignKey('State.State')
    country = models.ForeignKey('State.Country', related_name='employee_country', blank=True)
    state_of_origin = models.ForeignKey('State.State', related_name='employees_origin', blank=True)
    lga = models.ForeignKey('State.LGA', related_name='employees', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        permissions = (
            ('can_manage_employees', 'Can manage employees'),
            ('can_export_employees', 'Can export employee data'),
            ('can_view_personal_info', 'Can view personal information'),
            ('can_manage_personal_info', 'Can manage personal information'),
            ('can_manage_operation', 'Can manage Operation'),
            ('can_manage_marketing', 'Can manage marketing'),
            ('can_manage_finance', 'Can manage finance'),
            ('can_manage_store', 'Can mange store'),
            ('can_create_department', 'Can create department'),
            ('can_create_employee', 'Can create employee'),
            ('can_create_position', 'Can create position'),
            ('can_create_product', 'Can create product'),
            ('can_add_customer', 'Can add customer'),
            ('can_view_inventory', 'Can view inventory'),
            ('can_view_sales', 'Can view sales'),

        )
    def __str__(self):
        return self.user.get_full_name()

class PayType(models.Model):
    """
    Mechanism for breaking the pay items into different categories.

    These categories can be processed separately, or at the same time.
    This is mostly useful in situations where certain pay items will not be
    processed at all times (think "13th month").

    It allows us the flexibility of selecting which pay items will be processed.
    For example, the "13th month" pay items are processed in December, while bulk
    Transportation allowance will be paid by August.
    """

    MONTHLY, WEEKLY, ANNUAL = range(3)
    DURATION_TYPES = enumerate((('Monthly'), ('Weekly'), ('Annually')))

    MULTIPLIERS = {MONTHLY: 12, WEEKLY: 52, ANNUAL: 1}

    name = models.CharField(max_length=20, unique=True)
    frequency = models.PositiveIntegerField(default=1)
    duration = models.PositiveIntegerField(choices=DURATION_TYPES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    @property
    def number_per_annum(self):
        """This is the number of times this paytype is given per annum"""
        return self.frequency * self.MULTIPLIERS[self.duration]

class request(models.Model):
    employee = models.ForeignKey(Employee, editable=False)
    created_by = models.ForeignKey(User, editable=False, null=True)
    request = models.TextField()
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    substitute = models.ForeignKey(Employee, blank=True, related_name="employeerequest")
    date_created = models.DateField(editable=False, auto_now_add=True)

class complain(models.Model):
    employee = models.ForeignKey(Employee, editable=False)
    created_by = models.ForeignKey(User, editable=False, null=True)
    complain_suggestion = models.TextField()
    date_created = models.DateField(editable=False, auto_now_add=True)

class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.message