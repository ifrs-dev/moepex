### Deploy
[Source](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04#checking-for-the-gunicorn-socket-file)



Requisitos do sistema
```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl htop git vim
```


Banco de dados
```bash
sudo -u postgres psql
CREATE DATABASE moepex2019;
CREATE USER moepex2019 WITH PASSWORD 'moepex2019';
ALTER ROLE moepex2019 SET client_encoding TO 'utf8';
ALTER ROLE moepex2019 SET default_transaction_isolation TO 'read committed';
ALTER ROLE moepex2019 SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE moepex2019 TO moepex2019;
\q
```


Acesso SSH
```bash
ssh-keygen
cat ~/.ssh/id_rsa.pub
```
Adicionar chave em: https://github.com/ifrs-dev/moepex/settings/keys


Repositório
```bash
sudo mkdir /webapps/
sudo chown ifrs /webapps/
cd /webapps/
git clone git@github.com:ifrs-dev/moepex.git
cd /webapps/moepex/
git fetch
git checkout prod2019
```


Virtualenv
```bash
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
cd /webapps/
virtualenv envmoepex2019
source /webapps/envmoepex2019/bin/activate
pip install -r /webapps/moepex/project/requeriments_prod.txt
```


Database
```bash
cd /webapps/moepex/
python manage.py makemigrations
python manage.py migrate
```


Test app
```bash
cd /webapps/moepex/
sudo ufw allow 8000
python manage.py runserver 0.0.0.0:8000
python manage.py createsuperuser
gunicorn --bind 0.0.0.0:8000 project.wsgi
sudo ufw delete allow 8000
deactivate
```



Gunicorn Service File
_sudo vim /etc/systemd/system/moepex2019-gunicorn.socket_
```bash
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/moepex2019-gunicorn.sock

[Install]
WantedBy=sockets.target
```



Gunicorn Service File
_sudo vim /etc/systemd/system/moepex2019-gunicorn.service_
```bash
[Unit]
Description=gunicorn daemon
Requires=moepex2019-gunicorn.socket
After=network.target

[Service]
User=ifrs
Group=www-data
WorkingDirectory=/webapps/moepex/
ExecStart=/webapps/envmoepex2019/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/moepex2019-gunicorn.sock \
          project.wsgi:application

[Install]
WantedBy=multi-user.target
```


Gunicorn Service
```
sudo systemctl start moepex2019-gunicorn.socket
sudo systemctl enable moepex2019-gunicorn.socket
sudo systemctl status moepex2019-gunicorn.socket
file /run/moepex2019-gunicorn.sock
sudo journalctl -u moepex2019-gunicorn.socket
sudo systemctl status moepex2019-gunicorn
curl --unix-socket /run/moepex2019-gunicorn.sock localhost
sudo systemctl status moepex2019-gunicorn
sudo journalctl -u moepex2019-gunicorn
sudo systemctl daemon-reload
sudo systemctl restart moepex2019-gunicorn
```


NGINX File
_sudo vim /etc/nginx/sites-available/moepex2019_
```bash
server {
    listen 80;
    server_name moepex.ibiruba.ifrs.edu.br;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /webapps/moepex/project/static/;
    }

    location /arquivos/ {
        root /webapps/moepex/project/arquivos/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/moepex2019-gunicorn.sock;
    }
}
```


NGINX Service
```
sudo ln -s /etc/nginx/sites-available/moepex2019 /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
```


Deploys
```
cd /webapps/
source envmoepex2019/bin/activate
cd moepex2019
git pull
pip install -r moepex2019/project/requeriments_prod.txt
python manage.py migrate
python manage.py collectstatic
sudo systemctl restart moepex2019-gunicorn
sudo systemctl restart nginx
```
