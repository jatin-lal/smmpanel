from django.shortcuts import render

from django.shortcuts import render_to_response
from django.template import RequestContext

from blockpoax.forms import UserRegistrationForm

from django.core.mail import send_mail

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