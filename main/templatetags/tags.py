from django import template
from ..models import ExpenseReport, Collaborator, ExpenseLine, Mission

register = template.Library()
@register.filter
def sum(value,arg):
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
