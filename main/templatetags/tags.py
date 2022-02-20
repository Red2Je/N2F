from django import template
from ..models import ExpenseReport, Collaborator, ExpenseLine, Mission, RefundRequest

register = template.Library()
@register.filter
def sumRep(value,arg):
    sum = 0
    filt = list(RefundRequest.objects.filter(expenseReport = value))
    for eL in filt:
        sum += eL.amountTVA
    return str(sum)


@register.filter
def sumMission(value,arg):
    filtMiss = Mission.objects.get(name = value)
    filt = list(RefundRequest.objects.filter(expenseReport = arg).filter(mission = filtMiss))
    return str(len(filt))


@register.filter
def sumMissMoney(value,arg):
    sum = 0
    filtMiss = Mission.objects.get(name = value)
    filt = list(RefundRequest.objects.filter(expenseReport = arg).filter(mission = filtMiss))
    for eL in filt:
        sum += eL.amountTVA
    return (str(sum))


@register.filter
def sumMissionValid(value,arg):
    filtMiss = Mission.objects.get(id = value)
    filt = list(RefundRequest.objects.filter(expenseReport = arg,mission = filtMiss,state=ExpenseLine.sent))
    print(filt)
    return str(len(filt))


@register.filter
def sumMissMoneyValid(value,arg):
    sum = 0
    filtMiss = Mission.objects.get(id  = value)
    filt = list(RefundRequest.objects.filter(expenseReport = arg,mission = filtMiss,state=ExpenseLine.sent))
    for eL in filt:
        sum += eL.amountTVA
    print(filtMiss)
    print(filt)
    return (str(sum))


@register.filter
def get(dict,key):
    return(dict.get(key))


@register.filter
def urlFromFile(url,arg):
    try : 
        s = url.split('/')[1]
        return s
    except IndexError:
        return ''



@register.filter(name='get_class')
def get_class(value):
  return value.__class__.__name__

@register.filter
def get_from_pair(dict, args):
    argList = args.split('&')
    expRep = ExpenseReport.objects.get(id=int(argList[0]))
    mission = Mission.objects.get(id=int(argList[1]))
    return dict.get((expRep, mission))

@register.filter
def get_from_pair2(dict, args):
    argList = args.split('&')
    user = Collaborator.objects.get(id=int(argList[0]))
    expRep = ExpenseReport.objects.get(id=int(argList[1]))
    return dict.get((user, expRep))

@register.filter
def isHead(u,args):
    c = Collaborator.objects.get(user = u)
    return c.departmentHead is not None

@register.filter
def get_from_tuple(dict,args):
    argList = args.split('&')
    collab = Collaborator.objects.get(id = argList[0])
    expRep = ExpenseReport.objects.get(id = argList[1])
    mission = Mission.objects.get(id = argList[2])
    return dict.get((collab,expRep,mission))