# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
#if superuser visits the site, don't let him

# Create your views here.
def index(request):
	if request.method=='POST':
		user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
		if (user is not None) and (user.is_superuser==False):
			login(request,user)
			return redirect('/yearbook/profile')
		else:
			return render(request, 'myapp/index.html')
	return render(request, 'myapp/index.html')

@login_required()
def profile(request):
	# add image field edit
	u = request.user
	if request.method=='GET':
		UsrObj = Student(name=u.student.name, department=u.student.department,
			DP=u.student.DP,phone=u.student.phone,email=u.student.email,
			oneliner=u.student.oneliner)
		context={"user":UsrObj}
		return render(request, 'myapp/profile.html',context)
	u.student.name = request.POST['name']
	u.student.phone = request.POST['phone']
	u.student.email = request.POST['email']
	u.student.oneliner = request.POST['oneliner']
	u.student.save()
	return redirect('/yearbook/profile')



@login_required
def answerMyself(request):
	u = request.user
	if request.method=='GET':
		GenQuestions = GenQuestion.objects.all()
		AnswersDisplay = u.student.AnswersAboutMyself
		gen_GenQuestions = []
		for q in GenQuestions:
			gen_GenQuestions.append([q.id,q.question,""])
			if (AnswersDisplay.has_key(str(q.id))):
				gen_GenQuestions[-1][-1] = AnswersDisplay[str(q.id)]
		context={"genQuestions":gen_GenQuestions}
		return render(request, 'myapp/answers.html',context)
	u.student.AnswersAboutMyself[request.POST['id']] = request.POST['answer']
	u.student.save()
	return redirect('/yearbook/answer')	
@login_required()
def poll(request):
	u = request.user
	if request.method=='GET':
		allPolls = Poll.objects.filter(department="all")
		deptPolls = Poll.objects.filter(department=u.student.department)
		VotesDisplay = u.student.VotesIHaveGiven
		gen_allPolls=[]
		gen_deptPolls=[]
		for p in allPolls:
			gen_allPolls.append([p.id,p.poll,""])
			if (VotesDisplay.has_key(str(p.id))):
				gen_allPolls[-1][-1]=VotesDisplay[str(p.id)]
		for p in deptPolls:
			gen_deptPolls.append([p.id,p.poll,""])
			if (VotesDisplay.has_key(str(p.id))):
				gen_deptPolls[-1][-1]=VotesDisplay[str(p.id)]
	
		context={"allPolls":gen_allPolls, "deptPolls":gen_deptPolls}
		return render(request, 'myapp/poll.html',context)

	# if POST request 
	fetchPoll = ""
	if Poll.objects.filter(id = request.POST['id']).exists():
		fetchPoll = Poll.objects.get(id = request.POST['id'])
	else:
		return redirect("/yearbook/poll")
	if (u.student.VotesIHaveGiven.has_key(request.POST['id'])):
		OldVotePresent = u.student.VotesIHaveGiven[request.POST['id']]
		fetchPoll.votes[OldVotePresent] = fetchPoll.votes[OldVotePresent] - 1	
	
	if(fetchPoll.votes.has_key(request.POST['entrynumber'])):
		fetchPoll.votes[request.POST['entrynumber']] = fetchPoll.votes[request.POST['entrynumber']] + 1	
	else:
		fetchPoll.votes[request.POST['entrynumber']] = 1
	u.student.VotesIHaveGiven[request.POST['id']] = request.POST['entrynumber']		
	fetchPoll.save()
	u.student.save()
	return redirect("/yearbook/poll")
		
@login_required()
def comment(request):
	if request.method=='GET':
		u = request.user
		myComments = u.student.CommentsIWrite
		# Convert myComments to required types
		
		context={"myComments":myComments}
		return render(request, 'myapp/comment.html',context)
@login_required()
def otherComment(request):
	pass

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

	
