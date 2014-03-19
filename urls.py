from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

from registration import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    # ex: /registration/propose_lbw/
    url(r'^propose_lbw/$', views.propose_lbw, name='propose_lbw'),

    # ex: /lbw/5/
    url(r'^(?P<pk>\d+)/$', views.detail, name='detail'),

    # ex: /registration/1/register/
    url(r'^(?P<lbw_id>\d+)/register/$', views.register, name='register'),
    # ex: /registration/1/deregister/
    url(r'^(?P<lbw_id>\d+)/deregister/$', views.deregister, name='deregister'),
    # ex: /registration/5/activities/
    url(r'^(?P<lbw_id>\d+)/activities/$', views.activities, name='activities'),
    # ex: /registration/5/schedule/
    url(r'^(?P<pk>\d+)/schedule/$', views.Schedule, name='schedule'),
    # ex: /registration/5/tshirts/
    url(r'^(?P<lbw_id>\d+)/tshirts/$', views.tshirts, name='tshirts'),
    # ex: /registration/5/rides/
    url(r'^(?P<lbw_id>\d+)/rides/$', views.rides, name='rides'),
    # ex: /registration/5/participants/
    url(r'^(?P<lbw_id>\d+)/participants/$', views.participants, name='participants'),
    # ex: /registration/1/update/
    url(r'^(?P<lbw_id>\d+)/update/$', views.update_lbw, name='update_lbw'),
    # ex: /registration/1/delete/
    url(r'^(?P<lbw_id>\d+)/delete_lbw/$', views.delete_lbw, name='delete_lbw'),


    # ex: /lbw/5/propose_activity/
    url(r'^(?P<lbw_id>\d+)/propose_activity/$', views.propose_activity, name='propose_activity'),
    # ex: /lbw/5/cancel_activity/
    url(r'^(?P<lbw_id>\d+)/cancel_activity/$', views.cancel_activity, name='cancel_activity'),

    # ex: /lbw/5/activity/1/
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/$', views.activity, name='activity'),
    # ex: /lbw/5/activity/1/register
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/register$', views.ActivityRegister, name='activity_register'),

    # ex: /lbw/5/message/1/
    url(r'^(?P<lbw_id>\d+)/message/(?P<message_id>\d+)$', views.message, name='message'),

    # ex: /message/delete
    url(r'^message/delete/(?P<message_id>\d+)$', views.DeleteMessage, name='delete_message'),
    # ex: /registration/message/save
    url(r'^message/save$', views.save_message, name='save_message'),

    # ex: /registration/5/userview/1
    url(r'^(?P<lbw_id>\d+)/userview/(?P<user_id>\d+)/$', views.lbwuserview, name='lbwuserview'),

    # ex: /registration/userview/1
    url(r'^userview/(?P<pk>\d+)/$', views.UserView.as_view(), name='userview'),


)
