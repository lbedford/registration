"""URLs for LBWs."""
from django.conf.urls import patterns, url

from registration import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    # ex: /registration/propose_lbw/
    url(r'^propose_lbw/$', views.propose_lbw, name='propose_lbw'),

    # ex: /lbw/5/
    url(r'^(?P<lbw_id>\d+)/$', views.detail, name='detail'),

    # ex: /registration/1/register/
    url(r'^(?P<lbw_id>\d+)/register/$', views.register, name='register'),
    # ex: /registration/1/deregister/
    url(r'^(?P<lbw_id>\d+)/deregister/$', views.deregister, name='deregister'),
    # ex: /registration/5/activities/
    url(r'^(?P<lbw_id>\d+)/activities/$', views.activities, name='activities'),
    # ex: /registration/5/schedule/
    url(r'^(?P<lbw_id>\d+)/schedule/$', views.schedule, name='schedule'),
    # ex: /registration/5/tshirts/
    url(r'^(?P<lbw_id>\d+)/tshirts/$', views.tshirts, name='tshirts'),
    # ex: /registration/5/rides/
    url(r'^(?P<lbw_id>\d+)/rides/$', views.rides, name='rides'),
    # ex: /registration/5/participants/
    url(r'^(?P<lbw_id>\d+)/participants/$', views.participants,
        name='participants'),
    # ex: /registration/1/update/
    url(r'^(?P<lbw_id>\d+)/update/$', views.update_lbw, name='update_lbw'),
    # ex: /registration/1/delete/
    url(r'^(?P<lbw_id>\d+)/delete_lbw/$', views.delete_lbw, name='delete_lbw'),


    # ex: /lbw/5/propose_activity/
    url(r'^(?P<lbw_id>\d+)/propose_activity/$', views.propose_activity,
        name='propose_activity'),
    # ex: /lbw/5/cancel_activity/
    url(r'^(?P<lbw_id>\d+)/cancel_activity/$', views.cancel_activity,
        name='cancel_activity'),

    # ex: /lbw/5/activity/1/
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/$', views.activity,
        name='activity'),
    # ex: /lbw/5/activity/1/register
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/register$',
        views.activity_register, name='activity_register'),
    # ex: /lbw/5/activity/1/write_message
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/write_message$',
        views.write_activity_message, name='write_activity_message'),

    # ex: /lbw/5/message/1/
    url(r'^(?P<lbw_id>\d+)/write_message/$', views.write_lbw_message,
        name='write_lbw_message'),
    # ex: /lbw/5/message/1/
    url(r'^(?P<lbw_id>\d+)/message/(?P<message_id>\d+)$', views.message,
        name='message'),

    # ex: /message/delete
    url(r'^message/delete/(?P<message_id>\d+)$', views.delete_message,
        name='delete_message'),
    # ex: /registration/message/save
    url(r'^message/save$', views.save_message, name='save_message'),
)
