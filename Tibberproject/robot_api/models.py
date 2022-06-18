from django.db import models

# Create your models here.


class Execution(models.Model):
    timestamp = models.DateField()
    commands = models.IntegerField()
    result = models.IntegerField()
    duration = models.FloatField()



