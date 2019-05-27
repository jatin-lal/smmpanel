from django.contrib import admin
from django.urls import path, include

from public import views as public
from userauth import views as auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', public.home, name='home'),
    path('privacy-policy', public.privacyPolicy, name='privacy-policy'),
    path('terms-and-conditions', public.tandc, name='tandc'),
    path('disclaimer', public.disclaimer, name='disclaimer'),
    path('about-us', public.aboutUs, name='about-us'),
    path('login', auth.login, name='login'),
    path('register', auth.register, name='register'),
    path('logout', auth.logout, name='logout'),
    path('api/', include('api.urls')),
    path('dashboard/', include('dashboard.urls')),
]

handler404 = 'public.views.handler404'
handler500 = 'public.views.handler500'