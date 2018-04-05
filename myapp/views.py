# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *


# Create your views here.
def index(request):
	if request.method=='POST':
		user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
		if user is not None:
			login(request,user)
			return redirect('/yearbook/profile')
		else:
			return render(request, 'myapp/index.html')
	return render(request, 'myapp/index.html')

@login_required()
def profile(request):
	if request.method=='GET':
		u = request.user
		allGenQuestions = GenQuestion.objects.all()
		UsrObj = Student(name=u.student.name, department=u.student.department,
			DP=u.student.DP,phone=u.student.phone,email=u.student.email,
			oneliner=u.student.oneliner,AnswersAboutMyself=u.student.AnswersAboutMyself)

		context={"user":UsrObj,"questions":allGenQuestions}
		return render(request, 'myapp/profile.html',context)

@login_required()
def poll(request):
	if request.method=='GET':
		u = request.user
		allPolls = Poll.objects.all()
		deptPolls = Poll.objects.filter(department=u.student.department)
		# Create a new object to remove the field of votes

		context={"allPolls":allPolls, "deptPolls":deptPolls}
		return render(request, 'myapp/poll.html',context)

@login_required()
def comment(request):
	if request.method=='GET':
		u = request.user
		myComments = u.student.CommentsIWrite
		# Convert myComments to required types
		
		context={"myComments":myComments}
		return render(request, 'myapp/comment.html',context)

def userlogout(request):
	logout(request)
	return redirect("/yearbook/")

@login_required()
def changePassword(request):
	if request.method=='POST':
		if (request.POST['password1']!=request.POST['password2']):
			return redirect("/yearbook/changePassword")
		else:
			u = User.objects.get(id = request.user.id)
			u.set_password(request.POST['password1'])
			u.save()
			return redirect("/yearbook/profile")
	return render(request, 'myapp/changePassword.html')

	
