from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import Message, MobileUser

import pprint
import parser
from geopy import geocoders
from datetime import datetime

POST = 'POST'
SOUTH_SUDAN = 'South Sudan'

def toDict(queryDict):
	data = dict(queryDict)
	for key in data:
		data[key] = data[key][0]
	return data

@csrf_exempt
def send(request):
    if request.method == POST:
        data = request.POST['data']
        print data


@csrf_exempt
def check(request):
    if request.method == POST:
        data = request.POST['data']
        print data


@csrf_exempt
def receive(request):
    if request.method == POST:
        data = toDict(request.POST)
        pm = parser.parseMessage(data["sms_string"])
        phone_number = str(data["phone_number"])

        mobile_user = MobileUser.objects.get(mobile = phone_number)
        if mobile_user is None:
            return HttpResponse(401)

        message = pm.getMessage()
        tag = pm.getTag()
        raw_location = pm.getLocationDescriptor()
        geocoder = geocoders.GoogleV3()
        location_defined = True
        lat = None
        lng = None
        place = None

        try:
            place, (lat, lng) = geocoder.geocode(
                raw_location + ', ' + SOUTH_SUDAN
            )
            place_country = place.split(', ')[-1]
            if place_country != unicode(SOUTH_SUDAN):
                raise TypeError()
            new_message = Message(
                raw = data,
                tag = tag,
                message_body = message,
                message_time = datetime.now(),
                location = place,
                location_defined = location_defined,
                latitude = lat,
                longitude = lng
            )
            mobile_user.location = place
            mobile_user.longitude = lng
            mobile_user.latitude = lat
            mobile_user.location_updated = new_message.message_time
        except TypeError:
            location_defined = False
            place = raw_location
            new_message = Message(
                raw = data,
                tag = tag,
                message_body = message,
                message_time = datetime.now(),
                location = place,
                location_defined = location_defined
            )


        new_message.save()
        pprint.pprint(pm)
    return HttpResponse(200)

