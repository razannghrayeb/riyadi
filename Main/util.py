import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from . import models
# This may not be the best place to put such functions, we can create a new file for these functions, utils usually include functions that are reusable, like date time format switcher
def getNews(start = 0, end = 5):
    """
    return a list of atleast the latest five news
    """
    news = models.News.objects.order_by("-date_uploaded")[start:end]
    return news



