from django.conf.urls import url
from . import views
from ADTAA.views import *

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    # ex: /ADTAA/reg/
    url(r'^reg/$', Register.as_view(), name='reg'),

    # ex: /ADTAA/password
    url(r'^password/$', PasswordPage.as_view(), name='password'),

    # ex: /ADTAA/password2
    url(r'^password2/$', PasswordPage2.as_view(), name='password2'),

    # ex: /ADTAA/rootHome/
    url(r'^rootHome/$', views.root_home_page, name='rootHome'),

    # ex: /ADTAA/adminHome/
    url(r'^adminHome/$', views.admin_home_page, name='adminHome'),

    # ex: /ADTAA/schedulerHome/
    url(r'^schedulerHome/$', views.scheduler_home_page, name='schedulerHome'),

    # ex: /ADTAA/instrSetup/
    url(r'^instrSetup/$', views.setup_instructor, name='instrSetup'),

    # ex: /ADTAA/classSetup/
    url(r'^classSetup/$', views.setup_classes, name='classSetup')



]
