from django.db import models

# Create your models here.

class PunchAttendance(models.Model):
    employee_id = models.CharField(max_length=50)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

class Attendance(models.Model):
    employee_id = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=20)
    date = models.CharField(max_length=2)
 
    attendance = models.CharField(max_length=1)
