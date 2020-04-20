from django.conf.urls import url
from . import views
from ADTAA.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),

    # ex: /ADTAA/reg/
    url(r'^reg/$', Register.as_view(), name='reg'),

    # ex: /ADTAA/password/
    url(r'^password/$', ChangePassword.as_view(), name='password'),

    # ex: /ADTAA/rootHome/
    url(r'^rootHome/$', views.root_home_page, name='rootHome'),

    # ex: /ADTAA/adminHome/
    url(r'^adminHome/$', views.admin_home_page, name='adminHome'),

    # ex: /ADTAA/schedulerHome/
    url(r'^schedulerHome/$', views.scheduler_home_page, name='schedulerHome'),

    # ex: /ADTAA/instrSetup/
    url(r'^instrSetup/$', login_required(AddInstructor.as_view(), 'instrSetup')),

    # ex: /ADTAA/classSetup/
    url(r'^classSetup/$', login_required(AddClass.as_view(), 'classSetup')),

    # ex: /ADTAA/editSolutions/
    url(r'^editSolutions/$', views.edit_solutions, name='editSolutions'),

    # ex: /ADTAA/generateSolutions/
    url(r'^generateSolutions/$', GenerateSolutions.as_view(), name='generateSolutions'),

    # ex: /ADTAA/adminNav/
    url(r'^adminNav/$', views.admin_nav, name='adminNav'),

    # ex: /ADTAA/rootNav/
    url(r'^rootNav/$', views.root_nav, name='rootNav'),

    # ex: /ADTAA/schedulerNav/
    url(r'^schedulerNav/$', views.scheduler_nav, name='schedulerNav'),

    url(r'^logout/$', views.logout, name='logout'),

    url(r'^regRequests/$', views.regRequests, name='regRequests'),

    url(r'^userPage/$', views.user_page, name='userPage'),

    path('editInstr/<str:pk>/', views.edit_instructor, name='editInstr'),

    path('editClass/<str:pk>/', views.edit_class, name='editClass'),

    path('instructorProfile/<str:pk>/', views.instructor_profile, name='instructorProfile'),

    path('classProfile/<str:pk>/', views.class_profile, name='classProfile'),

]
