from ast import expr
from django.forms import ModelForm
from django import forms
from .models import Collaborator, ExpenseLine
from .models import ExpenseReport
from .models import RefundRequest
from .models import Advance
from .models import MileageExpense
import operator


# form for update/create
		

class RefundRequestForm(ModelForm):
    class Meta:
        model = RefundRequest
        fields = ['date', 'nature', 'expenseReport','mission','amountHT','amountTVA','proof']
        labels = {
            'date' : 'Date',
            'nature':'Nature',
            'expenseReport':'Note de frais',
            'mission':'Mission',
            'amountHT':'Remboursement hors taxe',
            'amountTVA':'Remboursement avec taxe',
            'proof':'Justificatif',
        }
        widgets = { 'date' : forms.SelectDateWidget}

    def __init__(self, *args, **kwargs, ):
        collab = kwargs.pop('collab',None)#kwargs is a list of argument that have keywords. if oyu call f(a, opt = 1), kwargs.pop('opt',None), return either 1 if opt is given and none if we call f(a)
        request = kwargs.pop('req',None)
        super(RefundRequestForm, self).__init__(*args, **kwargs)#very important that it must be here !
        if( request is not None and request.method == 'GET'):
            expRepL = ExpenseReport.objects.filter(collaborator = collab).order_by('-year') # we look for the the expense report of the user, order them by descending year
            self.fields['expenseReport'].queryset = expRepL#the queryset is the choice we have in the choicefield
            self.fields['expenseReport'].widget.choices = self.fields['expenseReport'].choices#we mus actualize the widget's choices along with the modek's choices
            self.fields['expenseReport'].initial = expRepL[0]# we set the initial value of the choice field to the most recent expense report




class AdvanceForm(ModelForm):
    class Meta:
        model = Advance
        fields = ['date', 'nature', 'expenseReport','mission','estimatedPrice','advanceCommentary']
        labels = {
            'date' : 'Date',
            'nature':'Nature',
            'expenseReport':'Note de frais',
            'mission':'Mission',
            'estimatedPrice' : 'Prix estime de la demande',
            'advanceCommentary' : "Commentaire",
        }
        widgets = { 'date' : forms.SelectDateWidget}

    def __init__(self, *args, **kwargs, ):
        collab = kwargs.pop('collab',None)
        request = kwargs.pop('req',None)
        super(AdvanceForm, self).__init__(*args, **kwargs)
        if(self.instance is None and request is not None and request.method == 'GET'):
            expRepL = ExpenseReport.objects.filter(collaborator = collab)
            c = [(" ".join((expRep.collaborator.user.username,expRep.month, str(expRep.year), 'aaaaaa')), expRep) for expRep in expRepL]
            self.fields['expenseReport'].choices =c


class MileageExpenseForm(ModelForm):
    class Meta:
        model = MileageExpense
        fields = ['date', 'nature', 'expenseReport','mission','carFiscalPower','startCity','endCity','distance','amountHT','amountTVA','proof']
        labels = {
            'date' : 'Date',
            'nature':'Nature',
            'expenseReport': 'Note de frais',
            'mission':'Mission',
            'carFiscalPower':'Puissance fiscale du vehicule',
            'startCity' : 'Ville de depart',
            'endCity' : "Ville d'arrivee",
            'distance':'Distance',
            'amountHT' : 'Remboursemnt hors taxes',
            'amountTVA' : 'Remoursement avec taxes',
            'proof' : 'Justificatif',
        }
        widgets = { 'date' : forms.SelectDateWidget}
    def __init__(self, *args, **kwargs ):
        collab = kwargs.pop('collab',None)
        request = kwargs.pop('req',None)
        super(MileageExpenseForm, self).__init__(*args, **kwargs)
        if(self.instance is None and request is not None and request.method == 'GET'):
            expRepL = ExpenseReport.objects.filter(collaborator = collab)
            c = [(" ".join((expRep.collaborator.user.username,expRep.month, str(expRep.year), 'aaaaaa')), expRep) for expRep in expRepL]
            self.fields['expenseReport'].choices =c

"""
class ExpenseLineCreateForm(ModelForm):
 
    class Meta:
        model = ExpenseLine
        fields = ['nature', 'date', 'amountHT', 'amountTVA','advance','proof','commentary','mission']
        labels = {
            'nature' : 'Nature',
            'date' : 'Date',
            'amountHT':'Remboursement hors taxe',
            'amountTVA':'Remboursement avec taxe',
            'advance':'Utiliser la somme avancée ?',
            'proof' : 'Preuve de dépense',
            'commentary':'Commentaires',
            'mission' : 'Mission'
        }
        mission = forms.ModelChoiceField(queryset=ExpenseLine.objects.all())
"""

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