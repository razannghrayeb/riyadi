from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.News)
admin.site.register(models.Player)
admin.site.register(models.Booking)
admin.site.register(models.Field)
