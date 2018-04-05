# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
	return 'media/{0}/{1}'.format(instance.student.student.department, filename)
# Create your models here.
class GenQuestion(models.Model):
	question = models.CharField(max_length=200)
	def __str__(self):
		return self.question

class Poll(models.Model):
	poll = models.CharField(max_length=200)
	department = models.CharField(max_length=200)
	oneliner = models.CharField(max_length=200)
	votes = JSONField()
	def __str__(self):
		return self.poll

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	department = models.CharField(max_length=100)
	DP = models.ImageField(upload_to="media/DP")
	phone = models.CharField(max_length=10,blank=True)
	email = models.CharField(max_length=100,blank=True)
	oneliner = models.CharField(max_length=100,blank=True)
	AnswersAboutMyself = JSONField(blank=True)
	VotesIHaveGiven = JSONField(blank=True)
	CommentsIWrite = JSONField(blank=True)
	CommensIGet = JSONField(blank=True)
	
class ImageModel(models.Model):
	image = models.ImageField(upload_to=user_directory_path)
	student = models.ForeignKey(User,on_delete=models.CASCADE)




