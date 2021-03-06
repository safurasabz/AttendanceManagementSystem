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
    graph = models.CharField(max_length=30, null=True)
    date = models.CharField(max_length=20)
    came = models.CharField(max_length=20)
    gone = models.CharField(max_length=20)
    early_came = models.CharField(max_length=20)
    late_came = models.CharField(max_length=20)
    late_camedec = models.IntegerField(null=True)
    late_camebin = models.IntegerField(null=True)
    early_gone = models.CharField(max_length=20)
    early_gonedec = models.IntegerField(null=True)
    late_gone = models.CharField(max_length=20)
    build_exit = models.IntegerField(null=True)
    distraction = models.CharField(max_length=20)
    overall_ghourdec = models.IntegerField(null=True)
    overall_hourdec = models.IntegerField(null=True)
    overall_ghour = models.CharField(max_length=20)
    overall_hour = models.CharField(max_length=20)
    overtimedec = models.IntegerField(null=True)
    permission = models.CharField(max_length=20, null=True)
    permissionreason = models.CharField(max_length=20, null=True)
    modalnum = models.CharField(max_length=50, null=True)
    modalnumdash = models.CharField(max_length=50, null=True)
    hour_str = models.CharField(max_length=300, null=True)
    def __str__(self):
        return self.fullname

class Permissions(models.Model):
    name = models.CharField(max_length=20)
    date = models.CharField(max_length=20)
    hour1 = models.CharField(max_length=20)
    hour2 = models.CharField(max_length=20)
    reason = models.CharField(max_length=20)
    note = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Shortday(models.Model):
    date = models.CharField(max_length=20)

    def __str__(self):
        return self.date






