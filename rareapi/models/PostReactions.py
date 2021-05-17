from django.db import models


class PostReaction(models.Model):

    reaction_id = models.ForeignKey("Reaction", on_delete=models.CASCADE)
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE)
    user_id = models.ForeignKey("RareUser", on_delete=models.CASCADE)
