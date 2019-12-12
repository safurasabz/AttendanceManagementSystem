from django.db import models


class Excel(models.Model):
    name = models.CharField(max_length=30, default="  ")
    dat = models.CharField(max_length=30, default="  ")
    time = models.CharField(max_length=30, default="  ")
    action = models.CharField(max_length=30, default="  ")

    def __str__(self):
        return self.name
#class Exc(models.Model):


class Staff(models.Model):
    name = models.CharField(max_length=50)
    excel_name = models.CharField(max_length=50)
    #graph = models.IntegerField()
    status = models.IntegerField()

    def __str__(self):
        return self.name


class Log(models.Model):
    staff_id = models.IntegerField()
    #graph = models.IntegerField()
    date = models.CharField(max_length=20)
    came = models.CharField(max_length=10)
    gone = models.CharField(max_length=10)
    early_came = models.IntegerField()
    late_came = models.IntegerField()
    early_gone = models.IntegerField()
    late_gone = models.IntegerField()
    build_exit = models.IntegerField()
    distraction = models.IntegerField()
    overall_ghour = models.IntegerField()
    overall_hour = models.IntegerField()


