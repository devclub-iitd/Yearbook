from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.userlogout, name='logout'),
    # url(r'^changePassword/$', views.changePassword, name='changePassword'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^answer/$', views.answerMyself, name='answer'),
    url(r'^poll/$', views.poll, name='poll'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^otherComment/$', views.otherComment, name='otherComment'),
    url(r'^auth/$', views.authenticate, name='otherComment'),
    # url(r'^yearbook/$', views.yearbook, name='yearbook'),    
    url(r'^yearbook/$', views.comingsoon, name='yearbook'),    
]
