from django.db import models


class Subscription(models.Model):

    label = models.CharField(max_length=50)
    img_url = models.URLField()
