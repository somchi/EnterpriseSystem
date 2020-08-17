from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum
from django.forms.formsets import formset_factory
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _, ungettext
from Finance.forms import BatchForm, BatchPayTypeForm
from Finance.models import Batch, EmployeePaySummary
from django.views.generic.list import ListView

@permission_required('Finance.can_process_payroll')
def process(request):
    """Process payroll for selected employees."""
    Formset = formset_factory(BatchPayTypeForm)
    if request.method == 'POST':
        form = BatchForm(request.POST)
        formset = Formset(request.POST)
        if form.is_valid() and formset.is_valid():
            data = form.cleaned_data
            data.update({'processed_by': request.user})
            batch = Batch(**data)
            batch.save()
            for formset_form in formset.forms:
                batch_paytype = formset_form.save(commit=False)
                batch_paytype.batch = batch
                batch_paytype.save()
                formset_form.save_m2m()
            return redirect('finance:pay_batch_detail', id=batch.pk)
    else:
        form = BatchForm()
        formset = Formset()
        # Don't proceed if we have un-posted batches:
        if Batch.objects.filter(status=Batch.PROCESSED).exists():
            messages.error(request, _(u'There is an unposted batch. You need to Post or Delete it before you can continue.'))
    return TemplateResponse(request, 'finance/process.html', {'form': form, 'formset': formset})


class BatchDetailView(ListView):
    template_name = 'finance/batch_detail.html'
    allow_empty = True

    def get_queryset(self):
        self.batch = get_object_or_404(Batch, pk=self.kwargs['id'])
        queryset = EmployeePaySummary.objects.filter(batch=self.batch).order_by('employee__first_name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BatchDetailView, self).get_context_data(**kwargs)
        context['batch'] = self.batch
        return context

batch_detail = permission_required('Employee.can_manage_finance')(BatchDetailView.as_view())


class BatchListView(ListView):
    template_name = 'payprocess/batches.html'
    allow_empty = True

    def get_queryset(self):
        queryset = Batch.objects.exclude(status=Batch.DELETED)
        self.status = self.request.GET.get('status', 'all')
        if self.status != 'all':
            queryset = queryset.filter(status=getattr(Batch, self.status.upper()))
        queryset = queryset.annotate(num_employees=Count('employees'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BatchListView, self).get_context_data(**kwargs)
        context['status'] = self.status
        return context
