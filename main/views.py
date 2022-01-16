from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from .forms import ExpenseLineCreateForm
from .forms import ExpenseReportForm
# Create your views here.

def void(request):
	return render(request,'main/void.html')

def createExpenseline(request):
	form = ExpenseLineCreateForm()
	if request.method == 'POST':
		form = ExpenseLineCreateForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/void')
			
	context = {'form':form}
	return render(request, 'main/form.html', context) 


def createExpenseReport(request):
	form = ExpenseReportForm()
	if request.method == 'POST':
		form = ExpenseReportForm(request.POST)
		if form.is_valid():
			form.save(user=request.user, commit=False)
			return redirect('/void')
			
	context = {'form':form}
	return render(request, 'main/form.html', context) 
