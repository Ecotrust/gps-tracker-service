from django.http import HttpResponse
from reports.models import Report
import datetime
import pytz
import csv
from django.contrib.gis.geos import Point

def submit(request):

    if not request.GET.has_key('imei'):
        return HttpResponse("Expected additional parameters")

    imei = request.GET['imei']
    nmea_str = request.GET['rmc']
    nmea_list = nmea_str.split(",")

    #Sanav sentence is of type GPRMC with a couple extra attributes for voltage and report type
    #imei - first parameter before sentence, provides a unique id for the device
    #NMEA type - $GPRMC
    #UTC time - 095838.000 hhmmss.sss
    #Status - A
    #Lat - 2458.9733 ddmm.mmmm Degree Decimal Minute
    #Lat dir - N
    #Lon - 12125.6583 ddmm.mmmm Degree Decimal Minute
    #Lon dir - E
    #Speed knots - 0.41
    #Course - 79.21
    #UTC Date - 220905 ddmmyy
    #Mag. deviation - blank
    #Checksum - *30
    #Voltage - 3777mv
    #Report type - POLL

    rep_time = nmea_list[1]
    rep_lat = nmea_list[3]
    rep_lat_dir = nmea_list[4]
    rep_lon = nmea_list[5]
    rep_lon_dir = nmea_list[6]
    rep_date = nmea_list[9]

    r = Report()
    r.imei = imei
    r.nmea_type = nmea_list[0][1:]
    r.status = nmea_list[2]
    r.speed = nmea_list[7]
    r.course = nmea_list[8]
    r.voltage = nmea_list[12][0:-2]
    r.rep_type = nmea_list[13]
    r.nmea_sentence = nmea_str    

    #parse and build location
    lon_dd = float(rep_lon[:-7])+float(rep_lon[-7:])/60.0
    if rep_lon_dir == 'W':
        lon_dd *= -1
    lat_dd = float(rep_lat[:-7])+float(rep_lat[-7:])/60.0
    if rep_lat_dir == 'S':
        lat_dd *= -1
    r.loc = Point(lon_dd, lat_dd)

    #parse and build timestamp    
    year = int(rep_date[4:6])
    month = int(rep_date[2:4])
    day = int(rep_date[0:2])
    hour = int(rep_time[0:2])
    minute = int(rep_time[2:4])
    sec = int(rep_time[4:6])
    ms = int(rep_time[7:])
    r.timestamp = datetime.datetime(year, month, day, hour, minute, sec, ms)

    r.save()
    
    return HttpResponse("Report logged")


def export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)

    # Write heading line.
    writer.writerow(['imei', 'nmea_type', 'timestamp', 'status', 'lat', 'lng', 'speed', 'course', 'voltage', 'rep_type', 'nmea_sentence', 'notes', 'ak_time'])

    # Write each record to a line.
    for r in Report.objects.all():
        writer.writerow([r.imei, r.nmea_type, r.timestamp, r.status, r.loc.y, r.loc.x, r.speed, r.course, r.voltage, r.rep_type, r.nmea_sentence, r.notes, r.ak_time])

    return response

