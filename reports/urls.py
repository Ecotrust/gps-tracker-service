from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^submit$', 'reports.views.submit', name='submit'),
    (r'^map/', login_required(TemplateView.as_view(template_name="map.html")))
)