from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import pprint

import json

def toDict(queryDict):
	data = dict(queryDict)
	for key in data:
		data[key] = data[key][0]
	return data

@csrf_exempt
def send(request):

    if request.method == 'POST':
        data = request.POST['data']
        print data


@csrf_exempt
def check(request):

    if request.method == 'POST':
        data = request.POST['data']
        print data


@csrf_exempt
def receive(request):
    if request.method == 'POST':
        data = toDict(request.POST)
        pprint.pprint(data)
        print data
    return HttpResponse(200)

