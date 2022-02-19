from time import strftime
from xmlrpc.client import DateTime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import MileageExpenseForm, RefundRequestForm, ExpenseReportForm, AdvanceForm
from .forms import RefundRequestForm
from .models import ExpenseReport, Collaborator, ExpenseLine, Advance, Mission, RefundRequest, MileageExpense
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.forms import ValidationError
from django.contrib.auth.decorators import user_passes_test
import datetime
import os
import locale
import mimetypes

#Check is the user is a validator
def is_validator(user):
    u= Collaborator.objects.get(user=user)
    return u.departmentHead is not None

def logoutPage(request):
    logout(request)
    return render(request, 'main/logout.html')


def user_login(request):
    # handle rediredct
    next = request.GET.get('next', '/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # if the user is valid and comes from another page, redirect him
            if next != '/':
                return redirect(next)
            return redirect('/void')
        else:
            form = AuthenticationForm()
            return render(request, 'main/login.html', {'form': form})

    else:
        form = AuthenticationForm()
        return render(request, 'main/login.html', {'form': form})


def void(request):
    return render(request, 'main/void.html')


def save_file(f):
    with open('proofs/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='/login/')
@user_passes_test(is_validator)
def sHistoric(request):
    u = Collaborator.objects.get(user=request.user)
    service = u.departmentHead
    uL = []
    expRepDict = {}
    advDict = {}
    mileDict = {}
    missionDict = {}
    expLinDict = {}
    if service is not None:
        uL = list(Collaborator.objects.filter(service=service))
        for user in uL:
            expRepDict[user] = list(ExpenseReport.objects.filter(collaborator=user))
            for expRep in expRepDict[user]:
                filt = list(RefundRequest.objects.filter(expenseReport=expRep))
                filtMiss = [f.mission for f in filt]
                filtMiss = list(set(filtMiss))  # remove duplicates
                missionDict[(user, expRep)] = filtMiss
                for miss in filtMiss:
                    expLinDict[(user, expRep, miss)] = list(RefundRequest.objects.filter(expenseReport=expRep, mission=miss))
                    advDict[(user,expRep,miss)] = list(Advance.objects.filter(expenseReport=expRep, mission=miss))
                    mileDict[(user,expRep,miss)] = list(MileageExpense.objects.filter(expenseReport=expRep, mission=miss))
                    expLinDict[(user,expRep,miss)] = [e for e in expLinDict[(user,expRep,miss)] if e.id not in [m.id for m in mileDict[(user,expRep,miss)]]]

    print(expRepDict.get(uL[0]))
    context = {'expRepDict': expRepDict, 'uL': uL, 'expLinDict': expLinDict, 'missDict': missionDict, 'mileDict': mileDict,
               'advDict': advDict}
    return render(request, 'main/historic.html', context)


@login_required(login_url='/login/')
def cHistoric(request):
    u = Collaborator.objects.get(user=request.user)

    expRepL = []
    expLinDict = {}
    advDict = {}
    mileDict = {}
    missionDict = {}
    if ExpenseReport.objects.filter(collaborator=u).count() >= 1:
        expRepL = list(ExpenseReport.objects.filter(collaborator=u).order_by('year', '-month'))
        for expRep in expRepL:
            filt = list(RefundRequest.objects.filter(expenseReport=expRep))
            filtMiss = [f.mission for f in filt]
            filtMiss = list(set(filtMiss))  # remove duplicates
            missionDict[expRep] = filtMiss
            for miss in filtMiss:
                expLinDict[(expRep, miss)] = list(RefundRequest.objects.filter(expenseReport=expRep, mission=miss))
                advDict[(expRep,miss)] = list(Advance.objects.filter(expenseReport=expRep, mission=miss))
                mileDict[(expRep,miss)] = list(MileageExpense.objects.filter(expenseReport=expRep, mission=miss))
                expLinDict[(expRep,miss)] = [e for e in expLinDict[(expRep,miss)] if e.id not in [m.id for m in mileDict[(expRep,miss)]]]
                    
                print(advDict)
    context = {'expRepL': expRepL, 'collab': u, 'expLinDict': expLinDict, 'missDict': missionDict, 'mileDict': mileDict,
               'advDict': advDict}
    return render(request, 'main/clientHistoric.html', context)


################################################################
#                 validator Homepage                           #
################################################################

@login_required(login_url='/login/')
@user_passes_test(is_validator)
def valid(request):
    validor = Collaborator.objects.get(user=request.user)  # valideur
    CollaboratorList = []  # liste des collaborateurs du valideur
    DictNoteDeFrais = {}  # dict de [collaborateur : [liste de notes de frais] ]
    DictMileageExpense = {}  # dict de [Note de frais: [liste de MileageExpense ] ]
    DictRefundRequest = {}  # dict de [Note de frais: [liste de RefundRequest ] ]
    DictAdvance = {}  # dict de [Note de frais: [liste de Advance ] ]
    DictMission = {}  # dict de  [Note de frais : [RefundRequest] ]

    if Collaborator.objects.filter(validator=validor).count() >= 1:  # on ne fait rien si personne n'a ce valideur
        CollaboratorList = list(Collaborator.objects.filter(validator=validor))

        # recuperation de ses notes de frais, peut etre mettre une date limite sinon tout sera envoye
        for collabo in CollaboratorList:
            if ExpenseReport.objects.filter(collaborator=collabo).count() >= 1:  # on ne fait rien si pas de note de frais
                DictNoteDeFrais[collabo] = list(ExpenseReport.objects.filter(collaborator=collabo))

                for notedefraise in DictNoteDeFrais[collabo]:
                    DictMission[notedefraise] = []

                    if RefundRequest.objects.filter(expenseReport=notedefraise).count() >= 1:
                        filt = list(RefundRequest.objects.filter(expenseReport=notedefraise))
                        Mission = [f.mission for f in filt]
                        Mission = list(set(Mission))  # remove duplicates
                        DictMission[notedefraise] += Mission # stockage des missions pour l'affichage
                        for miss in Mission:
                            DictRefundRequest[(notedefraise,miss)] = list(RefundRequest.objects.filter(expenseReport=notedefraise)) # ligne de frais de l'utilisateur pour cette note de frais
                        

                    if Advance.objects.filter(expenseReport=notedefraise).count() >= 1:
                        filt = list(Advance.objects.filter(expenseReport=notedefraise))
                        Mission = [f.mission for f in filt]
                        Mission = list(set(Mission))  # remove duplicates
                        DictMission[notedefraise] += Mission # stockage des missions pour l'affichage
                        for miss in Mission:
                            DictAdvance[(notedefraise,miss)] = list(Advance.objects.filter(expenseReport=notedefraise)) # avance de l'utilisateur pour cette note de frais
                        

                    if MileageExpense.objects.filter(expenseReport=notedefraise).count() >= 1:
                        filt = list(MileageExpense.objects.filter(expenseReport=notedefraise))
                        Mission = [f.mission for f in filt]
                        Mission = list(set(Mission))  # remove duplicates
                        DictMission[notedefraise] += Mission # stockage des missions pour l'affichage
                        for miss in Mission:
                            DictMileageExpense[(notedefraise,miss)] = list(MileageExpense.objects.filter(expenseReport=notedefraise)) # frais kilométriques de l'utilisateur pour cette note de frais

                            DictRefundRequest[(notedefraise,miss)] = [e for e in DictRefundRequest[(notedefraise,miss)] if e.id not in [m.id for m in DictMileageExpense[(notedefraise,miss)]]]

        """
        if request.method == 'POST':
            RefundRequestvalided= request.POST.getlist('validRefundRequest')
            print(RefundRequestvalided)
            Mileagevalided= request.POST.getlist('validMileage')
            Advancevalided= request.POST.getlist('validAvance')
            for refundamodif in RefundRequestvalided:
                 amodif =RefundRequest.objects.filter( id = RefundRequestvalided )
                 amodif.state='Accepté'
                 amodif.save()
        """
        if request.method == 'POST':
            fruits = request.POST.getlist('validRefundRequest')
            print(fruits)




                    
                    
                    


    context = {'CollaboratorList': CollaboratorList, 'DictNoteDeFrais': DictNoteDeFrais,
               'DictAdvance': DictAdvance,'DictMileageExpense': DictMileageExpense,'DictRefundRequest': DictRefundRequest,
                'validor': validor, 'DictMission': DictMission}
    return render(request, 'main/valid.html', context)

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
        return render(request, 'main/void.html')


def collabAndReport(request):
    if (
            locale.LC_TIME != 'fr'):  # avoid our month to be in english. As the database is in french, we force the format to be in french
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
        currExpenseReport = ExpenseReport.objects.get(collaborator=col, month=currMonth, year=currYear)
    except ExpenseReport.DoesNotExist:
        newReport = ExpenseReport(collaborator=col, month=currMonth, year=currYear)
        newReport.save()
        currExpenseReport = newReport

    return col, currExpenseReport


################################################################
#                      RefundRequest                           #
################################################################
@login_required(login_url='/login/')
def createRefundRequest(request, RefReq=None):
    # default the date to today
    today = datetime.date.today()
    today = today.strftime("%d/%m/%Y")
    # Handle the users that does not have a report yet
    col, currExpenseReport = collabAndReport(request)

    # if we give a refundrequest, display its state in the form
    form = RefundRequestForm(initial={'date': today}, collab=col, req=request)
    # if we give a refund request, and this refund request is not accepted (redundant with a verification in the html)
    if RefReq is not None and RefReq.state != RefundRequest.accepted:
        col = RefReq.expenseReport.collaborator
        form = RefundRequestForm(instance=RefReq, collab=col,
                                 req=request)  # we pass the instance of the already existing refund request to let the model form generate itself

    if request.method == 'POST':
        form = RefundRequestForm(request.POST, request.FILES, instance=RefReq, collab=col, req=request)
        if form.is_valid():
            if RefReq is None:  # if the refund request is not given, we check wich button is pressed
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
                obj = form.save(commit=False)
                obj.collaborator = col
                obj.validator = col.validator
                obj.state = RefundRequest.sent
                if obj.proof != RefReq.proof:  # if we give a new proof, we delete the old one from the server
                    RefReq.dele()
                    save_file(request.FILES['proof'])
                else:
                    obj.proof = RefReq.proof
                obj.proof = RefReq.proof
                obj.save()
                return redirect('/void')
        else:
            print("ERROR : ", form.errors)
    context = {'form': form}
    return render(request, 'main/form.html', context)

################################################################
#                      ConsultRefund                           #
################################################################
@login_required(login_url='/login/')
def consultRefund(request, refId):
    RefReq = RefundRequest.objects.get(id=refId)
    print(RefReq)
    return createConsultRefund(request, RefReq=RefReq)

@login_required(login_url='/login/')
def createConsultRefund(request, RefReq=None):
    validor = Collaborator.objects.get(user=request.user)  # valideur
    print(Collaborator.objects.filter(validator=validor).count())
    if Collaborator.objects.filter(validator=validor).count() < 1:  # on ne fait rien si personne n'a ce valideur
        return redirect('/void')
    ligneDeFrais = RefundRequest.objects.get(id=RefReq.id)
    context = {'ldf':ligneDeFrais}
    return render(request, 'main/consult.html', context)

################################################################
#                         Advance                              #
################################################################

@login_required(login_url='/login/')
def createAdvanceRequest(request, AdvRef=None):
    col, expRep = collabAndReport(request)
    # default the date to today
    today = datetime.date.today()
    today = today.strftime("%d/%m/%Y")
    form = AdvanceForm(collab=col, initial={'date': today})

    if AdvRef is not None and AdvRef.state != RefundRequest.accepted:
        col = AdvRef.expenseReport.collaborator
        form = AdvanceForm(instance=AdvRef, collab=col,
                                 req=request)  # we pass the instance of the already existing refund request to let the model form generate itself


    if request.method == 'POST':

        form = AdvanceForm(request.POST, request.FILES, collab=col)
        if form.is_valid():
            if AdvRef is None : 
                toValidate = RefundRequest.draft
                if 'Submit' in request.POST:
                    toValidate = RefundRequest.sent
                obj = form.save(commit=False)

                # Handle the users that does not have a report yet
                obj.proof = None
                obj.expenseReport = expRep
                obj.collaborator = col
                obj.validator = col.validator
                obj.validated = toValidate

                obj.save()
                return redirect('/void')
            else:
                obj = form.save(commit=False)
                obj.collaborator = col
                obj.validator = col.validator
                obj.state = RefundRequest.sent
                obj.proof = None
                obj.save()
                return redirect('/void')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'main/form.html', context)


################################################################
#                         Mileage                              #
################################################################

@login_required(login_url='/login/')
def createMileageExpense(request, MilRef=None):
    col, expRep = collabAndReport(request)
    # default the date to today
    today = datetime.date.today()
    today = today.strftime("%d/%m/%Y")
    form = MileageExpenseForm(initial={'date': today},collab=col, req = request)

    if MilRef is not None and MilRef.state != RefundRequest.accepted:
            col = MilRef.expenseReport.collaborator
            form = MileageExpenseForm(instance=MilRef, collab=col,
                                    req=request)  # we pass the instance of the already existing refund request to let the model form generate itself

    if request.method == 'POST':

        form = MileageExpenseForm(request.POST, request.FILES, collab=col)
        if form.is_valid():
            if MilRef is not None:
                toValidate = RefundRequest.draft
                if 'Submit' in request.POST:
                    toValidate = RefundRequest.sent
                obj = form.save(commit=False)
                obj.expenseReport = expRep
                obj.collaborator = col
                obj.validator = col.validator
                obj.validated = toValidate

                obj.save()
                save_file(request.FILES['proof'])
            else:
                obj = form.save(commit=False)
                obj.collaborator = col
                obj.validator = col.validator
                obj.state = RefundRequest.sent
                if obj.proof != MilRef.proof:  # if we give a new proof, we delete the old one from the server
                    MilRef.dele()
                    save_file(request.FILES['proof'])
                else:
                    obj.proof = MilRef.proof
                obj.save()
                return redirect('/void')
            return redirect('/void')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'main/form.html', context)


################################################################
#                     Modify Refund Request                    #
################################################################
@login_required(login_url='/login/')
def modifyRefund(request, refId):
    RefReq = RefundRequest.objects.get(id=refId)
    return createRefundRequest(request, RefReq=RefReq)

@login_required(login_url='/login/')
def modifyAdvance(request, advId):
    RefReq = Advance.objects.get(id=advId)
    return createAdvanceRequest(request, AdvRef=RefReq)

@login_required(login_url='/login/')
def modifyMileage(request, milId):
    RefReq = MileageExpense.objects.get(id=milId)
    return createMileageExpense(request, MilRef=RefReq)


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