from django.db import models

# Create your models here.
class Expert(models.Model):
    expertID  = models.BigIntegerField(20)
    expertName = models.CharField(max_length=10)
    work_for = models.CharField(max_length=128)
    keywords = models.CharField(max_length=256)

class Paper(models.Model):
    expertID = models.BigIntegerField(20)
    title = models.CharField(max_length=128)
    authorlist = models.CharField(max_length=128)
    pub_date = models.DateField()



