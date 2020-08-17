from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from Employee.models import Employee, Position, Unit, PayType
from django.db import models, transaction


class Batch(models.Model):
    """
    A batch represents a group of employee pay information processed together

    After processing, the batch's status will be PROCESSED can be either posted or deleted.
    modified_by is the user who either posts or deletes a batch
    """
    PROCESSED, POSTED, DELETED = 0, 1, 2
    STATUS_OPTIONS = (
        (PROCESSED, _(u'Processed')),
        (POSTED, _(u'Posted')),
        (DELETED, _(u'Deleted')),
    )

    process_from = models.DateField()
    process_to = models.DateField()
    status = models.PositiveIntegerField(choices=STATUS_OPTIONS, default=PROCESSED, editable=False)
    transaction_date = models.DateTimeField(default=datetime.now, editable=False)
    post_date = models.DateTimeField(blank=True, null=True)
    processed_by = models.ForeignKey(User, editable=False)
    modified_by = models.ForeignKey(User, editable=False, null=True, blank=True, related_name='batches_modified')
    employees = models.ManyToManyField('Employee.Employee', through='EmployeePaySummary')
    remarks = models.TextField(blank=True)

    class Meta:
        verbose_name = _(u'Batch')
        verbose_name_plural = _(u'Batches')
        ordering = ('-transaction_date',)
        permissions = (
            ('can_process_payroll', 'Can process payroll'),
            ('can_post_payroll', 'Can post payroll'),
            ('can_view_payroll_reports', 'Can view payroll reports'),
        )

    def __str__(self):
        return u'#%d: %s to %s' % (
            self.pk,
            self.process_from.strftime('%d-%b-%Y'),
            self.process_to.strftime('%d-%b-%Y'),
        )

    @permalink
    def get_absolute_url(self):
        return ('pay_batch_detail', (), {'id': self.pk})

    @property
    def get_is_processed(self):
        return self.status == self.PROCESSED

class EmployeePaySummary(models.Model):
    """
    The pay summary for an employee per batch

    total_entitlements and total_deductions help to denormalize for ease of
    obtaining net and gross pay for each employee in the batch
    """
    batch = models.ForeignKey(Batch, related_name='employee_pay_summary')
    employee = models.ForeignKey(Employee, related_name='employee_pay_summary')
    position = models.ForeignKey(Position)
    unit = models.ForeignKey(Unit)
    total_entitlements = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        verbose_name = _(u'Employee Pay Summary')
        verbose_name_plural = _(u'Employee Pay Summaries')
        ordering = ('-batch',)

    def __str__(self):
        return u'%s, batch: %s' % (self.employee, self.batch)

    @property
    def net_pay(self):
        return self.total_entitlements

    @property
    def gross_pay(self):
        return self.total_entitlements

    def get_bank(self):
        return self.employee.bank
    bank = property(get_bank)

class PayItem(models.Model):
    """
    Pay items that make up the salary of an employee.

    The category is used to differentiate between entitlements and deductions.
    The actual amount of the entitlement (or deduction) is computed from the
    formula (`PayFormula`) for this Pay item.
    """

    ENTITLEMENT = 0
    DEDUCTION = 1
    PAY_CATEGORIES = ((0, 'Entitlement'), (1, 'Deduction'))

    name = models.CharField(max_length=100, unique=True)
    category = models.PositiveIntegerField(choices=PAY_CATEGORIES)
    pay_type = models.ForeignKey(PayType)
    account_number = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = _(u'Pay Item')
        verbose_name_plural = _(u'Pay Items')
        ordering = ('category',)

    def __unicode__(self):
        return self.name

class ProcessedPayItem(models.Model):
    """
    info on the processed amount for each pay item per employee
    can either be entitlements or deductions (PAY_CATEGORIES)
    """
    summary = models.ForeignKey(EmployeePaySummary, related_name='processed_pay_items')
    pay_item = models.CharField(max_length=100)
    category = models.PositiveIntegerField(choices=PayItem.PAY_CATEGORIES)
    amount = models.DecimalField(max_digits=12,decimal_places=2)

    class Meta:
        verbose_name = _(u'Processed Pay Item')
        verbose_name_plural = _(u'Processed Pay Items')
        ordering = ('category', 'pay_item',)

    def __unicode__(self):
        return u'%s (%s): %.2f' % (self.pay_item, self.get_category_display(), self.amount)

    # TODO: Replace this property with a model field and make calculation part of payroll processing.


class BatchPayType(models.Model):
    batch = models.ForeignKey(Batch, related_name="pay_types")
    paytype = models.ForeignKey(PayType, related_name='batch_paytypes')


    class Meta:
        ordering = ('-batch',)

    def __unicode__(self):
        return self.paytype.name

