#!/bin/bash

echo "Script starts"

python3 manage.py makemigrations
python3 manage.py migrate

## Creating a default admin table object if it does not already exists
python3 setAdminTable.py

## Add random users
python3 add_random_users.py

## Add superusers
usernames=(
  2018_tester
)

passwords=(
  password
)

for index in ${!usernames[*]}; do 
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); print('User already exists') if User.objects.filter(username='${usernames[$index]}').exists() else User.objects.create_superuser('${usernames[$index]}', '${emails[$index]}', '${passwords[$index]}'); " | python manage.py shell 
done

python3 addPolls.py

exec "$@"