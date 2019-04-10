#!/bin/bash

echo "Script starts"

until psql $POSTGRES_HOST_URL -c '\l'; do
 	>&2 echo "Postgres is unavailable - sleeping"
 	sleep 1
done

if psql $POSTGRES_HOST_URL -lqt | cut -d \| -f 1 | grep -qw $POSTGRES_DB; then
    echo "DATABASE "$POSTGRES_DB" already exists"
else
    echo "DATABASE "$POSTGRES_DB" does not exists, creating DB"
   	psql $POSTGRES_HOST_URL -c "CREATE DATABASE $POSTGRES_DB ;"
   	psql $POSTGRES_HOST_URL -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER ;"
   	psql $POSTGRES_HOST_URL -l
fi

python3 manage.py makemigrations
python3 manage.py migrate
./yearbook_superuser.sh

## Add Users
python3 Scrape/Scrape.py
python3 CsvToDatabase.py
python3 addPolls.py


echo "Starting WEB Server"
python3 manage.py runserver 0.0.0.0:$DEPLOY_PORT

echo "Script complete"

