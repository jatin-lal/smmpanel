from django.urls import path

from dashboard import views as dashboard

urlpatterns = [
    path('', dashboard.home, name='dashboard-home'),
    path('new-order', dashboard.newOrder, name='new-order'),
    path('orders', dashboard.orders, name='orders'),
    path('wallet', dashboard.wallet, name='wallet'),
    path('telegram-services', dashboard.telegram, name='telegram-services'),
    path('website-services', dashboard.website, name='website-services'),
    path('ico-services', dashboard.ico, name='ico-services'),
    path('press-release-services', dashboard.press, name='press-release-services'),

    path('add-funds-paytm', dashboard.paytm, name='add-paytm'),
    path('add-funds-paypal', dashboard.paypal, name='add-paypal'),
    path('add-funds-bitcoin', dashboard.bitcoin, name='add-bitcoin'),
    path('add-funds-ethereum', dashboard.ethereum, name='add-ethereum'),

    path('transactions', dashboard.transactions, name='transactions'),

    path('paypal-transactions', dashboard.paypalTransactions, name="paypal-transactions"),
    path('paytm-transactions', dashboard.paytmTransactions, name="paytm-transactions"),
    path('bitcoin-transactions', dashboard.bitcoinTransactions, name="bitcoin-transactions"),
    path('ethereum-transactions', dashboard.ethereumTransactions, name="ethereum-transactions"),
]
