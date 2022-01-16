from django.forms import ModelForm
from .models import Collaborator, ExpenseLine
from .models import ExpenseReport



# form for update/create
		

class ExpenseLineCreateForm(ModelForm):

	
	class Meta:
		model = ExpenseLine
		fields = ['nature', 'date', 'amountHT', 'amountTVA','advance','proof','commentary','validated']
	

class ExpenseReportForm(ModelForm):
    class Meta:
        model = ExpenseReport
        fields = ('month',)  # take out user you don't need it here

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(ExpenseReportForm, self).save(**kwargs)
        instance.user = user
        instance.save()
        return instance