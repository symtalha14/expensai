from django.db import models
from datetime import datetime, date
# Create your models here.
class ExpenseRecord(models.Model):
    username = models.CharField(max_length=255, default="NA")
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default="INR")
    date_time = models.DateTimeField(default=datetime.now())
    date = models.DateField(default=date.today())
    month = models.CharField(max_length=10)
    year = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    comments = models.TextField(max_length=400, default="")
    def __str__(self):
        return str(self.amount)+" "+self.username


