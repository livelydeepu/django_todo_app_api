import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


def validate_date(due_date):
    if due_date < datetime.date.today():
        raise ValidationError("Date cannot be in the past")


class Todo(models.Model):

    status_list = (
        ('open', 'OPEN'),
        ('working', 'WORKING'),
        ('done', 'DONE'),
        ('overdue', 'OVERDUE')
    )

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    due_date = models.DateField(validators=[validate_date])
    tags = models.ManyToManyField(
        Tag, related_name="tags", related_query_name="tag")
    status = models.CharField(
        max_length=10, choices=status_list, default='open')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.title
        return '{}'.format(self.title)

    class Meta:
        ordering = ['status']
