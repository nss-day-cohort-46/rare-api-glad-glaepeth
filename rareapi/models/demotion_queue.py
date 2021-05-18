from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related

class DemotionQueue(models.Model):
    action = models.CharField(max_length=50)
    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="admin")
    approver_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name="approver")
