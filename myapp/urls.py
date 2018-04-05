from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.userlogout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^changePassword/$', views.changePassword, name='changePassword'),

]