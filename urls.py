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
    url(r'^changepassword/$', 'django.contrib.auth.views.password_change',
        name='changepassword',
        kwargs = {'post_change_redirect': 'registration:change_password_done'}),
    url(r'^change_password_done/$',
        'django.contrib.auth.views.password_change_done'),
    url(r'^register_user/$', views.register_user, name='register_user'),
    url(r'^resetpassword/$', password_reset, name='resetpassword'),
    url(r'^reset_password_done/$',
        'django.contrib.auth.views.password_reset_done'),

    url(r'^propose_lbw/$', views.propose_lbw, name='propose_lbw'),

    # ex: /lbw/5/
    url(r'^(?P<pk>\d+)/$', views.detail, name='detail'),

    # ex: /lbw/1/register/
    url(r'^(?P<lbw_id>\d+)/register/$', views.register, name='register'),
    # ex: /lbw/1/deregister/
    url(r'^(?P<lbw_id>\d+)/deregister/$', views.deregister, name='deregister'),
    # ex: /lbw/5/activities/
    url(r'^(?P<lbw_id>\d+)/activities/$', views.activities, name='activities'),
    # ex: /lbw/5/schedule/
    url(r'^(?P<pk>\d+)/schedule/$', views.Schedule, name='schedule'),
    # ex: /lbw/5/tshirts/
    url(r'^(?P<lbw_id>\d+)/tshirts/$', views.tshirts, name='tshirts'),
    # ex: /lbw/5/rides/
    url(r'^(?P<lbw_id>\d+)/rides/$', views.rides, name='rides'),
    # ex: /lbw/5/participants/
    url(r'^(?P<lbw_id>\d+)/participants/$', views.participants, name='participants'),


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
