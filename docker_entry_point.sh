#!/bin/bash

echo "Script starts"

# until psql $DATABASE_URL -c '\l'; do
# 	>&2 echo "Postgres is unavailable - sleeping"
# 	sleep 1
# done

psql $DATABASE_URL -c '\l' -v ON_ERROR_STOP=1 <<-EOSQL
    CREATE DATABASE $POSTGRES_DB;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL

python3 Scrape/Scrape.py
python3 CsvToDatabase.py
python3 manage.py makemigrations
python3 manage.py migrate
#move to .env
./yearbook_superuser.sh
echo "Starting WEB Server"
# gunicorn bookShelf.wsgi:application --bind 0.0.0.0:$PORT --workers 3
python3 manage.py runserver 0.0.0.0:$DEPLOY_PORT

echo "Script complete"

exec "$@"
