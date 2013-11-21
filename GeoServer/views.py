from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

import json


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
        data = request.POST
        print data
