# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User,Group
from .models import GenQuestion, Poll, Student


# Define an inline admin descriptor for Student model
# which acts a bit like a singleton

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,)
# class StudentAdmin(admin.ModelAdmin):
# 	inlines = (ImageInline,)

# Register your models here.
admin.site.register(Poll)
admin.site.register(GenQuestion)
admin.site.unregister(User)
admin.site.register(User, UserAdmin,)
admin.site.unregister(Group)
