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
    fullname = models.CharField(max_length=30)
    date = models.CharField(max_length=20)
    came = models.CharField(max_length=20)
    gone = models.CharField(max_length=20)
    early_came = models.CharField(max_length=20)
    late_came = models.CharField(max_length=20)
    early_gone = models.CharField(max_length=20)
    late_gone = models.CharField(max_length=20)
    build_exit = models.IntegerField()
    distraction = models.CharField(max_length=20)
    overall_ghour = models.CharField(max_length=20)
    overall_hour = models.CharField(max_length=20)
    # staff_id = models.IntegerField()
    # graph = models.IntegerField()

    def __str__(self):
        return self.fullname


