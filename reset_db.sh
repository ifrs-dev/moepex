rm -f project/db.sqlite3

./manage.py makemigrations
./manage.py migrate

./manage.py loaddata ~/users.json
