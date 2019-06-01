from django.shortcuts import render
from django.http import JsonResponse
from requests import post
from telethon import TelegramClient, events, sync
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from dashboard.models import Status, OrderStatus, Order, Bitcoin, Ethereum, Paypal, PayTM, Profile
from django.contrib.auth.models import User

from telegram.models import Members

import json
import uuid

BASE_URL = 'https://justanotherpanel.com/api/v2'
API_KEY = '9d8b3ad11f12be740298875407f5f877'

def services(request):
	services = post(BASE_URL + '?key=' + API_KEY + '&action=services').text
	jso = {}
	services = json.loads(services)

	for key, service in enumerate(services):
		tmp_jso = {}
		tmp_jso['name'] = service['name']
		tmp_jso['min'] = service['min']
		tmp_jso['max'] = service['max']

		tmp_jso['rate'] = 3 * float(service['rate'])
		jso[key] = tmp_jso

	return JsonResponse(jso, safe = False)

def getMembers(request):
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if request.method == 'GET':
		service_name = "Telegram Members"
		link = request.GET.get('group-name')
		quantity = "N/A"
		username = User.objects.get(username = request.user.username)
		order_status = OrderStatus.objects.get(name = 'Complete')
		final_amount = "10"

		if balance < 10:
			order_status = OrderStatus.objects.get(name = 'Cancelled')
			txn = Order(
				service_name = "Telegram Members",
				link = request.GET.get('group-name'),
				quantity = 0,
				status = order_status,
				user_id = username,
				amount = 10,
				remark = "No sufficient funds in your account"
			)
			txn.save()
			return HttpResponseRedirect('/dashboard/orders')

		api_id = 667824
		api_hash = 'ba6b86596e43ea4a732736cb42a51e2a'
		client = TelegramClient('session_name', api_id, api_hash)
		client.start()
		participants = client.get_participants("ripple", aggressive = True)
		client.disconnect()

		out = ''
		for participant in participants:
			if participant.username is not None:
				out = out + "@" + participant.username + "\n"

		profile = Profile.objects.get(user = User.objects.get(username = request.user.username))
		fin_balance = float(balance) - float(final_amount)
		fin_balance = str(round(fin_balance, 2))
		profile.balance = fin_balance
		profile.save()

		slug = uuid.uuid4().hex

		members = Members(
			group_name = str(request.GET.get("group-name")),
			members = str(out),
			slug = slug,
		)

		members.save()

		txn = Order(
			service_name = service_name,
			link = link,
			quantity = 0,
			status = order_status,
			user_id = username,
			slug = slug,
			amount = 10
		)
		txn.save()

	return JsonResponse({"status": True})

@login_required
def place_order(request):
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if request.method == 'POST':
		service_name = request.POST.get('service_name')
		link = request.POST.get('link')
		quantity = request.POST.get('quantity')
		username = User.objects.get(username = request.user.username)
		order_status = OrderStatus.objects.get(name = 'Recieved')
		final_amount = request.POST.get('usd')

		if balance < float(final_amount):
			order_status = OrderStatus.objects.get(name = 'Cancelled')
			txn = Order(
				service_name = service_name,
				link = link,
				quantity = quantity,
				status = order_status,
				user_id = username,
				amount = final_amount,
				remark = "No sufficient funds in your account"
			)
			txn.save()
			return HttpResponseRedirect('/dashboard/orders')

		profile = Profile.objects.get(user = User.objects.get(username = request.user.username))
		fin_balance = float(balance) - float(final_amount)
		fin_balance = str(round(fin_balance, 2))
		profile.balance = fin_balance
		profile.save()

		txn = Order(
			service_name = service_name,
			link = link,
			quantity = quantity,
			status = order_status,
			user_id = username,
			amount = final_amount
		)
		txn.save()

		return HttpResponseRedirect('/dashboard/orders')
	return render(request, 'dashboard/pages/place_order.html', {
		'curr_page': curr_page,
		'balance': balance
	})
