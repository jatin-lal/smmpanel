from django.urls import path

from api import views as api

urlpatterns = [
	path('get-services', api.services, name='services'),
	path('get-members', api.getMembers, name='telegram-members-api'),
]