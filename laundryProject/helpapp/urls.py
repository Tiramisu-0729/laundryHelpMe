from django.urls import path
from . import views

app_name = 'helpapp'

urlpatterns = [
    path('', views.helpapp, name='helpapp'),
    path('nologin', views.nologin, name='nologin'),
    path('home', views.home, name='home'),
    path('washing_machine', views.washing_machine, name='washing_machine'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('timeline', views.timeline, name='timeline'),
    path('register', views.register, name='register'),
    path("user",views.user, name="user"),
    path("judge",views.judge, name="judge"),
    path("cabinet_form",views.cabinet_form, name="cabinet_form"),
    path("cabinet_add",views.cabinet_add, name="cabinet_add"),
    path("cabinet_detail/<int:pk>/",views.cabinet_detail, name="cabinet_detail"),
]