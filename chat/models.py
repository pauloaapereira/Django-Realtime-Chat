from django.db import models

# Message model
class Message(models.Model):
    user_name = models.CharField(max_length=20)
    message = models.CharField(max_length=140)
