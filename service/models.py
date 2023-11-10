from django.db import models

class OfficeBooking(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    pickup_location = models.CharField(max_length=250)
    drop_location = models.CharField(max_length=250)
    pickup_time = models.TimeField()
    return_time = models.TimeField()
    want_return = models.BooleanField(default=False)
    selected_days = models.ManyToManyField('SelectedDay', blank=True)

class SelectedDay(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    day = models.CharField(max_length=10, choices=DAY_CHOICES)

    def __str__(self):
        return self.get_day_display()
class SchoolBooking(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    pickup_location = models.CharField(max_length=250)
    drop_location = models.CharField(max_length=250)
    pickup_time = models.TimeField()
    return_time = models.TimeField()
    date = models.DateField()