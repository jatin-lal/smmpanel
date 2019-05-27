from django.contrib import admin

from .models import Bitcoin
from .models import Ethereum
from .models import Paypal
from .models import PayTM
from .models import Status
from .models import OrderStatus
from .models import Order
from .models import Profile

admin.site.register(Bitcoin)
admin.site.register(Ethereum)
admin.site.register(Paypal)
admin.site.register(PayTM)
admin.site.register(Status)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(Profile)
