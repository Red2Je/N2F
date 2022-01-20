from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from .forms import ExpenseLineCreateForm
from .forms import ExpenseReportForm
from .models import ExpenseReport,Collaborator
import datetime
import os
import locale
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
				if(locale.LC_TIME != 'fr'):#avoid our month to be in english. As the database is in french, we force the format to be in french
					locale.setlocale(locale.LC_TIME,'fr')
				currMonth = datetime.datetime.now()
				currMonth = currMonth.strftime("%B")
				#Little piece of code to capitalize the first letter to match the database
				monthList = list(currMonth)
				monthList[0] = monthList[0].upper()
				currMonth = "".join(monthList)
				#
				newReport = ExpenseReport(collaborator = col, month = currMonth)
				newReport.save()
				obj.expenseReport = newReport
			obj.collaborator = col
			obj.validator = col.validator

			obj.save()
			save_file(request.FILES['proof'])
			return redirect('/void')
		else:
			print(form.errors)
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
