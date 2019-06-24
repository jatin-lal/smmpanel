from django.db import models
from django.contrib.auth.models import User

class Bitcoin(models.Model):
	id = models.AutoField(primary_key = True)
	wallet_id = models.CharField(max_length = 200)
	amount = models.DecimalField(default = 0, decimal_places = 12, max_digits = 20)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	transaction_id = models.CharField(max_length = 200)
	status = models.ForeignKey('Status', on_delete=models.CASCADE)
	remark = models.CharField(max_length = 5000, default = "", blank=True)
	usd = models.DecimalField(default = 0, decimal_places = 12, max_digits = 20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.wallet_id + " : " + str(self.amount) + " BTC"

class Ethereum(models.Model):
	id = models.AutoField(primary_key = True)
	wallet_id = models.CharField(max_length = 200)
	amount = models.DecimalField(default = 0, decimal_places = 12, max_digits = 20)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	transaction_id = models.CharField(max_length = 200)
	status = models.ForeignKey('Status', on_delete=models.CASCADE)
	remark = models.CharField(max_length = 5000, default = "", blank=True)
	usd = models.DecimalField(default = 0, decimal_places = 12, max_digits = 20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.wallet_id + " : " + str(self.amount) + " ETH"

class Paypal(models.Model):
	id = models.AutoField(primary_key = True)
	email = models.CharField(max_length = 200)
	amount = models.DecimalField(default = 0, decimal_places = 2, max_digits = 20)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	transaction_id = models.CharField(max_length = 200)
	status = models.ForeignKey('Status', on_delete=models.CASCADE)
	remark = models.CharField(max_length = 5000, default = "", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.email + " : " + str(self.amount) + " USD"

class Upi(models.Model):
	id = models.AutoField(primary_key = True)
	number = models.CharField(max_length = 200)
	amount = models.DecimalField(default = 0, decimal_places = 2, max_digits = 20)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	transaction_id = models.CharField(max_length = 200)
	status = models.ForeignKey('Status', on_delete=models.CASCADE)
	remark = models.CharField(max_length = 5000, default = "", blank=True)
	usd = models.DecimalField(default = 0, decimal_places = 12, max_digits = 20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.number + " : " + str(self.amount) + " INR"

class Status(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 500)

	def __str__(self):
		return self.name

class OrderStatus(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 500)

	def __str__(self):
		return self.name

class Order(models.Model):
	id = models.AutoField(primary_key = True)
	service_name = models.CharField(max_length = 300)
	link = models.CharField(max_length = 2048)
	quantity = models.IntegerField(default = 0)
	amount = models.DecimalField(default = 0, decimal_places = 2, max_digits = 20)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
	remark = models.CharField(max_length = 5000, blank=True)
	generate_url = models.FileField(blank = True, default='')
	slug = models.CharField(max_length = 256, default = "", blank=True)
	created_at = models.DateTimeField(auto_now_add=True, editable=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.user_id.username) + " : " + self.service_name + " : " + str(self.quantity) + " : " + self.link

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	balance = models.DecimalField(max_digits=10, decimal_places=5)
	spent = models.DecimalField(max_digits=10, decimal_places=5, default = 0)
	verify_email_slug = models.CharField(max_length = 200)
	email = models.EmailField(max_length=254)
	email_verified = models.BooleanField(default = False)

	def __str__(self):
		return self.user.username
