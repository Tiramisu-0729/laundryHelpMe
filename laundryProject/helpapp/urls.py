from django.urls import path
from . import views

app_name = 'helpapp'

urlpatterns = [
    path('', views.helpapp, name='helpapp'),
    path('nologin', views.nologin, name='nologin'),
    path('home', views.home, name='home'),
    path('washer', views.washer, name='washer'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('timeline', views.timeline, name='timeline'),
    path('register', views.register, name='register'),
    path("user",views.user, name="user"),
    path("judge",views.judge, name="judge"),
    path("judge_result",views.judge_result, name="judge_result"),
    path("cabinet_form",views.cabinet_form, name="cabinet_form"),
    path("cabinet_add",views.cabinet_add, name="cabinet_add"),
    path("cabinet_detail/<int:pk>/",views.cabinet_detail, name="cabinet_detail"),
    path("laundry_tag_check",views.laundry_tag_check, name="laundry_tag_check"),
]