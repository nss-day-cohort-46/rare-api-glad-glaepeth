from django.db import models


class Subscription(models.Model):

    created_on = models.DateTimeField()
    ended_on = models.DateTimeField()
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="follower")
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="author")
