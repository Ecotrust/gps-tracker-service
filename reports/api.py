from django.contrib.auth.models import User
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource

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