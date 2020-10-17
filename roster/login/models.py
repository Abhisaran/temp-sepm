from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id + " " + self.password


class Staff(models.Model):
    user_id = models.CharField(max_length=20, unique=True)

    leave_allowance = models.IntegerField(default=0)
    annual_leave = models.IntegerField(default=10)
    carer_leave = models.IntegerField(default=10)
    blood_donor_leave = models.IntegerField(default=10)
    sick_certificate_leave = models.IntegerField(default=10)
    sick_leave = models.IntegerField(default=10)
    parental_leave = models.IntegerField(default=10)
    unpaid_leave = models.IntegerField(default=10)

    request_history = models.TextField(default="")
    manager = models.CharField(max_length=20, default="abhi")

    def __str__(self):
        return self.user_id + " " + str(self.leave_allowance) + " " + str(self.annual_leave) + " " + \
               str(self.carer_leave) + " " + str(self.blood_donor_leave) + " " \
               + str(self.sick_certificate_leave) + \
               " " + str(self.sick_leave) + " " + str(self.parental_leave) + " " \
               + str(self.unpaid_leave) + " " + str(self.request_history)


class Manager(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    request_approve = models.TextField(default="")


class Admin(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
