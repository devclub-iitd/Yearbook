# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
	return '{0}/{1}'.format(instance.department, filename)
# Create your models here.
class GenQuestion(models.Model):
	question = models.CharField(max_length=200)
	def __str__(self):
		return self.question

class Poll(models.Model):
	departments = [
		("chemical", "chemical"),
		("civil", "civil"),
		("cse", "computer science"),
		("ee", "electrical"),
		("maths", "mathematics"),
		("mech", "mechanical"),
		("physics", "engineering physics"),
		("textile", "textile engineering"),
		("dbeb", "biotechnology"),
		("all", "all"),
	]
	poll = models.CharField(max_length=200)
	department = models.CharField(max_length=200,choices=departments)
	votes = JSONField(blank=True,default=dict)
	def __str__(self):
		return self.poll

class Student(models.Model):
	departments = [
		("chemical", "chemical"),
		("civil", "civil"),
		("cse", "computer science"),
		("ee", "electrical"),
		("maths", "mathematics"),
		("mech", "mechanical"),
		("physics", "engineering physics"),
		("textile", "textile engineering"),
		("dbeb", "biotechnology"),
		("all", "all")
	]
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100,blank=True)
	department = models.CharField(max_length=100,choices=departments)
	DP = models.ImageField(upload_to="DP",blank=True,default="DP/anonymous.png")
	genPic1 = models.ImageField(upload_to=user_directory_path,blank=True)
	genPic2 = models.ImageField(upload_to=user_directory_path,blank=True)
	phone = models.CharField(max_length=10,blank=True)
	email = models.CharField(max_length=100,blank=True)
	oneliner = models.CharField(max_length=100,blank=True)
	AnswersAboutMyself = JSONField(blank=True,default=dict)
	VotesIHaveGiven = JSONField(blank=True,default=dict)
	CommentsIWrite = JSONField(blank=True,default=list)
	CommentsIGet = JSONField(blank=True,default=list)
	def __str__(self):
		return self.name 




