from django.contrib import admin
from django.urls import path
from chart import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ticket-class/3/',
         views.ticket_class_view, name='ticket_class_view'),
    path('covid1/',
         views.covid1, name='covid1'),
    path('admin/', admin.site.urls),
]