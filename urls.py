"""URLs for LBWs."""
from django.conf.urls import url

from registration import views

app_name = 'registration'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # example: /propose_lbw/
    url(r'^propose_lbw/$', views.propose_lbw, name='propose_lbw'),

    # example: /5/
    url(r'^(?P<lbw_id>\d+)/$', views.detail, name='detail'),

    # example: /1/accommodation/
    url(r'^(?P<lbw_id>\d+)/accommodation/$', views.accommodation, name='accommodation'),
    # example: /1/register/
    url(r'^(?P<lbw_id>\d+)/register/$', views.register, name='register'),
    # example: /1/deregister/
    url(r'^(?P<lbw_id>\d+)/deregister/$', views.deregister, name='deregister'),
    # example: /5/activities/
    url(r'^(?P<lbw_id>\d+)/activities/$', views.activities, name='activities'),
    # example: /5/propose_activity/
    url(r'^(?P<lbw_id>\d+)/propose_activity/$', views.propose_activity, name='propose_activity'),
    # example: /5/schedule/
    url(r'^(?P<lbw_id>\d+)/schedule/$', views.schedule, name='schedule'),
    # example: /5/tshirts/
    url(r'^(?P<lbw_id>\d+)/tshirts/$', views.tshirts, name='tshirts'),
    # example: /5/rides/
    url(r'^(?P<lbw_id>\d+)/rides/$', views.rides, name='rides'),
    # example: /5/participants/
    url(r'^(?P<lbw_id>\d+)/participants/$', views.participants,
        name='participants'),
    # example: /1/update/
    url(r'^(?P<lbw_id>\d+)/update/$', views.update_lbw, name='update_lbw'),
    # example: /1/delete/
    url(r'^(?P<lbw_id>\d+)/delete/$', views.delete_lbw, name='delete_lbw'),
    # example: /5/details.json
    url(r'^(?P<lbw_id>\d+)/details.json$', views.details_json,
        name='details_json'),


    # example: /activity/1/
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/$', views.activity,
        name='activity'),
    # example: /activity/1/register
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/register$',
        views.activity_register, name='activity_register'),
    # example: /activity/6/update
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/update$', views.update_activity,
        name='update_activity'),
    # example: /activity/6/cancel
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/cancel$', views.cancel_activity,
        name='cancel_activity'),
    # example: /activity/1/write_message
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/write_message$',
        views.write_activity_message, name='write_activity_message'),
    # example: /activity/1/attachment
    url(r'^(?P<lbw_id>\d+)/activity/(?P<activity_id>\d+)/attachment$',
        views.activity_attachment, name='activity_attachment'),

    # example: /5/message/1/
    url(r'^(?P<lbw_id>\d+)/write_message/$', views.write_lbw_message,
        name='write_lbw_message'),

    # example: /message/reply/1
    url(r'^(?P<lbw_id>\d+)/message/reply/(?P<message_id>\d+)$', views.reply_message,
        name='reply_message'),

    # example: /message/delete
    url(r'^(?P<lbw_id>\d+)/message/delete/(?P<message_id>\d+)$', views.delete_message,
        name='delete_message'),
    # example: /message/save
    url(r'^(?P<lbw_id>\d+)/message/save$', views.save_message, name='save_message'),
]
