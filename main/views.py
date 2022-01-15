from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect

# Create your views here.

def void(request):
	return render(request,'main/void.html')