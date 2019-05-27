from django.shortcuts import render

from django.shortcuts import render_to_response
from django.template import RequestContext

from blockpoax.forms import UserRegistrationForm

def home(request):
	form = UserRegistrationForm()
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