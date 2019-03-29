#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from myapp import Config as config

import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()


def kerberos_to_entry_number(kerberos):
    return "20" + kerberos[3:5] + kerberos[:3].upper() + kerberos[5:]

# Create your views here.


def index(request):
    # if request.method == 'POST':
        # return redirect(config.authLinkPart1 + config.CLIENT_ID + config.authLinkPart2)
    myUser = User.objects.get(username=('atishya').lower())
    print (myUser)
    login(request, myUser)
    return redirect('/profile')
    # return render(request, 'myapp/index.html')


def authenticate(request):
    PostData = {'client_id': config.CLIENT_ID,
    'client_secret': config.CLIENT_SECRET,
    'grant_type': config.AUTHORIZATION_CODE,
    'code': request.GET.get('code')}
    print("###")

    r = requests.post(config.OauthTokenURL, PostData, verify=config.certiPath)
    a = r.json()
    access_token = a['access_token']
    PostData2 = {
        'access_token': access_token
    }
    r1 = requests.post(config.ResourceURL, PostData2, verify=config.certiPath)
    b = r1.json()

    # if User.objects.filter(username=(b['uniqueiitdid']).lower()).exists():
    #     myUser = User.objects.get(username=(b['uniqueiitdid']).lower())
    #     login(request, myUser)
    #     return redirect('/profile')
    # else:
    #     return redirect('/')
    myUser = User.objects.get(username=('mayank').lower())
    login(request, myUser)
    return redirect('/profile')

@login_required()
def profile(request):
    # add image field edit
    u = request.user
    UsrObj = Student(name=u.student.name, department=u.student.department,
            DP=u.student.DP, phone=u.student.phone, email=u.student.email,
            oneliner=u.student.oneliner, genPic1=u.student.genPic1, genPic2=u.student.genPic2)
    if request.method == 'GET':
        context = {"user": UsrObj}
        return render(request, 'myapp/profile.html', context)
    # print int(request.FILES.get('dp').size)<6000000
    if(request.FILES.get('dp') != None and int(request.FILES.get('dp').size) < 6000000):
        # Get the picture
        picture = request.FILES.get('dp')
        # check extension
        if not (picture.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            return render(request, 'myapp/profile.html', {"user": UsrObj, "image": "Image should be in .png, .jpg or .jpeg format"})
        picture.name = u.username + ".jpg"
        u.student.DP = picture

    if(request.FILES.get('genPic1') != None and int(request.FILES.get('genPic1').size) < 6000000):
        u.student.genPic1 = request.FILES.get('genPic1')
        if not (u.student.genPic1.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            return render(request, 'myapp/profile.html', {"user": UsrObj, "image": "Image should be in .png, .jpg or .jpeg format"})
        u.student.genPic1.name = u.username + "1.jpg"

    if(request.FILES.get('genPic2') != None and int(request.FILES.get('genPic2').size) < 6000000):
        u.student.genPic2 = request.FILES.get('genPic2')
        if not (u.student.genPic2.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            return render(request, 'myapp/profile.html', {"user": UsrObj, "image": "Image should be in .png, .jpg or .jpeg format"})
        u.student.genPic2.name = u.username + "2.jpg"

    u.student.name = request.POST.get('name')
    if len(u.student.name) == 0:
        return render(request, 'myapp/profile.html', {"user": UsrObj, "name": "Name cannot be empty"})

    # Phone email and oneliner can be empty if the user does not wish to specify.
    u.student.phone = request.POST.get('phone')
    u.student.email = request.POST.get('email')
    u.student.oneliner = request.POST.get('oneliner')
    u.student.save()
    return redirect('/profile')


@login_required
def answerMyself(request):
    u = request.user
    if request.method == 'GET':
        GenQuestions = GenQuestion.objects.all()
        AnswersDisplay = u.student.AnswersAboutMyself
        gen_GenQuestions = []
        for q in GenQuestions:
            gen_GenQuestions.append([q.id, q.question, ""])
            if (AnswersDisplay.has_key(str(q.id))):
                gen_GenQuestions[-1][-1] = AnswersDisplay[str(q.id)]
        context = {"genQuestions": gen_GenQuestions}
        return render(request, 'myapp/answers.html', context)
    # print request.POST.getlist('answer[]')
    for i in range(len(request.POST.getlist('answer[]'))):
        if GenQuestion.objects.filter(id=request.POST.getlist('id[]')[i]).exists() and len(str(request.POST.getlist('answer[]')[i]).strip())>0:
            u.student.AnswersAboutMyself[request.POST.getlist(
                'id[]')[i]] = request.POST.getlist('answer[]')[i]
        else:
            continue
        u.student.save()
    return redirect('/answer')


@login_required()
def poll(request):
    u = request.user
    if request.method == 'GET':
        enum_to_name = {}
        users_all = User.objects.filter(is_superuser=False).order_by('username')
        
        dept_users = []
        users = [] # made seperate for same year vote only

        for i in users_all:
            enum_to_name[i.username] = i.student.name
            if i.username[:4] == u.username[:4]:
                users.append(i)
                if i.student.department==u.student.department:
                    dept_users.append(i)

        allPolls = Poll.objects.filter(department="all")
        deptPolls = Poll.objects.filter(department=u.student.department)
        VotesDisplay = u.student.VotesIHaveGiven
        gen_allPolls=[]
        gen_deptPolls=[]
        
        for p in allPolls:
            gen_allPolls.append([p.id,p.poll,"", ""])
            if (VotesDisplay.has_key(str(p.id))):
                gen_allPolls[-1][2]=VotesDisplay[str(p.id)]
                gen_allPolls[-1][3]=enum_to_name.get(VotesDisplay[str(p.id)], "")
                
        for p in deptPolls:
            gen_deptPolls.append([p.id,p.poll,"", ""])
            if (VotesDisplay.has_key(str(p.id))):
                gen_deptPolls[-1][2]=VotesDisplay[str(p.id)]
                gen_deptPolls[-1][3]=(enum_to_name.get(VotesDisplay[str(p.id)], ""))
        context={"allPolls":gen_allPolls, "deptPolls":gen_deptPolls,"users":users,"deptUsers":dept_users}
        return render(request, 'myapp/poll.html',context)

    # if POST request 
    # print request.POST.getlist('entrynumber[]')
    for i in range(len(request.POST.getlist('entrynumber[]'))):
        fetchPoll = ""
        if Poll.objects.filter(id = request.POST.getlist('id[]')[i]).exists():
            fetchPoll = Poll.objects.get(id = request.POST.getlist('id[]')[i])
        else:
            return redirect("/poll")
        if (u.student.VotesIHaveGiven.has_key(request.POST.getlist('id[]')[i])):
            OldVotePresent = u.student.VotesIHaveGiven[request.POST.getlist('id[]')[i]]
            if(OldVotePresent in fetchPoll.votes):
                fetchPoll.votes[OldVotePresent] = fetchPoll.votes[OldVotePresent] - 1   
        
        lowerEntry = (request.POST.getlist('entrynumber[]')[i]).lower()
        if(fetchPoll.votes.has_key(lowerEntry)):
            if ((lowerEntry != u.username.lower())):
                fetchPoll.votes[lowerEntry] = fetchPoll.votes[lowerEntry] + 1   
            else:
                return redirect("/poll")
        else:
            # A not found check for poll and Cannot vote oneself
            if (User.objects.filter(username = lowerEntry).exists() and (lowerEntry != u.username.lower())):
                toVoteDepartment = (User.objects.get(username=lowerEntry)).student.department
                if (((fetchPoll.department.lower() == "all") or (fetchPoll.department.lower() == toVoteDepartment.lower())) and (lowerEntry[0:4] == u.username[0:4])):      
                    fetchPoll.votes[lowerEntry] = 1
                else:
                    return redirect("/poll")        
            #else:
            #    return redirect("/poll")
        if(lowerEntry != u.username.lower()):
            u.student.VotesIHaveGiven[request.POST.getlist('id[]')[i]] = lowerEntry     
        fetchPoll.save()
        u.student.save()
    return redirect("/poll")
        
@login_required()
def comment(request):
    u = request.user
    users_all = User.objects.filter(is_superuser=False).order_by('username') 
        # we pass this to display options, remove self user
    myComments = u.student.CommentsIWrite
    gen_comments = []
    for c in myComments:
        tmpName=c["forWhom"]
        if User.objects.filter(username = c["forWhom"]).exists():
            tmpName=User.objects.get(username=c["forWhom"]).student.name
        gen_comments.append([c["comment"],c["forWhom"],tmpName])
    context={"comments":gen_comments,"users":users_all}
    if request.method=='GET':
        return render(request, 'myapp/comment.html',context)
    for i in range(len(request.POST.getlist('forWhom[]'))):
        lowerEntry = (request.POST.getlist('forWhom[]')[i]).lower()
        for c in u.student.CommentsIWrite:
            if c["forWhom"]==lowerEntry: #updating an already written message
                c["comment"]=request.POST.getlist('val[]')[i]
                # A not found check for the user
                if (User.objects.filter(username = lowerEntry).exists() and (u.username.lower() != lowerEntry)):
                    u_new = User.objects.get(username=lowerEntry) 
                else:
                    return redirect('/comment')
                for c_new in u_new.student.CommentsIGet:
                    if c_new["fromWhom"]==u.username:
                        c_new["comment"]=request.POST.getlist('val[]')[i]
                        break
                u_new.student.save()
                break
        else:
            u.student.CommentsIWrite.append({"comment":request.POST.getlist('val[]')[i],"forWhom":lowerEntry})
            # A not found check of user and I cant comment for myself
            if (u.username.lower() == lowerEntry):
                return render(request, 'myapp/comment.html', {"comments":gen_comments,"users":users_all, "comment": "You can't comment for yourself :)"})
            if (User.objects.filter(username = lowerEntry).exists()):
                u_new = User.objects.get(username=lowerEntry)
            else:
                print (User.objects.filter(username = lowerEntry).exists())
                return redirect('/comment')
            u_new.student.CommentsIGet.append({"comment":request.POST.getlist('val[]')[i],"fromWhom":u.username,"displayInPdf":"True"})
            u_new.student.save()
        u.student.save()
    return redirect('/comment')

@login_required()
def otherComment(request):
    u = request.user
    if request.method=='GET':
        CommentsIGet = u.student.CommentsIGet
        gen_comments=[]
        for c in CommentsIGet:
            tmpName=c["fromWhom"]
            if User.objects.filter(username = c["fromWhom"]).exists():
                tmpName=User.objects.get(username=c["fromWhom"]).student.name
            gen_comments.append([c["comment"],c["fromWhom"],tmpName,c["displayInPdf"]])
        context={"comments":gen_comments}
        return render(request, 'myapp/otherComment.html',context)
    for i in range(len(request.POST.getlist('fromWhom[]'))):
        lowerEntry = (request.POST.getlist('fromWhom[]')[i]).lower()
        for c in u.student.CommentsIGet:
            if c["fromWhom"]==lowerEntry:
                c["displayInPdf"]=request.POST.getlist('val[]')[i]
                break
        u.student.save()
    return redirect('/otherComment')
@login_required()
def yearbook(request):
    dep=""
    departmentDic={
            "chemical": "chemical",
            "civil": "civil",
            "cse": "computer science",
            "ee": "electrical",
            "maths": "mathematics",
            "mech": "mechanical",
            "physics": "engineering physics",
            "textile": "textile engineering",
            "dbeb": "biotechnology",
            "all": "all"
        }
    if request.user.is_superuser:
        dep = request.GET.get('department')
    else:
        dep = request.user.student.department
        
    departmentN=""
    if departmentDic.has_key(dep):
        departmentN = departmentDic[dep]
    else:
        departmentN = "all"
    GenQuestions = GenQuestion.objects.all()
    students_dep = Student.objects.filter(department=dep)
    for i in students_dep:
        gen_GenQuestions=list([])
        for q in GenQuestions:
            if (i.AnswersAboutMyself.has_key(str(q.id)) and i.AnswersAboutMyself[str(q.id)]!=""):
                gen_GenQuestions.append([])
                gen_GenQuestions[-1] = [q.question,i.AnswersAboutMyself[str(q.id)]]
        i.AnswersAboutMyself=list(gen_GenQuestions)

        gen_commentsIGet=list([])
        for a in i.CommentsIGet:
            if(User.objects.filter(username=a['fromWhom']).exists() and a['comment']!="" and a['displayInPdf']=="True"):
                gen_commentsIGet.append([])
                gen_commentsIGet[-1] = [a['comment'],User.objects.filter(username=a['fromWhom'])[0].student.name]
        i.CommentsIGet=list(gen_commentsIGet)

    all_polls=[]
    for p in Poll.objects.filter(department="all"):
        tmpVotes = []
        for (person,count) in p.votes.iteritems():
            Person=""
            if(User.objects.filter(username=person).exists()):
                Person=User.objects.filter(username=person)[0].student.name
            tmpVotes.append([int(count),Person])
        tmpVotes.sort(reverse=True)
        ind = min(5,len(tmpVotes))
        if ind!=0:
            all_polls.append([p.poll,tmpVotes[0:ind]])
    dep_polls=[]
    for p in Poll.objects.filter(department=dep):
        tmpVotes = []
        for (person,count) in p.votes.iteritems():
            Person=""
            if(User.objects.filter(username=person).exists()):
                Person=User.objects.filter(username=person)[0].student.name
            tmpVotes.append([int(count),Person])
        tmpVotes.sort(reverse=True)
        ind = min(5,len(tmpVotes))
        if ind!=0:
            dep_polls.append([p.poll,tmpVotes[0:ind]])

    context={"students":students_dep,"department":departmentN,"allPolls":all_polls,"deptPolls":dep_polls}
    return render(request, 'myapp/yearbook.html',context)
   


def userlogout(request):
    logout(request)
    return redirect("/")
