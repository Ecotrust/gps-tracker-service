from django.template.defaultfilters import date
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
import datetime

from models import Report
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

class ReportResource(ModelResource):

    class Meta:
        queryset = Report.objects.all()
        resource_name = 'report'        
        authentication = Authentication()
        authorization = Authorization()

    #Require user to be authenticated already rather than using a key
    def obj_create(self, bundle, *args, **kwargs):
        try:
            bundle = super(ReportResource, self).obj_create(bundle, *args, **kwargs)
            if bundle.request.user and bundle.request.user.is_authenticated():
                bundle.obj.user = bundle.request.user
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest('IntegrityError')
        return bundle        

    def dehydrate(self, bundle):
        # format the timestamp to include timezone as tastypie doesn't
        bundle.data['timestamp'] = date(bundle.obj.timestamp, 'c')
        time = bundle.obj.timestamp+datetime.timedelta(hours=8)
        bundle.data['ak_time'] = datetime.datetime(time.year+2000, time.month, time.day, time.hour, time.minute, time.second).strftime("%m/%d/%y %H:%M")
        return bundle        