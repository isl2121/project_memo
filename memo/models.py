from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Memo(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def save_memo(self):
        self.save()

    def total_like(self):
        return self.likes.count()
