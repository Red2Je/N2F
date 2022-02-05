
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from .forms import ExpenseLineCreateForm
from .forms import ExpenseReportForm
from .models import ExpenseReport, Collaborator
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import datetime
import os
import locale
import mimetypes



# Create your views here.

def logoutPage(request):
    logout(request)
    return render(request,'main/logout.html')

def user_login(request):
    #handle rediredct
    next = request.GET.get('next', '/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
            #if the user is valid and comes from another page, redirect him
            if(next != '/'):
                return redirect(next)
            return redirect('/void')
        else:
            form = AuthenticationForm()
            return render(request,'main/login.html',{'form':form})
     
    else:
        form = AuthenticationForm()
        return render(request, 'main/login.html', {'form':form})

def void(request):
    return render(request, 'main/void.html')


def save_file(f):
    with open('proofs/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required(login_url='/login/')
def sHistoric(request):
    return render(request,'main/historic.html')

@login_required(login_url='/login/')
def sValid(request):
    return render(request,'main/valid.html')

@login_required(login_url='/login/')
def cHistoric(request):
    return render(request,'main/clientHistoric.html')

@login_required(login_url='/login/')
def createExpenseline(request):
    form = ExpenseLineCreateForm()
    if request.method == 'POST':

        form = ExpenseLineCreateForm(request.POST, request.FILES)
        if form.is_valid():
            toValidate = None
            if 'Submit' in request.POST:
                toValidate = False
            obj = form.save(commit=False)
            col = Collaborator.objects.get(user=request.user)

            if (
                    locale.LC_TIME != 'fr'):  # avoid our month to be in english. As the database is in french,
                # we force the format to be in french
                locale.setlocale(locale.LC_TIME, 'fr')
            currMonth = datetime.datetime.now()
            currMonth = currMonth.strftime("%B")
            # Little piece of code to capitalize the first letter to match the database
            monthList = list(currMonth)
            monthList[0] = monthList[0].upper()
            currMonth = "".join(monthList)

            # Handle the users that does not have a report yet
            try:
                obj.expenseReport = ExpenseReport.objects.get(collaborator=col, month=currMonth)
            except ExpenseReport.DoesNotExist:
                newReport = ExpenseReport(collaborator=col, month=currMonth)
                newReport.save()
                obj.expenseReport = newReport
            obj.collaborator = col
            obj.validator = col.validator
            obj.validated = toValidate

            obj.save()
            save_file(request.FILES['proof'])
            return redirect('/void')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'main/form.html', context)

def download_file(request, filename=''):
	if filename != '':
		# Define Django project base directory
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		# Define the full file path
		filepath = BASE_DIR + '/proofs/' + filename
		# Open the file for reading content
		path = open(filepath, 'rb')
		# Set the mime type
		mime_type, _ = mimetypes.guess_type(filepath)
		# Set the return value of the HttpResponse
		response = HttpResponse(path, content_type=mime_type)
		# Set the HTTP header for sending to browser
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		# Return the response value
		return response
	else:
		# Load the template
		return render(request, 'void.html')

def createExpenseReport(request):
    form = ExpenseReportForm()
    if request.method == 'POST':
        form = ExpenseReportForm(request.POST)
        if form.is_valid():
            col = Collaborator.objects.get(user=request.user)
            form.save(collaborator=col)
            return redirect('/void')

    context = {'form': form}
    return render(request, 'main/form.html', context)



def home(request):
    return render(request, 'main/home.html')
