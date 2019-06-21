from django.shortcuts import render
from django.http import JsonResponse
from requests import post
from telethon import TelegramClient, events, sync
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from dashboard.models import Status, OrderStatus, Order, Bitcoin, Ethereum, Paypal, PayTM, Profile
from django.contrib.auth.models import User
from django.contrib import messages
from telegram.models import Members

import telethon

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
				link = "https://t.me/" + request.GET.get('group-name'),
				quantity = 0,
				status = order_status,
				user_id = username,
				amount = 10,
				remark = "No sufficient funds in your account"
			)
			txn.save()
			messages.add_message(request, messages.ERROR, 'No sufficient funds in your account')
			return HttpResponseRedirect('/dashboard/orders')

		api_id = 667824
		api_hash = 'ba6b86596e43ea4a732736cb42a51e2a'
		client = TelegramClient('session_name', api_id, api_hash)
		client.start()
		try:
			participants = client.get_participants(link, aggressive = True)
		except ValueError:
			client.disconnect()
			return JsonResponse({"status": False, "error": "A Telegram Account or Telegram Group with such Username does not exist"})
		except telethon.errors.rpcerrorlist.ChatAdminRequiredError:
			client.disconnect()
			return JsonResponse({"status": False, "error": "Please add and promote @ngage as admin of this group or channel to fetch members"})
		if len(participants) == 1:
			client.disconnect()
			return JsonResponse({"status": False, "error": "This is a username User Profile's Username, please enter Username of a Group"})
		client.disconnect()

		out = ''
		for participant in participants:
			if participant.username is not None:
				out = out + "@" + participant.username + "\n"

		profile = Profile.objects.get(user = User.objects.get(username = request.user.username))
		fin_balance = float(balance) - float(final_amount)
		fin_balance = str(round(fin_balance, 5))
		profile.balance = fin_balance
		spent = Profile.objects.get(user = User.objects.get(username = request.user.username)).spent
		spent_amount = float(spent) + 10.00
		profile.spent = spent_amount
		profile.save()

		slug = uuid.uuid4().hex

		no_of_members = len(out.split("@"))
		members = Members(
			group_name = str(request.GET.get("group-name")),
			members = str(out),
			no_of_members = no_of_members,
			slug = slug,
		)

		members.save()

		txn = Order(
			service_name = service_name,
			link = link,
			quantity = no_of_members,
			status = order_status,
			user_id = username,
			slug = slug,
			amount = 10
		)
		txn.save()

		messages.add_message(request, messages.SUCCESS, 'Group fetched succesfully, click on Download file to view usernames')

	return JsonResponse({"status": True})