from django.db import models
# from Accounts.models import Profile
from django.contrib.auth.models import User

# Create your models here.


class Events(models.Model):
    event_name=models.CharField(max_length=200)
    venue= models.CharField(max_length=200)
    description= models.TextField(max_length=500)
    starts_at= models.DateTimeField()
    ends_at= models.DateTimeField()

class Participants(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    event_name=models.ForeignKey(Events, on_delete=models.CASCADE)
    is_registered= models.BooleanField(default=False)

    class Meta:
        default_related_name = 'participants'
    def __str__(self):
        return self.user.username