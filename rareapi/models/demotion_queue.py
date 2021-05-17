from django.db import models
from django.contrib.auth.models import User

class DemotionQueue(models.Model):
    action = models.CharField(max_length=50)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    approver_one = models.ForeignKey(User, on_delete=models.CASCADE)
