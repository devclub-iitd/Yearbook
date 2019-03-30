#!/bin/bash

echo "Script starts"

until psql -p $db_port -h 0.0.0.0 -c '\l' -d $database -U $user; do
	>&2 echo "Postgres is unavailable - sleeping"
	sleep 1
done

python3 Scrape/Scrape.py
python3 Scrape/CsvToDatabase.py
python3 manage.py makemigrations
python3 manage.py migrate
#move to .env
./yearbook_superuser.sh
echo "Starting WEB Server"
# gunicorn bookShelf.wsgi:application --bind 0.0.0.0:$PORT --workers 3
python3 manage.py runserver 0.0.0.0:$DEPLOY_PORT

echo "Script complete"

exec "$@"
