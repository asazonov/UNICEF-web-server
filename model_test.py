from GeoServer.models import MobileUser, Message
import datetime

Message.objects.create(location ="1 Canary Wharf", processed=True)
MobileUser.objects.create(name ="Charles Wu", location_updated=datetime.datetime.now() )
