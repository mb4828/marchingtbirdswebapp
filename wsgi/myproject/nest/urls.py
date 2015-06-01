from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from nest import views

urlpatterns = patterns('',
    url(r'^$', 'nest.views.nest_home', name='nest'),
    url(r'^profile/$', 'nest.views.profile', name='profile'),
    #url(r'^uniform/$', 'nest.views.uniform', name='uniform'),
    url(r'^change_password/$', 'nest.views.password_change', name='changepass'),
    url(r'^register/$', 'nest.views.register', name='register'),
    url(r'^login/$', 'nest.views.user_login', name='login'),
    url(r'^logout/$', 'nest.views.user_logout', name='logout'),
)
