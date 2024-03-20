from django.db import models


# Create your models here.
class PathChecker(models.Model):
    title = models.CharField(max_length=100)
    path = models.TextField()

    def __str__(self):
        return self.title