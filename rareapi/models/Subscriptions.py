from django.db import models


class Subscription(models.Model):

    created_on = models.DateTimeField()
    ended_on = models.DateTimeField()
    follower_id = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    user_id = models.ForeignKey("RareUser", on_delete=models.CASCADE)
