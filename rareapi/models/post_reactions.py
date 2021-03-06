from django.db import models


class PostReaction(models.Model):

    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
