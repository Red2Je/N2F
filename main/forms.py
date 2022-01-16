from django.forms import ModelForm
from .models import ExpenseLine



# form for update/create
		

class ExpenseLineCreateForm(ModelForm):
	class Meta:
		model = ExpenseLine
		fields = '__all__'
	