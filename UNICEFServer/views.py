from django.shortcuts import render


def index(request):
    print "hi"
    return render(request, "index.html")
