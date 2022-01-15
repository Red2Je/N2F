from django.db import models

class Service(models.Model):
    #id = models.fields.IntegerField(unique=True)
    name = models.fields.CharField(max_length=100)

class Mission(models.Model):
    #id = models.fields.IntegerField(unique=True)
    nae = models.fields.CharField(max_length=100)


#class Validator(models.Model):
#    substitite = models.fields.BooleanField(default=False)

#    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)

class Collaborator(models.Model):
    #id = models.fields.IntegerField(unique=True)
    login = models.fields.CharField(max_length=100)
    password = models.fields.CharField(max_length=500) # pas en clair pour le modele, longueur a modifier selon le codage
    firstname = models.fields.CharField(max_length=100)
    lastname = models.fields.CharField(max_length=100)
    isvalidator = models.fields.BooleanField(default=False)

    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    validator = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='cValidator')


class ExpenseReport(models.Model):
    #id = models.fields.IntegerField(unique=True)
        
    class Month(models.TextChoices):
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
    
    collaborator = models.ForeignKey(Collaborator, null=True, on_delete=models.SET_NULL) # ~~~~~~

class ExpenseLine(models.Model):
    #id = models.fields.IntegerField(unique=True)
    nature = models.fields.CharField(max_length=100)
    date = models.fields.DateField()
    amountHT = models.fields.FloatField()
    amountTVA = models.fields.FloatField()
    advance = models.fields.BooleanField(default=False)
    proof = models.FileField(upload_to='proofs') 
    commentary = models.fields.CharField(max_length=1000)
    validated = models.fields.BooleanField(null=True)

    expenseReport = models.ForeignKey(ExpenseReport, null=True, on_delete=models.SET_NULL)
    collaborator = models.ForeignKey(Collaborator, null=True, on_delete=models.SET_NULL, related_name='elCollaborator')
    validator = models.ForeignKey(Collaborator, null=True, on_delete=models.SET_NULL, related_name='elValidator')
    mission = models.ForeignKey(Mission, null=True, on_delete=models.SET_NULL)
