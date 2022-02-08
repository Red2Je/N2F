from django import template
from ..models import ExpenseReport, Collaborator, ExpenseLine, Mission

register = template.Library()
@register.filter
def sumRep(value,arg):
    sum = 0
    filt = list(ExpenseLine.objects.filter(expenseReport = value))
    for eL in filt:
        sum += eL.amountTVA
    return str(sum)


@register.filter
def sumMission(value,arg):
    filtMiss = Mission.objects.get(name = value)
    filt = list(ExpenseLine.objects.filter(expenseReport = arg).filter(mission = filtMiss))
    return str(len(filt))


@register.filter
def sumMissMoney(value,arg):
    sum = 0
    filtMiss = Mission.objects.get(name = value)
    filt = list(ExpenseLine.objects.filter(expenseReport = arg).filter(mission = filtMiss))
    for eL in filt:
        sum += eL.amountTVA
    return (str(sum))


@register.filter
def get(dict,key):
    return(dict.get(key))


@register.filter
def urlFromFile(url,arg):
    return(url.split('/')[1])