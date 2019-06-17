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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

import uuid

def login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')

	user = authenticate(request, username=username, password=password)
	if user is not None:
		auth_login(request, user)
		return HttpResponseRedirect('/dashboard')
	else:
		messages.add_message(request, messages.INFO, 'Either the Username or Password entered by you is incorrect')
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
				temp_slug = uuid.uuid4().hex
				profile.verify_email_slug = temp_slug
				profile.save()
				send_mail(
				    'Verify your Email ID',
				    'Link to verify Email ID <a href="https://smmpanel.guru/verify-email/' + temp_slug + '">Verify Email ID</a>',
				    'admin@smmpanel.guru',
				    [email_address],
				    fail_silently=False,
				)
				return HttpResponseRedirect('/dashboard')
			else:
				messages.add_message(request, messages.INFO, 'Looks like a username with that email or password already exists.')
				return HttpResponseRedirect('/')
	return HttpResponseRedirect('/')

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')

@login_required
def emailNotVerified(request):
	email = Profile.objects.get(user = User.objects.get(username = request.user.username)).email
	if Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		messages.add_message(request, messages.INFO, 'Your Email ID is already verified, you can now access your dashboard.')
		return HttpResponseRedirect('/dashboard')
	return render(request, "dashboard/error/email-not-verified.html", {
		'email': email
	})