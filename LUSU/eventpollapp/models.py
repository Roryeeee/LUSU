from django.db import models
from django.contrib.auth.models import User
import uuid

class UserGroup(models.Model):
    name = models.CharField(max_length=100)
    member = models.ManyToManyField(User, related_name='user_groups')

    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)



    def __str__(self):
        return self.user.username


class Event(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug= models.SlugField(unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    visible_to = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.title

class TimeOption(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='time_options')
    option = models.DateTimeField()


    def __str__(self):
        return f"{self.event.title} - {self.option}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_option = models.ForeignKey(TimeOption, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'time_option')

    def __str__(self):
        return f"{self.user.username} voted for {self.time_option}"