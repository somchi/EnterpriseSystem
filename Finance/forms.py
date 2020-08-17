from django import forms
from .base import ModelForm
from .widgets import CalendarWidget
from .models import Batch, BatchPayType

class BatchPayTypeForm(ModelForm):
    class Meta:
        model = BatchPayType
        exclude = ('batch',)

class BatchForm(ModelForm):
    process_from = forms.DateField(
            input_formats=('%d/%m/%Y',),
            widget=CalendarWidget(format='%d/%m/%Y'),
            required=True)
    process_to = forms.DateField(
            input_formats=('%d/%m/%Y',),
            widget=CalendarWidget(format='%d/%m/%Y'),
            required=True)

    class Meta:
        model = Batch
        exclude = ('employees', 'remarks', 'post_date')

    def clean(self):
        if 'process_from' not in self.cleaned_data:
            raise forms.ValidationError('Required fields')
        if not 'process_to' in self.cleaned_data:
            raise forms.ValidationError('Required fields')

        pending = Batch.objects.filter(status=Batch.PROCESSED).count()
        if pending == 1:
            raise forms.ValidationError("""There is still 1 unprocessed batch.
                    You have to post or delete it first""")
        elif pending > 1:
            raise forms.ValidationError("""There are still %s unprocessed batches.
                    You have to post or delete them first""" % pending)
        if 'process_to' in self.cleaned_data and 'process_from' in self.cleaned_data:
            if self.cleaned_data['process_from'] > self.cleaned_data['process_to']:
                raise forms.ValidationError('The date range given is invalid')
            return self.cleaned_data
