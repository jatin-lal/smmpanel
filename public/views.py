from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from dashboard.models import Profile
from blockpoax.forms import UserRegistrationForm
from django.contrib import messages
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

def home(request):
	form = UserRegistrationForm()
	"""send_mail(
	    'Subject here',
	    'Here is the message that is sent to confirm whether the Zoho Mail integration with the website SMMPanel.guru is working or not.',
	    'admin@smmpanel.guru',
	    ['jatinlal1994@gmail.com'],
	    fail_silently=False,
	)"""
	return render(request, 'public/pages/home.html', {
		'form': form
	})

def verify(request, token):
	try:
		profile = Profile.objects.get(verify_email_slug = token)
	except ObjectDoesNotExist:
		messages.add_message(request, messages.INFO, 'You have tried to access a wrong URL, please resend verification Email ID')
		return HttpResponseRedirect('/')

	profile.email_verified = True
	profile.save()

	messages.add_message(request, messages.INFO, 'Email ID Verified, you can now access dashboard')

	return HttpResponseRedirect('/dashboard')

@login_required
def resendEmail(request):
	email = User.objects.get(username = request.user.username).email
	temp_slug = Profile.objects.get(username = request.user.username).verify_email_slug
	send_mail(
	    'Verify your Email ID',
	    'Link to verify Email ID <a href="https://smmpanel.guru/verify-email/' + temp_slug + '">Verify Email ID</a>',
	    'admin@smmpanel.guru',
	    [email],
	    fail_silently=False,
	)
	messages.add_message(request, messages.INFO, 'Confirmation Email resent to ' + email)
	return HttpResponseRedirect('/')

def contact(request):
	if request.method == "POST":
		full_name = request.POST.get("full-name")
		email_id = request.POST.get('email-id')
		query = request.POST.get('query')

	send_mail(
	    full_name + ' contacted by footer contact page',
	    email_id + ' sent query \n\n ' + query,
	    'admin@smmpanel.guru',
	    ['jatinlal1994@gmail.com'],
	    fail_silently=False,
	)
	messages.add_message(request, messages.INFO, 'Thanks for contacting, We will reach out to you within next 24 hours')
	return HttpResponseRedirect('/')

def privacyPolicy(request):
	return render(request, 'public/pages/privacypolicy.html', {})

def tandc(request):
	return render(request, 'public/pages/tandc.html', {})

def disclaimer(request):
	return render(request, 'public/pages/disclaimer.html', {})

def aboutUs(request):
	return render(request, 'public/pages/about-us.html', {})

def handler404(request, *args, **argv):
	response = render_to_response('public/error/404.html', {},
	                  context_instance=RequestContext(request))
	response.status_code = 404
	return response

def handler500(request, *args, **argv):
	response = render_to_response('public/error/500.html', {},
	                              context_instance=RequestContext(request))
	response.status_code = 500
	return response