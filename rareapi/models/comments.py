from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    content = models.CharField(max_length=500)
    created_on = models.DateTimeField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)



