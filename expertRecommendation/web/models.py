from django.db import models

# Create your models here.
class expert(models.Model):
    expertID  = models.BigIntegerField()
    expertName = models.CharField(max_length=20)
    work_for = models.CharField(max_length=200)