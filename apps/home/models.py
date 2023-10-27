# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

class user_info(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.IntegerField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    departament = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)



class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=100, blank=True, null=True)

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    prefix = models.CharField(max_length=100, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(user_info, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True)

class Assignments(models.Model): # ! tabla nub entre profesor y asignatura
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(user_info, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True)