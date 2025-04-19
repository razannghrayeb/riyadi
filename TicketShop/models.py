from django.db import models
from django.conf import settings
import cloudinary.uploader

class Game(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    total_tickets = models.IntegerField(default=0)
    tickets_sold = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    thumbnail = models.URLField(default="https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    def __str__(self):
        return f"{self.name} at {self.location} on {self.date.strftime('%Y-%m-%d')}"
    def save(self, *args, **kwargs):
        if hasattr(self, '_thumbnail_file') and self._thumbnail_file: 
            upload_result = cloudinary.uploader.upload(self._thumbnail_file)
            self.thumbnail = upload_result['url']  
            self._thumbnail_file = None  

        super(Game, self).save(*args, **kwargs)

    def set_thumbnail_file(self, file):
        self._thumbnail_file = file  # Temporary storage of the file
    def is_user_attendee(self, user):
        return self.attendees.filter(id=user.id).exists()