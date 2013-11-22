from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import Message, MobileUser

import pprint
import parser
import json
from geopy import geocoders
from datetime import datetime
import time

POST = 'POST'
SOUTH_SUDAN = 'South Sudan'
TO_SEND = True

def toDict(queryDict):
	data = dict(queryDict)
	for key in data:
		data[key] = data[key][0]
	return data

@csrf_exempt
def getMessages(request):
    """
    Gets all of the messages from the database and converts them
    to JSON with the associated metadata
    """

    messages = Message.objects.all()
    if not messages.exists:
        return HttpResponse("{}")

    #print messages
    if request.method == "GET":
        retList = list()
        for message in messages:
            retList.append({
                "tag": message.tag,
                "location": message.location,
                "latitude": message.latitude,
                "longitude": message.longitude,
                "time_stamp": time.mktime(message.message_time.timetuple()),
                "body": message.message_body,
                "sender_name": message.sender.name,
                "sender_mobile": message.sender.mobile,
                "processed": message.processed
            })

        return HttpResponse(json.dumps(retList))

@csrf_exempt
def getUsers(request):
    users = MobileUser.objects.all()
    if not users.exists:
        return HttpResponse("{}")

    if request.method == "GET":
        retList = list()
        for user in users:
            retList.append({
                "mobile": user.mobile,
                "name": user.name,
                "user_type": user.user_type,
                "location": user.location,
                "longitude": user.longitude,
                "latitude": user.latitude,
                "last_updated": time.mktime(
                    user.location_updated.timetuple()
                )
            })

        return HttpResponse(json.dumps(retList))

@csrf_exempt
def send(request):
    if request.method == "GET":
        if TO_SEND:
        	return HttpResponse(
        		json.dumps({
        			'numbers': ["+447926677745", "+447582733198"],
        			'message': "balls and tits with fuck"
        		})
        	)


@csrf_exempt
def check(request):
    if request.method == "GET":
        return HttpResponse(str(not TO_SEND).lower())
    	# if process():
     # 		return str(True)
     # 	else return str(False)

@csrf_exempt
def receive(request):
    if request.method == POST:
        data = toDict(request.POST)
        pm = parser.parseMessage(data["sms_string"])

        if pm is None:
            return HttpResponse("Not working bro")

        phone_number = str(data["phone_number"])

        try:
            mobile_user = MobileUser.objects.get(mobile = phone_number)
        except Exception as e:
            print "Exception:", e
            return HttpResponse("Dude, are you a rebel?")

        message = pm.getMessage()
        tag = pm.getTag()
        raw_location = pm.getLocationDescriptor()
        geocoder = geocoders.GoogleV3()
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
            	processed = False,
                raw = data,
                sender = mobile_user,
                tag = tag,
                message_body = message,
                message_time = datetime.now(),
                location = place,
                location_defined = True,
                latitude = lat,
                longitude = lng
            )
            mobile_user.location = place
            mobile_user.longitude = lng
            mobile_user.latitude = lat
            mobile_user.location_updated = new_message.message_time
            mobile_user.save()
        except TypeError:
            place = raw_location
            new_message = Message(
            	processed = False,
                raw = data,
                tag = tag,
                message_body = message,
                message_time = datetime.now(),
                location = place,
                location_defined = False
            )

        new_message.save()
        print pm
    return HttpResponse(200)

def process():
	try:
		message = Message.objects.filter(processed = False)
		return True
	except Message.DoesNotExistError:
	    return False
