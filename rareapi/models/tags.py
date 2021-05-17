from django.db import models

class Tag():
    label = models.CharField(max_length=50)