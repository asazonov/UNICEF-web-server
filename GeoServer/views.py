from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

import json


@csrf_exempt
def send(request):

    if request.method == 'POST':
        data = request.POST['data']
        print data


@csrf_exempt
def recieve(request):
    """The methods for the registration of a multiple user"""
    if request.method == 'POST':

        encoded = request.POST['data']

        decoded = encoded
        try:
            decoded = json.loads(encoded)
        except ValueError:
            return HttpResponse('Not json')

        finalList = []

        for user in decoded:
            a = User.create(
                name = user['name'],
                password = user['password'],
                mobile_number = user['mobile_number'],
                user_type = user['user_type']
            )
            a.save()
            finalList.append((a.userid, a.name))

        return HttpResponse(str(finalList))

    return HttpResponse('404, man')
