from django.db import models



class RareUser(models.Model):

    user = models.OneToOneField("User", on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url = models.CharField(max_length=250)
    created_on = models.DateTimeField()
    active = models.BooleanField()
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
