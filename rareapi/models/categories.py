from django.db import models

class Category():
    label = models.CharField(max_length=50)
    