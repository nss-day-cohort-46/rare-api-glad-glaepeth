from django.db import models

class Comment():
    content = models.CharField(max_length=500)
    created_on = models.DateTimeField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    


