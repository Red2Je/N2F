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
        collab = kwargs.pop('collab',None)
        request = kwargs.pop('req',None)
        passing = kwargs.pop('passing',False)
        super(RefundRequestForm, self).__init__(*args, **kwargs)
        if( not passing and request is not None and request.method == 'GET'):
            expRepL = ExpenseReport.objects.filter(collaborator = collab).order_by('-year')
            self.fields['expenseReport'].queryset = expRepL
            self.fields['expenseReport'].widget.choices = self.fields['expenseReport'].choices
            self.fields['expenseReport'].initial = expRepL[0]
            # c = [(str(expRep), expRep.id) for expRep in expRepL]
            # # c = sorted(c, key = lambda x: x[1].year, reverse=True)
            # self.fields['expenseReport'].choices =c




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