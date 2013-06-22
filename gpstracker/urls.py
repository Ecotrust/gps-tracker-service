from django.conf.urls import patterns, include, url
from reports.api import ReportResource
from tastypie.api import Api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ReportResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^report/', include('reports.urls')),
    url(r'^admin/', include(admin.site.urls))    
)
