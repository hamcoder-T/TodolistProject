from django.db import models
from django.urls.base import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Event(models.Model):
    class Status(models.TextChoices):
        DONE = 'DO', 'Done'
        UNDONE = 'UN', 'Undone'

    user = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name="عنوان", blank=True, default="(عنوانی وجود ندارد)")
    description = models.TextField(verbose_name="توضیحات", blank=True, default="(توضیحاتی وجود ندارد)")
    begin = models.DateTimeField(verbose_name="زمان شروع", default=timezone.now, blank=True)
    end = models.DateTimeField(verbose_name="زمان پایان", null=True, blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.UNDONE)  # type: ignore

    class Meta:
        ordering = ['begin']
        indexes = [
            models.Index(fields=['begin'])
        ]

    def save(self, *args, **kwargs):
        if self.begin and not self.end:
            self.end = self.begin + timedelta(hours=2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todolist:event-detail', args=[self.id])  # type: ignore


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    is_done = models.BooleanField(default=False, verbose_name="انجام شده؟")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
