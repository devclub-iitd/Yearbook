# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

	class Meta:
		unique_together = ("poll", "department")

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
	DP = models.ImageField(upload_to="DP",blank=True,default="DP/anonymous.jpg")
	genPic1 = models.ImageField(upload_to=user_directory_path,blank=True)
	genPic2 = models.ImageField(upload_to=user_directory_path,blank=True)
	phone = models.CharField(max_length=10,blank=True)
	email = models.CharField(max_length=100,blank=True)
	oneliner = models.CharField(max_length=100,blank=True)
	future = models.CharField(max_length=100,blank=True)
	AnswersAboutMyself = JSONField(blank=True,default=dict)
	VotesIHaveGiven = JSONField(blank=True,default=dict)
	CommentsIWrite = JSONField(blank=True,default=list)
	CommentsIGet = JSONField(blank=True,default=list)
	WordCloud = models.ImageField(upload_to="wordcloud",blank=True)
	def __str__(self):
		return self.name 

class Adjective(models.Model):
	adjective_list = [
		("optimistic", "optimistic"),
		("kanjoos", "kanjoos"),
		("genius", "genius"),
		("gym-freak","gym-freak"),
		("tharki", "tharki"),
		("maggu", "maggu"),
		("helpful", "helpful"),
		("cry-baby", "cry-baby"),
		("hard-working","hard-working"),
		("show-off", "show-off"),
		("pakau", "pakau"),
		("foodie", "foodie"),
		("gossiper", "gossiper")
	]
	adjective = models.CharField(max_length=100, choices=adjective_list)
	forWhom = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="AdjectivesIGet")
	byWhom = models.ManyToManyField(Student, related_name="AdjectivesIGive")

class AdminTable(models.Model):
	displayYearbook = models.BooleanField(default=False)
	deadline = models.DateTimeField()

	def save(self, *args, **kwargs):
		if not self.pk and AdminTable.objects.exists():
			raise ValidationError('Only one instance of admin table is allowed. Please edit the existing admin table object.')
		return super(AdminTable, self).save(*args, **kwargs)



