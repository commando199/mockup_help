"""eRezept URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from django.conf.urls import include
from django.contrib import admin
from accounts import views
from django.conf.urls import url
from accounts.views import showroute,showmap,showroute1


urlpatterns = [
    path('<str:lat1>,<str:long1>,<str:lat2>,<str:long2>', showroute, name='showroute'),
    path('map_all/', showroute, name='showroute'),
    path('detailed_past_shippings/', views.detailed_past_shippings, name='detailed_past_shippings'),
    path('kpis/', views.kpis, name='kpis'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('optimize/', views.optimize, name='optimize'),
    path('admin/logout/', views.signout),
    path('admin-page/', views.admin_page, name="admin-page"),
    path('', views.home, name="arzt-home"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('liste_shippings/', views.patientenauswahl, name='patientenauswahl'),
    path('medikamentauswahl/', views.past_shippings, name='medikamentauswahl'),
    path('list/', views.list, name="list"),
    path('praxis/', views.praxis_home, name='praxis-home'),
]
