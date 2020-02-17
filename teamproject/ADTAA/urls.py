from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /ADTAA/reg/
    url(r'^reg/$', views.reg_page, name='reg'),

    # ex: /ADTAA/password
    url(r'^password/$', views.password_page, name='password'),

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
