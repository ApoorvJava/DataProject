from django.db import models

class Weather(models.Model):
    date = models.DateField()
    max_temperature = models.FloatField()
    min_temperature = models.FloatField()
    precipitation = models.FloatField()
    station_id = models.CharField(max_length = 20)

class Yield(models.Model):
    total_corn = models.IntegerField()
    year = models.IntegerField()

class Results(models.Model):
    year = models.IntegerField(default=2022)
    station_id = models.CharField(max_length = 20, default='')
    avg_max_temperature = models.FloatField()
    avg_min_temperature = models.FloatField()
    total_precipitation = models.FloatField()