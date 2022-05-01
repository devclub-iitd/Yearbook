#-*- coding: utf-8 -*-
from __future__ import unicode_literals
# from myapp import Config as config

import requests
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

import io
import json

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

from django.template.defaulttags import register

import logging
logger = logging.getLogger(__name__)

def kerberos_to_entry_number(kerberos):
    return "20" + kerberos[3:5] + kerberos[:3].upper() + kerberos[5:]

# Create your views here.

def index(request):
    # logger.info(os.environ["OauthTokenURL"])
    # if request.method == 'POST':
        # return redirect(config.authLinkPart1 + config.CLIENT_ID + config.authLinkPart2)

    # For local development
    if hasattr(settings, 'BYPASS_OAUTH') and settings.BYPASS_OAUTH:
        myUser = User.objects.get(username=('2018_tester').lower())
        if not hasattr(myUser, 'student'):
            myUser.student = Student(name='2018_tester', department='cse')
            myUser.student.save()
            logger.info("New student created for user 2018_tester")
        
        login(request, myUser)
        return redirect('/profile')

    # For production
    if request.method == 'POST':
        return redirect(os.environ["authLinkPart1"] + os.environ["CLIENT_ID"] + os.environ["authLinkPart2"])
    return render(request, 'myapp/index.html')
    # return render(request, 'myapp/index.html')


def authenticate(request):
    # PostData = {'client_id': config.CLIENT_ID,
    # 'client_secret': config.CLIENT_SECRET,
    # 'grant_type': config.AUTHORIZATION_CODE,
    # 'code': request.GET.get('code')}

    PostData = {'client_id': os.environ["CLIENT_ID"],
    'client_secret': os.environ["CLIENT_SECRET"],
    'grant_type': os.environ["AUTHORIZATION_CODE"],
    'code': request.GET.get('code')}
    logger.info("###")

    r = requests.post(os.environ["OauthTokenURL"], PostData)
    a = r.json()
    access_token = a['access_token']
    PostData2 = {
        'access_token': access_token
    }
    r1 = requests.post(os.environ["ResourceURL"], PostData2)
    b = r1.json()

    if User.objects.filter(username=(b['uniqueiitdid']).lower()).exists():
        myUser = User.objects.get(username=(b['uniqueiitdid']).lower())
        login(request, myUser)
        return redirect('/profile')
    else:
        # return redirect('/')
        return render(request, 'myapp/index.html', {"error_string": "You are unauthorized to access"})
        # return HttpResponse('Unauthorized to access')
    # myUser = User.objects.get(username=('atishya').lower())
    # login(request, myUser)
    # return redirect('/profile')

@login_required()
def profile(request):
    # add image field edit
    u = request.user
    UsrObj = Student(name=u.student.name, department=u.student.department,
            DP=u.student.DP, phone=u.student.phone, email=u.student.email,
            oneliner=u.student.oneliner, future=u.student.future, genPic1=u.student.genPic1, genPic2=u.student.genPic2)
    if request.method == 'GET':
        context = {"user": UsrObj}
        return render(request, 'myapp/profile.html', context)

    ## Need it to stop people from uploading new pics
    if is_deadline_over():
        return deadlineover(request)

    obj = {}
    flag = False
    # logger.info(int(request.FILES.get('dp').size)<6000000)
    if(request.FILES.get('dp') != None and int(request.FILES.get('dp').size) < 6000000):
        # Get the picture
        picture = request.FILES.get('dp')
        # check extension
        if not (picture.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            return render(request, 'myapp/profile.html', {"user": UsrObj, "image": "Image should be in .png, .jpg or .jpeg format"})
        extension = picture.name.lower()[picture.name.lower().rfind("."):] 
        picture.name = u.username + extension
        u.student.DP = picture

    if(request.FILES.get('genPic1') != None and int(request.FILES.get('genPic1').size) < 6000000):
        u.student.genPic1 = request.FILES.get('genPic1')
        if not (u.student.genPic1.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            flag = True
            obj["image"] = "Image should be in .png, .jpg or .jpeg format"
        else:
            extension = u.student.genPic1.name.lower()[u.student.genPic1.name.lower().rfind("."):]
            u.student.genPic1.name = u.username + extension

    if(request.FILES.get('genPic2') != None and int(request.FILES.get('genPic2').size) < 6000000):
        u.student.genPic2 = request.FILES.get('genPic2')
        if not (u.student.genPic2.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            flag = True
            obj["image"] = "Image should be in .png, .jpg or .jpeg format"
        else:
            extension = u.student.genPic2.name.lower()[u.student.genPic2.name.lower().rfind("."):] 
            u.student.genPic2.name = u.username + extension

    u.student.name = request.POST.get('name')
    if len(u.student.name) == 0:
        return render(request, 'myapp/profile.html', {"user": UsrObj, "name": "Name cannot be empty"})

    # Phone email and oneliner can be empty if the user does not wish to specify.
    if len(request.POST.get('phone')) > 10:
        flag = True
        obj["phone"] = "Number has to be less than 10 characters"
    else:
        u.student.phone = request.POST.get('phone')

    if len(request.POST.get('email')) > 100: 
        flag = True
        obj["email"] = "Email has to be less than 100 characters"
    else:
        u.student.email = request.POST.get('email')

    if len(request.POST.get('oneliner')) > 100: 
        flag = True
        obj["oneliner"] = "Oneliner has to be less than 100 characters"
    else:
        u.student.oneliner = request.POST.get('oneliner')

    if len(request.POST.get('future')) > 100: 
        flag = True
        obj["future"] = "Future has to be less than 100 characters"
    else:
        u.student.future = request.POST.get('future')

    u.student.save()

    if flag:
        obj["user"] = u.student
        return render(request, 'myapp/profile.html', obj)

    return redirect('/profile')

@login_required
def delete_image(request, type):
    if type == 'DP':
        request.user.student.DP.delete()
        return redirect('/profile')
    elif type == 'genPic1':
        request.user.student.genPic1.delete()
        return redirect('/profile')
    elif type == 'genPic2':
        request.user.student.genPic2.delete()
        return redirect('/profile')
    elif type == 'closeFriendsPic':
        request.user.student.closeFriendsPic.delete()
        return redirect('/closeFriends')


@login_required
def answerMyself(request):
    u = request.user
    if request.method == 'GET':
        GenQuestions = GenQuestion.objects.all()
        AnswersDisplay = u.student.AnswersAboutMyself
        gen_GenQuestions = []
    
        for q in GenQuestions:
            gen_GenQuestions.append([q.id, q.question, ""])
            if (str(q.id) in AnswersDisplay):
                gen_GenQuestions[-1][-1] = AnswersDisplay[str(q.id)]
        context = {"genQuestions": gen_GenQuestions}
        return render(request, 'myapp/answers.html', context)
    # logger.info(request.POST.getlist('answer[]'))

    ## Need it to stop people from uploading new pics
    if is_deadline_over():
        return deadlineover(request)

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
    ## Need it to turn it off after deadline
    if is_deadline_over():
        return deadlineover(request)

    u = request.user

    enum_to_name = {}
    users_all = User.objects.filter(is_superuser=False).order_by('username')
    
    dept_users = []

    for i in users_all:
        enum_to_name[i.username] = i.student.name
        if i.student.department==u.student.department:
            dept_users.append(i)

    allPolls = Poll.objects.filter(department="all").order_by('poll')
    deptPolls = Poll.objects.filter(department=u.student.department).order_by('poll')
    VotesDisplay = u.student.VotesIHaveGiven
    gen_allPolls=[]
    gen_deptPolls=[]
    
    for p in allPolls:
        gen_allPolls.append([p.id,p.poll,"", ""])
        if (str(p.id) in VotesDisplay):
            gen_allPolls[-1][2]=VotesDisplay[str(p.id)]
            gen_allPolls[-1][3]=enum_to_name.get(VotesDisplay[str(p.id)], "")
            
    for p in deptPolls:
        gen_deptPolls.append([p.id,p.poll,"", ""])
        if (str(p.id) in VotesDisplay):
            gen_deptPolls[-1][2]=VotesDisplay[str(p.id)]
            gen_deptPolls[-1][3]=(enum_to_name.get(VotesDisplay[str(p.id)], ""))
    context={"allPolls":gen_allPolls, "deptPolls":gen_deptPolls,"users":users_all,"deptUsers":dept_users}

    if request.method == 'GET':
        return render(request, 'myapp/poll.html',context)

    # if POST request
    # logger.info(request.POST.getlist('entrynumber[]'))
    for i in range(len(request.POST.getlist('entrynumber[]'))):
        lowerEntry = (request.POST.getlist('entrynumber[]')[i]).lower()
        if not lowerEntry:
            continue

        fetchPoll = ""
        if Poll.objects.filter(id = request.POST.getlist('id[]')[i]).exists():
            fetchPoll = Poll.objects.get(id = request.POST.getlist('id[]')[i])
        else:
            return redirect("/poll")
        if (request.POST.getlist('id[]')[i] in u.student.VotesIHaveGiven):
            OldVotePresent = u.student.VotesIHaveGiven[request.POST.getlist('id[]')[i]]
            if(OldVotePresent in fetchPoll.votes):
                fetchPoll.votes[OldVotePresent] = fetchPoll.votes[OldVotePresent] - 1   
        
        if(lowerEntry in fetchPoll.votes):
            if ((lowerEntry != u.username.lower())):
                fetchPoll.votes[lowerEntry] = fetchPoll.votes[lowerEntry] + 1   
            else:
                return redirect("/poll")
        else:
            # A not found check for poll and Cannot vote oneself
            if (u.username.lower() == lowerEntry):
                return render(request, 'myapp/poll.html', {"allPolls":gen_allPolls, "deptPolls":gen_deptPolls,"users":users_all,"deptUsers":dept_users, "selfvote": "You cannot vote for yourself :)"})
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
        

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required()
def comment(request):
    u = request.user
    users_all = User.objects.filter(is_superuser=False).order_by('username')
        # we pass this to display options, remove self user
    myComments = u.student.CommentsIWrite
    myAdjectives = u.student.AdjectivesIGive.all()

    adj_dictionary = {}
    name_dictionary = {}
    for i in myAdjectives:
        name_dictionary[i.forWhom.user.username] = i.forWhom.name
        if i.forWhom.user.username in adj_dictionary:
            adj_dictionary[i.forWhom.user.username].append(i.adjective)
        else:
            adj_dictionary[i.forWhom.user.username] = [i.adjective]

    gen_comments = []

    for c in myComments:
        tmpName=c["forWhom"]
        if User.objects.filter(username = c["forWhom"]).exists():
            tmpName=User.objects.get(username=c["forWhom"]).student.name
        gen_comments.append([c["comment"],c["forWhom"],tmpName])

    adjective_list = [adj[0] for adj in Adjective.adjective_list]

    # Convert to json objects
    comments_json = json.dumps(gen_comments)
    adj_dictionary_json = json.dumps(adj_dictionary)
    adjective_list_json = json.dumps(adjective_list)

    context={"comments":gen_comments, "comments_json": comments_json, "users":users_all, "adjective_list": adjective_list, "adjective_list_json": adjective_list_json, "adj_dictionary": adj_dictionary, "adj_dictionary_json": adj_dictionary_json, "name_dictionary": name_dictionary}

    if request.method=='GET':
        return render(request, 'myapp/comment.html',context)
    
    ## Need it to close based on deadline
    if is_deadline_over():
        return render(request, 'myapp/comment.html', {"comments":gen_comments, "comments_json": comments_json, "users":users_all, "comment": "You can't comment after deadline :(", "adjective_list": adjective_list, "adjective_list_json": adjective_list_json, "adj_dictionary": adj_dictionary, "adj_dictionary_json": adj_dictionary_json, "name_dictionary": name_dictionary})

    for i in range(len(request.POST.getlist('forWhom[]'))):
        lowerEntry = (request.POST.getlist('forWhom[]')[i]).lower()

        for c in u.student.CommentsIWrite:
            if c["forWhom"]==lowerEntry: #updating an already written message
                c["comment"]=request.POST.getlist('val[]')[i]
                # A not found check for the user
                if (User.objects.filter(username = lowerEntry).exists() and (u.username.lower() != lowerEntry)):
                    u_new = User.objects.get(username=lowerEntry)

                    for a in request.POST.getlist('adjectivesSelected'):
                        addAdjective(a,  User.objects.get(username=lowerEntry), u)

                    for a in set(adjective_list)-set(request.POST.getlist('adjectivesSelected')):
                        removeAdjective(a, User.objects.get(username=lowerEntry), u)
                        
                else:
                    return redirect('/comment')
                for c_new in u_new.student.CommentsIGet:
                    if c_new["fromWhom"]==u.username:
                        c_new["comment"]=request.POST.getlist('val[]')[i]
                        break
                u_new.student.save()
                break
        else:
            if request.POST.getlist('val[]')[i] != '':
                u.student.CommentsIWrite.append({"comment":request.POST.getlist('val[]')[i],"forWhom":lowerEntry})
                # A not found check of user and I cant comment for myself
            if (u.username.lower() == lowerEntry):
                return render(request, 'myapp/comment.html', {"comments":gen_comments, "comments_json": comments_json, "users":users_all, "comment": "You can't comment for yourself :)", "adjective_list": adjective_list, "adjective_list_json": adjective_list_json, "adj_dictionary": adj_dictionary, "adj_dictionary_json": adj_dictionary_json, "name_dictionary": name_dictionary})
            if (User.objects.filter(username = lowerEntry).exists()):

                for a in request.POST.getlist('adjectivesSelected'):
                    addAdjective(a,  User.objects.get(username=lowerEntry), u)

                for a in set(adjective_list)-set(request.POST.getlist('adjectivesSelected')):
                    removeAdjective(a, User.objects.get(username=lowerEntry), u)
                    
                u_new = User.objects.get(username=lowerEntry)
            else:
                logger.info((User.objects.filter(username = lowerEntry).exists()))
                return redirect('/comment')

            if request.POST.getlist('val[]')[i] != '':
                u_new.student.CommentsIGet.append({"comment":request.POST.getlist('val[]')[i],"fromWhom":u.username,"displayInPdf":"True"})
            u_new.student.save()
        u.student.save()
    return redirect('/comment')


@login_required
def delete_comment(request, forwhom):
    u = request.user
    forWhom = User.objects.get(username=forwhom)

    for c in u.student.CommentsIWrite:
        if c["forWhom"] == forwhom:
            u.student.CommentsIWrite.remove(c)
            break
    u.student.save()

    for c in forWhom.student.CommentsIGet:
        if c["fromWhom"]==u.username:
            forWhom.student.CommentsIGet.remove(c)
            break
    forWhom.student.save()
    return redirect('/comment')

@login_required
def delete_adjectives(request, forwhom):
    u = request.user
    forWhom = User.objects.get(username=forwhom)
    for adj in u.student.AdjectivesIGive.filter(forWhom=forWhom.student):
        removeAdjective(adj.adjective, forWhom, u)
    return redirect('/comment')


def addAdjective(adjective_txt, forWhom, byWhom):
    for adj in forWhom.student.AdjectivesIGet.all():
        if adj.adjective == adjective_txt: # if someone has already voted for this adjective
            if adj.byWhom.filter(user=byWhom.student.user).exists(): # already voted for that adjective by byWhom
                print("already voted for this adj")
            else:
                adj.byWhom.add(Student.objects.get(user=byWhom.student.user))
                adj.save()
            break
    else:
        # no one has voted for this adjective yet
        a = Adjective(adjective=adjective_txt, forWhom=forWhom.student)
        a.save()
        a.byWhom.add(byWhom.student)
        a.save()


def removeAdjective(adjective_txt, forWhom, byWhom):
    for adj in forWhom.student.AdjectivesIGet.all():
        if adj.adjective == adjective_txt: # if someone has already voted for this adjective
            if adj.byWhom.filter(user=byWhom.student.user).exists(): # already voted for that adjective by byWhom
                adj.byWhom.remove(byWhom.student)
                adj.save()
                if adj.byWhom.count() == 0: # if byWhom was the only voter before
                    adj.delete()
            else:
                print("User has not voted for this adjective")
            break
    else:
        # no one has voted for this adjective yet
        print("Student has no such adjective; Nothing to remove")
    

@login_required()
def otherComment(request):
    u = request.user
    if request.method=='GET':
        myComments = u.student.CommentsIGet
        gen_comments=[]
        for c in myComments:
            tmpName=c["fromWhom"]
            if User.objects.filter(username = c["fromWhom"]).exists():
                tmpName=User.objects.get(username=c["fromWhom"]).student.name
            gen_comments.append([c["comment"],c["fromWhom"],tmpName,c["displayInPdf"]])
        
        if len(gen_comments) == 0 and not u.student.AdjectivesIGet:
            return render(request, 'myapp/no_comment.html')

        context = {"comments": gen_comments}

        return render(request, 'myapp/otherComment.html', context)
    
    ## Need it to stop people from changing view of comments
    if is_deadline_over():
        return deadlineover(request)

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
            "chemical": "Chemical Engineering",
            "civil": "Civil Engineering",
            "cse": "Computer Science and Engineering",
            "ee": "Electrical Engineering",
            "maths": "	Mathematics & Computing",
            "mech": "Mechanical Engineering",
            "physics": "Engineering Physics",
            "textile": "Textile Engineering",
            "dbeb": "Biochemical Engineering and Biotechnology",
            "all": "all"
        }
    if request.user.is_superuser:
        dep = request.GET.get('department')
    else:
        return redirect("https://drive.google.com/drive/u/1/folders/1aZJPdJbGrWiOi56WMVnJWqRtmGpxrr9D")
        dep = request.user.student.department
        
    departmentN=""
    if dep in departmentDic:
        departmentN = departmentDic[dep]
    else:
        departmentN = "all"
    GenQuestions = GenQuestion.objects.all()
    students_dep = Student.objects.filter(department=dep).order_by('name')
    for i in students_dep:
        gen_GenQuestions=list([])
        for q in GenQuestions:
            if ((str(q.id) in i.AnswersAboutMyself) and i.AnswersAboutMyself[str(q.id)]!=""):
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
        for (person,count) in p.votes.items():
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
        for (person,count) in p.votes.items():
            Person=""
            if(User.objects.filter(username=person).exists()):
                Person=User.objects.filter(username=person)[0].student.name
            tmpVotes.append([int(count),Person])
        tmpVotes.sort(reverse=True)
        ind = min(5,len(tmpVotes))
        if ind!=0:
            dep_polls.append([p.poll,tmpVotes[0:ind]])

    context={"students":students_dep,"department":departmentN,"allPolls":all_polls,"deptPolls":dep_polls, "deptDict":departmentDic}
    return render(request, 'myapp/yearbook.html', context)

def display_yearbook(request):
    if AdminTable.objects.first().displayYearbook or request.user.is_superuser:
        return yearbook(request)
    else:
        return comingsoon(request)

def userlogout(request):
    logout(request)
    return redirect("/")

def comingsoon(request):
    return render(request, 'myapp/comingsoon.html')

def is_deadline_over():
    if timezone.now() > AdminTable.objects.first().deadline:
        return True
    else:
        return False

def deadlineover(request):
    return render(request, 'myapp/deadlineover.html')


@login_required()
def closeFriends(request):
    if is_deadline_over():
        return deadlineover(request)

    u = request.user
    UsrObj = Student(name=u.student.name, department=u.student.department,
        DP=u.student.DP, phone=u.student.phone, email=u.student.email,
        oneliner=u.student.oneliner, future=u.student.future, genPic1=u.student.genPic1, genPic2=u.student.genPic2, closeFriends=u.student.closeFriends, closeFriendsPic=u.student.closeFriendsPic)
    users_all = User.objects.filter(is_superuser=False).order_by('username')
    users_json = []
    for user in users_all:
        users_json.append({"id": user.username, "user": user.student.name + " (" + user.username + ")"})

    users_json = json.dumps(users_json)
    curr_close_friends = u.student.closeFriends
    curr_close_friends = ','.join(list(curr_close_friends.keys()))

    if request.method=='GET':   
        context = {"user": UsrObj, "users_json": users_json, "curr_close_friends": curr_close_friends}
        return render(request, 'myapp/closeFriends.html', context)

    u.student.closeFriends = {}
    closeFriends = request.POST.get('closeFriends[]')
    if closeFriends:
        closeFriends = [x.strip() for x in closeFriends.split(',')]
        for friendUserName in closeFriends:
            if User.objects.filter(username=(friendUserName).lower()).exists():
                u.student.closeFriends[friendUserName] = User.objects.get(username=(friendUserName).lower()).student.name

    if(request.FILES.get('closeFriendsPic') != None and int(request.FILES.get('closeFriendsPic').size) < 6000000):
        u.student.closeFriendsPic = request.FILES.get('closeFriendsPic')
        if not (u.student.closeFriendsPic.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            return render(request, 'myapp/profile.html', {"user": UsrObj, "image": "Image should be in .png, .jpg or .jpeg format"})
        extension = u.student.closeFriendsPic.name.lower()[u.student.closeFriendsPic.name.lower().rfind("."):] 
        u.student.closeFriendsPic.name = u.username + extension

    u.student.save()
    return redirect('/closeFriends')

@login_required
def allYearbooks(request):
    print(request.build_absolute_uri())
    return render(request, 'myapp/allYearbooks.html', {})

class PersonalYearbookView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if AdminTable.objects.first().displayYearbook or self.request.user.is_superuser:
            return str(self.request.user) + '_personalYearbook.html'
        else:
            return 'myapp/comingsoon.html'


@login_required
def getPersonalYearbook(request):
    personal_yb = open(settings.BASE_DIR + "/media/collage_and_yearbook_personal/" + str(request.user) + "/final_yearbook_" + str(request.user) + ".pdf", 'rb').read()
    return HttpResponse(personal_yb, content_type='application/pdf')


