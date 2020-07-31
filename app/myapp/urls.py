from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

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
    url(r'^yearbook/$', views.display_yearbook, name='yearbook'),
    url(r'^closeFriends/$', views.closeFriends, name='closeFriends'),
    url(r'^personalYearbook/$', views.PersonalYearbookView.as_view(), name="personalYearbook"),
    url(r'^allYearbooks/$', views.allYearbooks, name="allYearbooks"),
    path('delete-image/<type>', views.delete_image, name="delete_image"),
    path('delete-comment/<forwhom>', views.delete_comment, name="delete_comment"),
    path('delete-adjectives/<forwhom>', views.delete_adjectives, name="delete_adjectives"),
    # url(r'^yearbook/$', views.yearbook, name='yearbook'),
    # url(r'^yearbook/$', views.comingsoon, name='yearbook'),
]
