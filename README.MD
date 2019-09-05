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
CREATE DATABASE moepex;
CREATE USER moepex WITH PASSWORD 'moepex';
ALTER ROLE moepex SET client_encoding TO 'utf8';
ALTER ROLE moepex SET default_transaction_isolation TO 'read committed';
ALTER ROLE moepex SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE moepex TO moepex;
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
git checkout prod
```


Virtualenv
```bash
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
cd /webapps/
virtualenv envmoepex
source /webapps/envmoepex/bin/activate
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
_sudo vim /etc/systemd/system/moepex-gunicorn.socket_
```bash
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/moepex-gunicorn.sock

[Install]
WantedBy=sockets.target
```



Gunicorn Service File
_sudo vim /etc/systemd/system/moepex-gunicorn.service_
```bash
[Unit]
Description=gunicorn daemon
Requires=moepex-gunicorn.socket
After=network.target

[Service]
User=ifrs
Group=www-data
WorkingDirectory=/webapps/moepex/
ExecStart=/webapps/envmoepex/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/moepex-gunicorn.sock \
          project.wsgi:application

[Install]
WantedBy=multi-user.target
```


Gunicorn Service
```
sudo systemctl start moepex-gunicorn.socket
sudo systemctl enable moepex-gunicorn.socket
sudo systemctl status moepex-gunicorn.socket
file /run/moepex-gunicorn.sock
sudo journalctl -u moepex-gunicorn.socket
sudo systemctl status moepex-gunicorn
curl --unix-socket /run/moepex-gunicorn.sock localhost
sudo systemctl status moepex-gunicorn
sudo journalctl -u moepex-gunicorn
sudo systemctl daemon-reload
sudo systemctl restart moepex-gunicorn
```


NGINX File
_sudo vim /etc/nginx/sites-available/moepex_
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
        proxy_pass http://unix:/run/moepex-gunicorn.sock;
    }
}
```


NGINX Service
```
sudo ln -s /etc/nginx/sites-available/moepex /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
```


Deploys
```
cd /webapps/
source envmoepex/bin/activate
cd moepex
git pull
pip install -r moepex/project/requeriments_prod.txt
python manage.py migrate
python manage.py collectstatic
sudo systemctl restart moepex-gunicorn
sudo systemctl restart nginx
```
