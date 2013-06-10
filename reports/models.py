from django.contrib.gis.db import models
import datetime

class Report(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    imei = models.BigIntegerField()
    nmea_type = models.CharField(max_length=4)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=1)
    loc = models.PointField(srid=4326)
    speed = models.FloatField()
    course = models.FloatField()
    voltage = models.IntegerField()
    rep_type = models.TextField()
    nmea_sentence = models.TextField()
    objects = models.GeoManager()

    @property
    def ak_time(self):
        return self.timestamp-datetime.timedelta(hours=8)

    #NMEA type - $GPRMC
    #UTC time - 095838.000 hhmmss.sss
    #Status - A
    #Lat - 2458.9733 ddmm.mmmm Degree Decimal Minute
    #Lat dir - N
    #Lon - 12125.6583 ddmm.mmmm Degree Decimal Minute
    #Lon dir - E
    #Speed knots - 0.41
    #Course - 79.21
    #UTC Date - 220905
    #Mag. deviation - blank
    #Checksum - *30
    #Voltage - 3777mv
    #Report type - POLL