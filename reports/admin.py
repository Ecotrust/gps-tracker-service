from django.contrib import admin
from models import *

class ReportAdmin(admin.ModelAdmin):
    list_display = ('imei', 'timestamp', 'ak_time', 'status', 'rep_type', 'loc', 'speed', 'course', 'voltage')

admin.site.register(Report, ReportAdmin)