from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django import forms
from blockpoax.forms import UserRegistrationForm
from dashboard.models import Profile

def login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')

	user = authenticate(request, username=username, password=password)
	if user is not None:
		auth_login(request, user)
		return HttpResponseRedirect('/dashboard')
	else:
		return HttpResponseRedirect('/')

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			username = userObj['username']
			email_address =  userObj['email']
			password =  userObj['password']
			User = get_user_model()
			if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email_address).exists()):
				User.objects.create_user(username, email_address, password)
				user = authenticate(username = username, password = password)
				auth_login(request, user)
				profile = Profile(user = User.objects.get(username = username), balance = 0, email = email_address)
				profile.save()
				return HttpResponseRedirect('/dashboard')
			else:
				raise forms.ValidationError('Looks like a username with that email or password already exists')
	return HttpResponseRedirect('/')


def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')