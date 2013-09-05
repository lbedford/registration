from django.conf.urls import patterns, url

from registration import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /lbw/5/
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /lbw/5/register/
    url(r'^(?P<lbw_id>\d+)/register/$', views.register, name='register'),
)
