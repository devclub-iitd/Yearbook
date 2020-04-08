#!/bin/bash
clear
PROJECT="/home/devclub/Projects/yearbook"
cd $PROJECT
. venv/bin/activate  #Activate your virtual environment
python manage.py runserver localhost:5060 #run django server

