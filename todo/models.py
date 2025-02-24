from django.db import models
from django.contrib.auth.models import User

class ToDoo(models.Model):
    sr_no = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    