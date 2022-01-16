from django.db import models
from django.contrib.auth.models import User
from .dataValidator import validate_file_type
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

class Service(models.Model):
    #id = models.fields.IntegerField(unique=True)
    name = models.fields.CharField(max_length=100)
    def __str__(self):
	    return self.name

class Mission(models.Model):
    #id = models.fields.IntegerField(unique=True)
    name = models.fields.CharField(max_length=100)

    def __str__(self):
	    return self.name

#class Validator(models.Model):
#    substitite = models.fields.BooleanField(default=False)

#    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)

class Collaborator(models.Model):
    #id = models.fields.IntegerField(unique=True)
    #login = models.fields.CharField(max_length=100)
    #password = models.fields.CharField(max_length=500) # pas en clair pour le modele, longueur a modifier selon le codage
    #firstname = models.fields.CharField(max_length=100)
    #lastname = models.fields.CharField(max_length=100)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isvalidator = models.fields.BooleanField(default=False)

    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    validator = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='cValidator')

    def __str__(self):
	    return self.user.username


class ExpenseReport(models.Model):
    #id = models.fields.IntegerField(unique=True)
    january  = 'Janvier'
    february  = 'Fevrier'
    march  = 'Mars'
    april  = 'Avril'
    may  = 'Mai'
    june  ='Juin'
    july  = 'Juillet'
    august  = 'Aout'
    september  = 'Septembre'
    october  = 'Octobre'
    november  = 'Novembre'
    december  = 'Decembre'
   
    Month_CHOICES = [
		(january  , 'Janvier'),
		(february  , 'Fevrier'),
        (march  , 'Mars'),
		(april  , 'Avril'),
		(may,'Mai'),
		(june,'Juin'),
		(july,'Juillet'),
		(august,'Aout'),
		(september,'Septembre'),
        (october,'Octobre'),
        (november,'Novembre'),
        (december,'Decembre'),
    ]
    month = models.CharField(
        max_length=20,
		choices=Month_CHOICES,
	)
    
    collaborator = models.ForeignKey(Collaborator, null=True, on_delete=models.SET_NULL) # ~~~~~~

    

    def __str__(self):
	    return str(self.collaborator.user.username) +" "+self.month

class ExpenseLine(models.Model):
    #id = models.fields.IntegerField(unique=True)
    nature = models.fields.CharField(max_length=100)
    date = models.fields.DateField()
    amountHT = models.fields.FloatField()
    amountTVA = models.fields.FloatField()
    advance = models.fields.BooleanField(default=False)
    proof = models.FileField(upload_to='proofs',validators = [validate_file_type])
    commentary = models.fields.CharField(max_length=1000)
    validated = models.fields.BooleanField(null=True)

    expenseReport = models.ForeignKey(ExpenseReport, null=True, on_delete=models.SET_NULL)
    collaborator = models.ForeignKey(Collaborator, null=True, on_delete=models.SET_NULL, related_name='elCollaborator')
    validator = models.ForeignKey(Collaborator, null=True, on_delete=models.SET_NULL, related_name='elValidator')
    mission = models.ForeignKey(Mission, null=True, on_delete=models.SET_NULL)

    @receiver(pre_delete)
    def dele(sender,instance,**kwargs):
        os.remove(instance.proof.name)
    def __str__(self):
	    return self.nature+' '+self.proof.name



