from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import requests

from .models import Status, OrderStatus, Order, Bitcoin, Ethereum, Paypal, PayTM, Profile
from telegram.models import Members
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse

@login_required
def home(request):
	curr = "home"
	profile = Profile.objects.get(user = User.objects.get(username = request.user.username))
	balance = profile.balance
	spent = profile.spent
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")

	orders = Order.objects.filter(user_id = User.objects.get(username = request.user.username)).order_by('-created_at')[:10]
	return render(request, 'dashboard/pages/home.html', {
		'balance': balance,
		'spent': spent,
		'orders': orders,
		'curr': curr
	})

@login_required
def newOrder(request):
	curr = "new-order"
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
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
			messages.add_message(request, messages.ERROR, 'No sufficient funds in your account')
			return HttpResponseRedirect('/dashboard/orders')

		try:
			requests.get(link).status_code
		except requests.exceptions.ConnectionError:
			order_status = OrderStatus.objects.get(name = 'Cancelled')
			txn = Order(
				service_name = service_name,
				link = link,
				quantity = quantity,
				status = order_status,
				user_id = username,
				amount = final_amount,
				remark = "The link you have provided is not working, please check the link"
			)
			txn.save()
			messages.add_message(request, messages.ERROR, 'Please check the link you have provided')
			return HttpResponseRedirect('/dashboard/orders')
		except requests.exceptions.SSLError:
			order_status = OrderStatus.objects.get(name = 'Cancelled')
			txn = Order(
				service_name = service_name,
				link = link,
				quantity = quantity,
				status = order_status,
				user_id = username,
				amount = final_amount,
				remark = "The link you have provided is not working, please check the link"
			)
			txn.save()
			return HttpResponseRedirect('/dashboard/orders')

		profile = Profile.objects.get(user = User.objects.get(username = request.user.username))
		spent = Profile.objects.get(user = User.objects.get(username = request.user.username)).spent

		spent_amount = float(spent) + float(final_amount)

		fin_balance = float(balance) - float(final_amount)
		fin_balance = str(round(fin_balance, 2))
		profile.spent = spent_amount
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

		messages.add_message(request, messages.SUCCESS, 'Your order has been placed succesfully')

		return HttpResponseRedirect('/dashboard/orders')

	return render(request, 'dashboard/pages/new-order.html', {
		'balance': balance,
		'curr': curr
	})

@login_required
def wallet(request):
	curr = 'wallet'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	spent = Profile.objects.get(user = User.objects.get(username = request.user.username)).spent
	return render(request, 'dashboard/pages/wallet.html', {
		'balance': balance,
		'spent': spent,
		'curr': curr
	})

@login_required
def telegram(request):
	curr = "telegram"
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	return render(request, 'dashboard/pages/telegram-services.html', {
		'balance': balance,
		"curr": curr
	})

@login_required
def website(request):
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	return render(request, 'dashboard/pages/website-services.html', {
		'balance': balance
	})

@login_required
def ico(request):
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	return render(request, 'dashboard/pages/ico-services.html', {
		'balance': balance
	})

@login_required
def press(request):
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	return render(request, 'dashboard/pages/press-release-services.html', {
		'balance': balance
	})

@login_required
def paytm(request):
	curr = 'wallet'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	if request.method == 'POST':
		number = request.POST.get('number')
		amount = request.POST.get('amount')
		txn_id = request.POST.get('txn-id')
		username = User.objects.get(username = request.user.username)
		status = Status.objects.get(name = 'Pending')
		usd_value = request.POST.get('usd_value')

		txn = PayTM(
			number = number,
			amount = amount,
			user_id = username,
			transaction_id = txn_id,
			status = status,
			usd = usd_value
		)

		txn.save()
		return HttpResponseRedirect('/dashboard/paytm-transactions')
	return render(request, 'dashboard/add-funds/paytm.html', {
		'balance': balance,
		'curr': curr
	})

@login_required
def paypal(request):
	curr = 'wallet'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	if request.method == 'POST':
		email_id = request.POST.get('email_id')
		amount = request.POST.get('amount')
		txn_id = request.POST.get('txn-id')
		username = User.objects.get(username = request.user.username)
		status = Status.objects.get(name = 'Pending')

		txn = Paypal(
			email = email_id,
			amount = amount,
			user_id = username,
			transaction_id = txn_id,
			status = status,
		)

		txn.save()
		return HttpResponseRedirect('/dashboard/paypal-transactions')
	else:
		return render(request, 'dashboard/add-funds/paypal.html', {
			'balance': balance,
			'curr': curr
		})

@login_required
def bitcoin(request):
	curr = 'wallet'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	if request.method == 'POST':
		address = request.POST.get('address')
		amount = request.POST.get('amount')
		txn_id = request.POST.get('txn-id')
		username = User.objects.get(username = request.user.username)
		status = Status.objects.get(name = 'Pending')
		usd_value = request.POST.get('usd_value')

		txn = Bitcoin(
			wallet_id = address,
			amount = amount,
			user_id = username,
			transaction_id = txn_id,
			status = status,
			usd = usd_value
		)

		txn.save()

		return HttpResponseRedirect('/dashboard/bitcoin-transactions')	
	else:
		return render(request, 'dashboard/add-funds/bitcoin.html', {
		'balance': balance,
		'curr': curr
	})

@login_required
def ethereum(request):
	curr = 'wallet'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	if request.method == 'POST':
		address = request.POST.get('address')
		amount = request.POST.get('amount')
		txn_id = request.POST.get('txn-id')
		username = User.objects.get(username = request.user.username)
		status = Status.objects.get(name = 'Pending')
		usd_value = request.POST.get('usd_value')

		txn = Ethereum(
			wallet_id = address,
			amount = amount,
			user_id = username,
			transaction_id = txn_id,
			status = status,
			usd = usd_value
		)

		txn.save()
		return HttpResponseRedirect('/dashboard/ethereum-transactions')
	return render(request, 'dashboard/add-funds/ethereum.html', {
		'balance': balance,
		'curr': curr
	})


@login_required
def orders(request):
	curr = 'orders'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	orders = Order.objects.filter(user_id = User.objects.get(username = request.user.username)).order_by('-created_at')
	return render(request, 'dashboard/pages/orders.html', {
		'curr': curr,
		'orders': orders,
		'balance': balance
	})


@login_required
def transactions(request):
	curr = 'transactions'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	return render(request, 'dashboard/pages/transactions.html', {
		'balance': balance,
		'curr': curr
	})


@login_required
def paypalTransactions(request):
	curr = 'transactions'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	transactions = Paypal.objects.filter(user_id = User.objects.get(username = request.user.username))
	return render(request, 'dashboard/transactions/paypal.html', {
		'transactions': transactions,
		'balance': balance,
		'curr': curr
	})

@login_required
def paytmTransactions(request):
	curr = 'transactions'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	transactions = PayTM.objects.filter(user_id = User.objects.get(username = request.user.username))
	return render(request, 'dashboard/transactions/paytm.html', {
		'transactions': transactions,
		'balance': balance,
		'curr': curr
	})

@login_required
def bitcoinTransactions(request):
	curr = 'transactions'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	transactions = Bitcoin.objects.filter(user_id = User.objects.get(username = request.user.username))
	return render(request, 'dashboard/transactions/bitcoin.html', {
		'transactions': transactions,
		'balance': balance,
		'curr': curr
	})

@login_required
def telegramMembers(request, slug):
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	return render(request, 'dashboard/pages/telegram-members.html', {})

@login_required
def members(request, slug):
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	members_list = Members.objects.get(slug = slug)
	group_name = members_list.group_name
	list_1 = members_list.members
	date = members_list.created_at

	return render(request, 'dashboard/pages/members.html', {
		"group_name": group_name,
		"list": list_1,
		"date": date
	})

@login_required
def ethereumTransactions(request):
	curr = 'transactions'
	balance = Profile.objects.get(user = User.objects.get(username = request.user.username)).balance
	if not Profile.objects.get(user = User.objects.get(username = request.user.username)).email_verified:
		return HttpResponseRedirect("/email-not-verified")
	transactions = Ethereum.objects.filter(user_id = User.objects.get(username = request.user.username))
	return render(request, 'dashboard/transactions/ethereum.html', {
		'transactions': transactions,
		'balance': balance,
		'curr': curr
	})
