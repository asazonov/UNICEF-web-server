from django.db import models

class MobileUser(models.Model):
	mobile = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=50)
	user_type = models.CharField(max_length=20)
	location = models.CharField(max_length=200)
	longitude = models.CharField(max_length=15)
	latitude = models.CharField(max_length=15)

	def __unicode__(self):
		return 'name: {} mobile: {} user_type: {} location: {}'.format(name, mobile, user_type, location)