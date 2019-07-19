"""URLs for LBWs."""
from django.conf.urls import url
from django.urls import path

from registration import views

app_name = 'registration'

urlpatterns = [
    path('', views.index, name='index'),

    # example: /propose_lbw/
    path('propose_lbw/', views.propose_lbw, name='propose_lbw'),

    # example: /5/
    path('<int:lbw_id>/', views.detail, name='detail'),

    # example: /1/accommodation/
    path('<int:lbw_id>/accommodation/', views.accommodation, name='accommodation'),
    # example: /1/register/
    path('<int:lbw_id>/register/', views.register, name='register'),
    # example: /1/deregister/
    path('<int:lbw_id>/deregister/', views.deregister, name='deregister'),
    # example: /5/activities/
    path('<int:lbw_id>/activities/', views.activities, name='activities'),
    # example: /5/propose_activity/
    path('<int:lbw_id>/propose_activity/', views.propose_activity, name='propose_activity'),
    # example: /5/schedule/
    path('<int:lbw_id>/schedule/', views.schedule, name='schedule'),
    # example: /5/tshirts/
    path('<int:lbw_id>/tshirts/', views.tshirts, name='tshirts'),
    # example: /5/rides/
    path('<int:lbw_id>/rides/', views.rides, name='rides'),
    # example: /5/participants/
    path('<int:lbw_id>/participants/', views.participants, name='participants'),
    # example: /1/update/
    path('<int:lbw_id>/update/', views.update_lbw, name='update_lbw'),
    # example: /1/delete/
    path('<int:lbw_id>/delete/', views.delete_lbw, name='delete_lbw'),
    # example: /5/details.json
    path('<int:lbw_id>/details.json', views.details_json, name='details_json'),

    # example: /activity/1/
    path('<int:lbw_id>/activity/<int:activity_id>/', views.activity,
        name='activity'),
    # example: /activity/1/register
    path('<int:lbw_id>/activity/<int:activity_id>/register',
        views.activity_register, name='activity_register'),
    # example: /activity/6/update
    path('<int:lbw_id>/activity/<int:activity_id>/update', views.update_activity,
        name='update_activity'),
    # example: /activity/6/cancel
    path('<int:lbw_id>/activity/<int:activity_id>/cancel', views.cancel_activity,
        name='cancel_activity'),
    # example: /activity/1/write_message
    path('<int:lbw_id>/activity/<int:activity_id>/write_message',
        views.write_activity_message, name='write_activity_message'),
    # example: /activity/1/attachment
    path('<int:lbw_id>/activity/<int:activity_id>/attachment',
        views.activity_attachment, name='activity_attachment'),

    # example: /5/message/1/
    path('<int:lbw_id>/write_message/', views.write_lbw_message,
        name='write_lbw_message'),

    # example: /message/reply/1
    path('<int:lbw_id>/message/reply/<int:message_id>', views.reply_message,
        name='reply_message'),

    # example: /message/delete
    path('<int:lbw_id>/message/delete/<int:message_id>', views.delete_message,
        name='delete_message'),
    # example: /message/save
    path('<int:lbw_id>/message/save', views.save_message, name='save_message'),
]
