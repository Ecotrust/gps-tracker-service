from django.contrib.gis import admin
from models import *

class ReportAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'imei', 'timestamp', 'ak_time', 'status', 'rep_type', 'loc', 'speed', 'course', 'voltage')
    ordering = ('timestamp','id')
admin.site.register(Report, ReportAdmin)