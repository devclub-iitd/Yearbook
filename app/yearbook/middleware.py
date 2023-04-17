from django.shortcuts import redirect
from django.urls import reverse_lazy
import jwt
import requests
import json
import time
import re
import logging

from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.http.response import HttpResponse
from django.conf import settings
from myapp.models import Student

SSO_TOKEN = 'token'
REFRESH_TOKEN = 'rememberme'
AUTH_URL = 'https://auth.devclub.in/user/login'
REFRESH_URL = 'https://auth.devclub.in/auth/refresh-token'
PUBLIC_KEY = 'yearbook/public.pem'
MAX_TTL_ALLOWED = 60 * 5
QUERY_PARAM = 'serviceURL'
LOGOUT_PATH = '/logout/'

USER_MODEL = User

# An array of path regexes that will not be processed by the middleware
PUBLIC_PATHS = ['^/public.*','^/$','^/static.*','^/admin', '^/media.*', '^/yearbook'] 

# A dictionary of path regexes mapping to the roles. A user needs to have all roles in order to be authorized
ROLES = {
    '^/admin.*': ['admin']
}

DEFAULT_ROLES = ['iitd_user','yearbook_user']
UNAUTHORIZED_HANDLER = lambda request: HttpResponse("Alas You are out of scope! Go get some more permissions dude",status=401)

code2dept = {
	"ce":"civil",
	"ch":"chemical",
	"cs":"cse",
	"bb":"dbeb",
	"ee":"ee",
	"mt":"maths",
	"me":"mech",
	"ph":"physics",
	"tt":"textile"
}


class SSOMiddleware:
    def __init__(self, get_response):
        self.configure()
        self.get_response = get_response
        self.public_key = open(PUBLIC_KEY,'rb').read()
        self.cookies = None
        
    def __call__(self, request):

        if (request.path == LOGOUT_PATH):
            return self.logout(request)

        try:
            token = request.COOKIES[SSO_TOKEN]
        except:
            token = None

        try:
            rememberme = request.COOKIES[REFRESH_TOKEN]
        except:
            rememberme = None
            

        if(not token and not rememberme):
            logging.info("line 75 (not token and not remember me if statement)")
            return self.redirect(request)
        
        if(token is not None):
            try:
                decoded = jwt.decode(token,self.public_key,algorithms='RS256')
                # logging.info("jwt.decode run successfully")

                if(float(decoded['exp']) - time.time() < MAX_TTL_ALLOWED):
                    decoded['user'] = self.refresh(request=request,token={SSO_TOKEN:token})
                    # logging.info("self.refresh executed")

                if(not self.authorize_roles(request, decoded['user'])):
                    # logging.info("line 88")
                    return UNAUTHORIZED_HANDLER(request)
                self.assign_user(request, decoded['user'])
                logging.info("user assigned")

            except Exception as err:
                # print(err)
                # logging.info("line 95")
                # logging.info(err)
                return self.redirect(request)
        else:
            try:
                decoded = jwt.decode(rememberme,self.public_key,algorithms='RS256')
                user = self.refresh(request,{REFRESH_TOKEN:rememberme})

                if(not self.authorize_roles(request, decoded['user'])):
                    return UNAUTHORIZED_HANDLER(request)
                self.assign_user(request,user_payload=user)

            except Exception as err:
                print(err)
                # logging.info("line 109")
                return self.redirect(request)

        response = self.get_response(request)

        if(self.cookies is not None):
            response._headers['set-cookie1'] = ('Set-Cookie',self.cookies.split('\n')[0])
            try:
                response._headers['set-cookie2'] = ('Set-Cookie', self.cookies.split('\n')[1])
            except:
                pass
            
            self.cookies = None

        return response

    def configure(self):
        for key, value in globals().items():
            if(key.isupper()):
                new_val = getattr(settings, key, value)
                if(type(new_val) != type(value)):
                    err = f"Type Mismatch, {key} should be of {type(value)} but found as {type(new_val)}"
                    raise TypeError(err)
                globals()[key] = new_val

    def assign_user(self,request,user_payload):
        if(request.user.is_authenticated):
            return
        try:
            user = USER_MODEL.objects.get(email=user_payload['email'])
        except:
            user = USER_MODEL.objects.create_user(email=user_payload['email'],username=user_payload['username'])
        
            user.first_name = user_payload['firstname']
            user.last_name = user_payload['lastname']
            user.username = user_payload['username']
            user.save()
            code = user_payload['username'][:2]
            s = Student(name=user_payload['firstname'],department=code2dept[code])
            user.student = s
            user.student.save()
        login(request, user)
    
    def authorize_roles(self,request,user_payload):
        if(len(ROLES.keys()) == 0 or match_regex_list(request.path, PUBLIC_PATHS)):
            return True
        try:
            user_roles = user_payload['roles']
        except:
            return False
            
        match = match_regex_list(request.path, ROLES.keys())
        if(match is None):
            reqd_roles = DEFAULT_ROLES
        else:
            reqd_roles = ROLES[match]
        
        for role in reqd_roles:
            if(role not in user_roles):
                return False
        
        return True
        
    
    def refresh(self,request,token):
        r=requests.post(REFRESH_URL,data=token)
        self.cookies = r.headers['Set-Cookie'].replace('Lax,','Lax\n')
        return json.loads(r.text)['user']

    def logout(self,request):
        logout(request)
        response = self.get_response(request)
        response.delete_cookie(SSO_TOKEN,domain='devclub.in')
        response.delete_cookie(REFRESH_TOKEN,domain='devclub.in')
        return response
    
    def redirect(self,request):
        if(match_regex_list(request.path,PUBLIC_PATHS)):
            return self.get_response(request)
        logging.info(f"request: {request}")
        logging.info("inside redirect function, line 189")
        return redirect(AUTH_URL+f"/?{QUERY_PARAM}={re.sub(r'vm2-internal','devclub.in',request.build_absolute_uri()).replace('http','https')}")


def match_regex_list(key,regex_array):
    """ Match every  regex element in an array against the key"""
    for regex in regex_array:
        if(re.search(regex,key) is not None):
            return regex
    return None