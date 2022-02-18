
from time import strftime
from xmlrpc.client import DateTime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import MileageExpenseForm, RefundRequestForm, ExpenseReportForm, AdvanceForm
from .forms import RefundRequestForm
from .models import ExpenseReport, Collaborator, ExpenseLine, Advance, Mission, RefundRequest, MileageExpense
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.forms import ValidationError
import datetime
import os
import locale
import mimetypes






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
    valid = Collaborator.objects.get(user = request.user)
    

    context = {'valid' : valid}
    return render(request,'main/valid.html',context)

@login_required(login_url='/login/')
def cHistoric(request):
    u = Collaborator.objects.get(user = request.user)

    expRepL = []
    expLinDict = {}
    advDict = {}
    mileDict = {}
    missionDict = {}
    tempELDict ={}
    tempMDict = {}
    if ExpenseReport.objects.filter(collaborator=u).count() >= 1:
        expRepL = list(ExpenseReport.objects.filter(collaborator = u))
        for expRep in expRepL:
            filt = list(RefundRequest.objects.filter(expenseReport = expRep))
            if(Advance.objects.filter(expenseReport = expRep).count() >= 1):
                advDict[expRep] = list(Advance.objects.filter(expenseReport = expRep))
            filtMiss = [f.mission for f in filt]
            filtMiss = list(set(filtMiss))#remove duplicates
            missionDict[expRep] = filtMiss
            for miss in filtMiss:
                tempELDict[miss] = list(RefundRequest.objects.filter(expenseReport = expRep, mission = miss))
                expLinDict[expRep] = tempELDict
                if MileageExpense.objects.filter(expenseReport = expRep, mission = miss).count() >= 1:
                    tempMDict[miss] = list(MileageExpense.objects.filter(expenseReport = expRep, mission = miss))
                    mileDict[expRep] = tempMDict

    context = {'expRepL' : expRepL, 'collab' : u, 'expLinDict' : expLinDict, 'missDict' : missionDict, 'mileDict' : mileDict, 'advDict' : advDict}
    return render(request,'main/clientHistoric.html',context)

################################################################
#                 validator Homepage                           #
################################################################

@login_required(login_url='/login/')
def valid(request):
    validor = Collaborator.objects.get(user = request.user) # valideur
    CollaboratorList = [] # liste des collaborateurs du valideur
    DictNoteDeFrais = {} # dict de [collaborateur : [liste de notes de frais] ]
    DictLigneDeFrais= {} # dict de [Note de frais: [liste de ExpenseLine ] ]
    DictMission = {} # dict de  [Note de frais : [mission]

    if Collaborator.objects.filter(validator= validor).count() >= 1: # on ne fait rien si personne n'a ce valideur
        CollaboratorList = list(Collaborator.objects.filter(validator= validor))

        # recuperation de ses notes de frais, peut etre mettre une date limite sinon tout sera envoye
        for collabo in CollaboratorList:
            if ExpenseReport.objects.filter(collaborator = collabo) >= 1: # on ne fait rien si pas de note de frais
                DictNoteDeFrais[collabo]=list(ExpenseReport.objects.filter(collaborator = collabo))
                for notedefraise in DictNoteDeFrais[collabo]:
                    temp=[]
                    Mission=[]
                    temp=list(Advance.objects.filter(expenseReport= note))
                    Mission.append(f.mission for f in temp)
                    temp=list(MileageExpense.objects.filter(expenseReport= note))
                    Mission.append(f.mission for f in temp)
                    temp=list(RefundRequest.objects.filter(expenseReport= note))
                    Mission.append(f.mission for f in temp)
                    DictMission[notedefraise]=Mission  

            # on associe a chaque note de frais envoyee les lignes correspondantes
            for note in DictNoteDeFrais[collabo]:
                DictLigneDeFrais[note]=[] 
                # ajout de ses advances 
                DictLigneDeFrais[note].append(list(Advance.objects.filter(expenseReport= note).fitler(state = "sent")))
                # ajout de ses lignes de frais
                DictLigneDeFrais[note].append(list(RefundRequest.objects.filter(expenseReport= note).fitler(state = "sent")))
                # ajout de ses frais kilometriques
                DictLigneDeFrais[note].append(list(MileageExpense.objects.filter(expenseReport= note).fitler(state = "sent")))
        

    context = {'CollaboratorList' : CollaboratorList, 'DictNoteDeFrais' : DictNoteDeFrais, 'DictLigneDeFrais' : DictLigneDeFrais, 'validor' : validor,'DictMission' : DictMission }
    return render(request,'main/valid.html',context)




    
    
    # missionDict = {}
    # tempDict ={}

    # if ExpenseReport.objects.filter(collaborator=u).count() >= 1:
    #     expRepL = list(ExpenseReport.objects.filter(collaborator = u))
    #     for expRep in expRepL:
    #         filt = list(ExpenseLine.objects.filter(expenseReport = expRep))
    #         filtMiss = [f.mission for f in filt]
    #         missionDict[expRep] = filtMiss
    #         for miss in filtMiss:
    #             tempDict[miss] = list(ExpenseLine.objects.filter(expenseReport = expRep, mission = miss))
    #             expLinDict[expRep] = tempDict
    # context = {'expRepL' : expRepL, 'collab' : u, 'expLinDict' : expLinDict, 'missDict' : missionDict}
    # return render(request,'main/clientHistoric.html',context)


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



def collabAndReport(request):
    if (locale.LC_TIME != 'fr'):  # avoid our month to be in english. As the database is in french, we force the format to be in french
            locale.setlocale(locale.LC_TIME, 'fr')
    currMonth = datetime.datetime.now()
    currYear = currMonth.strftime("%Y")
    currMonth = currMonth.strftime("%B")
    # Little piece of code to capitalize the first letter to match the database
    monthList = list(currMonth)
    monthList[0] = monthList[0].upper()
    currMonth = "".join(monthList)

    col = Collaborator.objects.get(user=request.user)
    try:
        currExpenseReport = ExpenseReport.objects.get(collaborator=col, month=currMonth, year = currYear )
    except ExpenseReport.DoesNotExist:
        newReport = ExpenseReport(collaborator=col, month=currMonth, year=currYear)
        newReport.save()
        currExpenseReport = newReport

    return col,currExpenseReport


################################################################
#                      RefundRequest                           #
################################################################
@login_required(login_url='/login/')
def createRefundRequest(request, RefReq = None):
    #default the date to today
    today = datetime.date.today()
    today = today.strftime("%d/%m/%Y")
    # Handle the users that does not have a report yet
    col,currExpenseReport = collabAndReport(request)

    #if we give a refundrequest, display its state in the form
    form = RefundRequestForm(initial={'date':today}, collab=col, req = request)
    #if we give a refund request, and this refund request is not accepted (redundant with a verification in the html)
    if RefReq is not None and RefReq.state != RefundRequest.accepted:
        col = RefReq.expenseReport.collaborator
        form = RefundRequestForm(instance = RefReq, collab=col, req=request)#we pass the instance of the already existing refund request to let the model form generate itself

    if request.method == 'POST':
        form = RefundRequestForm(request.POST, request.FILES,instance = RefReq, collab=col, req = request)
        if form.is_valid():
            if RefReq is None:#if the refund request is not given, we check wich button is pressed
                toValidate = RefundRequest.draft
                if 'Submit' in request.POST:
                    toValidate = RefundRequest.sent
                obj = form.save(commit=False)
                obj.collaborator = col
                obj.validator = col.validator
                obj.state = toValidate

                obj.save()
                save_file(request.FILES['proof'])
                return redirect('/void')
            else:
                obj = form.save(commit = False)
                obj.collaborator = col
                obj.validator = col.validator
                obj.state = RefundRequest.sent
                if obj.proof != RefReq.proof :#if we give a new proof, we delete the old one from the server
                    RefReq.dele()
                    save_file(request.FILES['proof'])
                else:
                    obj.proof = RefReq.proof
                obj.proof = RefReq.proof
                obj.save()
                return redirect('/void')
        else:
            print("ERROR : ",form.errors)
    context = {'form': form}
    return render(request, 'main/form.html', context)


################################################################
#                         Advance                              #
################################################################

@login_required(login_url='/login/')
def createAdvanceRequest(request):
    col, expRep = collabAndReport(request)
    #default the date to today
    today = datetime.date.today()
    today = today.strftime("%d/%m/%Y")
    form = AdvanceForm(collab=col, initial={'date':today})
    if request.method == 'POST':

        form = AdvanceForm(request.POST, request.FILES, collab=col)
        if form.is_valid():
            toValidate = None
            if 'Submit' in request.POST:
                toValidate = False
            obj = form.save(commit=False)

            # Handle the users that does not have a report yet
            obj.expenseReport = expRep
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



################################################################
#                         Mileage                              #
################################################################

@login_required(login_url='/login/')
def createMileageExpense(request):
    col, expRep = collabAndReport(request)
    #default the date to today
    today = datetime.date.today()
    today = today.strftime("%d/%m/%Y")
    form = MileageExpenseForm(collab=col, initial={'date':today})
    if request.method == 'POST':

        form = MileageExpenseForm(request.POST, request.FILES, collab=col)
        if form.is_valid():
            toValidate = None
            if 'Submit' in request.POST:
                toValidate = False
            obj = form.save(commit=False)
            obj.expenseReport = expRep
            obj.collaborator = col
            obj.validator = col.validator
            obj.validated = toValidate

            obj.save()
            try:
                save_file(request.FILES['proof'])
            except MultiValueDictKeyError:
                pass
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
        return render(request, 'main/void.html')




################################################################
#                     Modify Refund Request                    #
################################################################
@login_required(login_url='/login/')
def modifyRefund(request, refId):
    RefReq = RefundRequest.objects.get(id = refId)
    print(RefReq)
    return createRefundRequest(request, RefReq=RefReq)


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
