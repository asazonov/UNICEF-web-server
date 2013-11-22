from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import Message, MobileUser

import pprint
import parser
import json
from geopy import geocoders, Point, distance
from datetime import datetime

POST = 'POST'
SOUTH_SUDAN = 'South Sudan'

MESSAGES_TO_SEND = []

def toDict(queryDict):
	data = dict(queryDict)
	for key in data:
		data[key] = data[key][0]
	return data

@csrf_exempt
def send(request):
    if request.method == "GET":
        if TO_SEND:
        	return HttpResponse(
        		json.dumps(MESSAGES_TO_SEND)
        	)


@csrf_exempt
def check(request):
    if request.method == "GET":
        return str(process())

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
        except MobileUser.DoesNotExistError:
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
		messages = Message.objects.filter(processed = False)
		if not messages.exists():
            return False
        
        all_users = MobileUser.objects.all()
        
        for message in messages:
            message.processed = True
            message.save()
            send_to = []

            message_location = Point(message.latitude, message.longitude)


            if message.latitude is "" and message.longitude is "":
                if(message.tag == "danger"):
                    send_to = list(all_users)
                    #do something with send_to


            elif message.tag == "danger":
                for user in all_users:
                    user_location = Point(user.latitude, user.longitude)
                    if within_distance(user_location,message_location,15):
                        send_to.append(user.mobile)

            elif message.tag == "local":
                for user in all_users:
                    user_location = Point(user.latitude, user.longitude)
                    if within_distance(user_location,message_location,3):
                        send_to.append(user.mobile)

            elif message.tag == "teachers" and message.sender.user_type = "teacher":
                teachers = MobileUser.objects.filter(user_type = "teacher")
                for teacher in teachers:
                    user_location = Point(teacher.latitude, teacher.longitude)
                    if within_distance(user_location,message_location, 10):
                        send_to.append(teacher.mobile)

            elif message.tag == "students" and message.sender.user_type = "teacher":
                students = MobileUser.objects.filter(user_type = "student")
                for student in students:
                    user_location = Point(student.latitude, student.longitude)
                    if within_distance(user_location,message_location, 10):
                        send_to.append(student.mobile)

            if len(send_to) > 0:
                msg = {'numbers': send_to, 'message': message.message_body + " @" + message.location}
                MESSAGES_TO_SEND.append(msg)


def within_distance(p1, p2, d):
    if distance.distance(p1,p2).kilometers <= d:
        return True
    else False

