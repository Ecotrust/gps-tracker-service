from django.conf.urls import patterns, url
from reports import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^submit$', views.submit, name='submit')
)