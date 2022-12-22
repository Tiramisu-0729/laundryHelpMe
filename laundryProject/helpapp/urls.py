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
    path("user/",views.user, name="user"),
    path("judge",views.judge, name="judge"),
    path("judge_result",views.judge_result, name="judge_result"),
    path("cabinet_judge",views.cabinet_judge, name="cabinet_judge"),
    path("cabinet_form",views.cabinet_form, name="cabinet_form"),
    path("cabinet_add",views.cabinet_add, name="cabinet_add"),
    path("cabinet_detail/<int:pk>/",views.cabinet_detail, name="cabinet_detail"),
    path("washer_add",views.washer_add, name="washer_add"),
    path("washer_add_redirect",views.washer_add_redirect, name="washer_add_redirect"),
    path("washer_judge",views.washer_judge, name="washer_judge"),
    path("washer_complete",views.washer_complete, name="washer_complete"),
    path("washers_delete",views.washers_delete, name="washers_delete"),
    path("washer_clear",views.washer_clear, name="washer_clear"),
    path("laundry_tag_check",views.laundry_tag_check, name="laundry_tag_check"),
    path("cabinet_delete/<int:pk>/",views.cabinet_delete, name="cabinet_delete"),
    path("cabinets_delete",views.cabinets_delete, name="cabinets_delete"),
    path("test",views.testYolo, name="test"),
    path("washer_log_add",views.washer_log_add, name="washer_log_add"),
    path("washer_log",views.washer_log, name="washer_log"),
    path("washer_log_detail/<int:pk>/",views.washer_log_detail, name="washer_log_detail"),
    

]