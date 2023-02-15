from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

class Sample(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    values = models.JSONField()

# class Pattern(models.Model):
#     sample = models.ForeignKey(Sample, on_delete=models.CASCADE)



