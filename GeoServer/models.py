from django.db import models

class MobileUser(models.Model):
    mobile = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    longitude = models.CharField(max_length=15)
    latitude = models.CharField(max_length=15)
    location_updated = models.DateTimeField()


    # def __str__(self):
    #     return (
    #         "name: {} mobile: {} " +
    #         "user_type: {} location: {}".format(
    #             name, mobile,
    #             user_type, location
    #         )
    #     )

class Message(models.Model):
    processed = models.BooleanField()
    sender = models.ForeignKey(MobileUser)
    raw = models.CharField(max_length=500)
    tag = models.CharField(max_length=10)
    recipient = models.CharField(max_length=20)
    body = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    location_defined = models.BooleanField()
    longitude = models.CharField(max_length=15)
    latitude = models.CharField(max_length=15)

    def __str__(self):
        return (
            "raw: " + self.raw + "\n" +
            "tag: " + self.tag + "\n" +
            "recipient: " + self.recipient + "\n" +
            "location: " + self.location + "\n" +
            "latitude: " + self.latitude + "\n" +
            "longitude: " + self.longitude
        )
