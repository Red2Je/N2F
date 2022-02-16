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