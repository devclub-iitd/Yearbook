import django
django.setup()

from django.contrib.auth import get_user_model
from myapp.models import *

User = get_user_model()

print("Adding random users...")

for i in range(800):
    student_name = '2017_student_' + str(i)
    if not User.objects.filter(username=student_name).exists():
        user = User.objects.create_user(username=student_name,
                                    email=student_name + '@gmail.com',
                                    password='password')
        user.student = Student(name=student_name, department='cse')
        user.student.save()