from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from .forms import ExpenseLineCreateForm
from .forms import ExpenseReportForm
from .models import ExpenseReport,Collaborator
import datetime
import os
# Create your views here.

def void(request):
	return render(request,'main/void.html')

def save_file(f):
	with open('proofs/'+f.name,'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


def createExpenseline(request):
	form = ExpenseLineCreateForm()
	if request.method == 'POST':
		form = ExpenseLineCreateForm(request.POST, request.FILES)
		if form.is_valid():

			obj = form.save(commit = False)
			col = Collaborator.objects.get(user = request.user)
			
			# Handle the users that does not have a report yet
			try:
				obj.expenseReport = ExpenseReport.objects.get(collaborator = col)
			except ExpenseReport.DoesNotExist:
				currMonth = datetime.datetime.now()
				currMonth = currMonth.strftime("%B")
				newReport = ExpenseReport(collaborator = col, month = currMonth.lower())
				newReport.save()
				obj.expenseReport = newReport
			obj.collaborator = col
			obj.validator = col.validator
			print("ca marche la mission ?")
			#mission ?
			print("oui")

			obj.save()
			save_file(request.FILES['proof'])
			return redirect('/void')
	context = {'form':form}
	return render(request, 'main/form.html', context) 


def createExpenseReport(request):
	form = ExpenseReportForm()
	if request.method == 'POST':
		form = ExpenseReportForm(request.POST)
		if form.is_valid():
			col = Collaborator.objects.get(user = request.user)
			form.save(collaborator=col)
			return redirect('/void')
			
	context = {'form':form}
	return render(request, 'main/form.html', context) 
