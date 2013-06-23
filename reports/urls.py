from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from reports import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^submit$', views.submit, name='submit'),
    (r'^map/', TemplateView.as_view(template_name="map.html")),
)