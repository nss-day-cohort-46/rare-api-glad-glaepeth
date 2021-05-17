from django.db import models

class PostTag():
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    