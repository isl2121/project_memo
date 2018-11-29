from django.db import models
from django.utils.timezone import now

# Create your models here.
class Memo(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    content = models.TextField()
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return self.title