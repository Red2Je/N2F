from django.contrib import admin
from .models import ExpenseLine
from .models import ExpenseReport
from .models import Collaborator
from .models import Mission
from .models import Service, RefundRequest, MileageExpense, Advance

# Register your models here.







#class ExpenseLineAdmin(admin.ModelAdmin):
#    list_display1 = [field.name for field in ExpenseLine._meta.get_fields()]

class ExpenseReportAdmin(admin.ModelAdmin):
    list_display2 = [field2.name for field2 in ExpenseReport._meta.get_fields()]

class CollaboratorAdmin(admin.ModelAdmin):
    list_display3 = [field3.name for field3 in Collaborator._meta.get_fields()]

class MissionAdmin(admin.ModelAdmin):
    list_display4 = [field4.name for field4 in Mission._meta.get_fields()]


class ServiceAdmin(admin.ModelAdmin):
    list_display5 = [field5.name for field5 in Service._meta.get_fields()]

class RefundRequestAdmin(admin.ModelAdmin):
    list_display6 = [field6.name for field6 in RefundRequest._meta.get_fields()]
    
class MileageExpenseAdmin(admin.ModelAdmin):
    list_display7 = [field7.name for field7 in MileageExpense._meta.get_fields()]

class AdvanceAdmin(admin.ModelAdmin):
    list_display8 = [field8.name for field8 in Advance._meta.get_fields()]



#admin.site.register(ExpenseLine, ExpenseLineAdmin)
admin.site.register(ExpenseReport, ExpenseReportAdmin)
admin.site.register(Collaborator, CollaboratorAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(RefundRequest, RefundRequestAdmin)
admin.site.register(MileageExpense, MileageExpenseAdmin)
admin.site.register(Advance, AdvanceAdmin)
