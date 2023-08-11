from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=250, blank=True)
    content = models.TextField()
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateField(default=timezone.now)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
