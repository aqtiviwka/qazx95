1. Зайти по SSH на свой сервер root@“Ваш ip“
Создать нового юзера adduser „name“ — где name имя создаваемого пользователя
Заполнить все необходимые поля
Обновить пакеты apt upgrade

 Дать права юзеру usermod -aG „name“
 Сменить юзера su „name“
 Установить необходимые пакеты sudo apt install nginx git supervisor

 2. УСТАНОВИМ MYSQL

 wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb
 sudo dpkg -i mysql-apt-config_0.8.29-1_all.deb
 sudo mysql_secure_installation
 mysql -u root -p
 CREATE DATABASE data;
 CREATE USER „name“@“%“ IDENTIFIED BY „pass“;
 GRANT ALL PRIVILEGES ON data.* TO 'name'@'%';

3. Создать папку code:  mkdir code
 Создать папку с проектом qazx95: mkdir qazx95
 Создать виртуальное окружение: python3.10 -m venv venv
 Загрузить проект из гитхаб: git clone „url“
 Активировать виртуальное окружение:  source venv/bin/activate
 Подтянуть из файла requirements.txt все зависимости: pip install -r       requirements.txt
 Установить gunicorn: pip instal gunicorn

4. Создать файл gunicorn_config.py и внести следующие изменения

 command = '/home/dima/code/qazx95/venv/bin/gunicorn'
 pythonpath = 'home/dima/code/qazx95/'
 bind = '127.0.0.1:8001'
 workers = 3
 user = 'dima'
 limit_request_fields = 20000
 limit_request_fiels_size = 0
 raw_env = 'DJANGO_SETTINGS_MODULE=qazx95.settings'

5. Создадим папку bin ней файл start_gunicorn.sh

source /home/dima/code/qazx95/venv/bin/activate
exec gunicorn -c '/home/dima/code/qazx95/gunicorn_config.py' qazx95.wsgi

Выполнить команду chmod +x bin/start_gunicorn.sh

6. Перейдем в директорию etc/nginx/sites_enabled/ и изменим файл defaut:

server {
	listen 80 default_server;
  listen [::]:80 default_server;
	server_name  _;
	location / {
                	proxy_pass http://127.0.0.1:8001;
                  proxy_set_header X-Forwarded-Host $server_name
                	proxy_set_header X-Real-IP $remote_addr;
                	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        	}
}

7. Настроим супервизор
Открываем фаил etc/supervisor/conf.d/qazx95.conf

[program:gunicorn]
command=/home/dima/code/qazx95/bin/start_gunicorn.sh
user=dima
process_name=%(program_name)s
numproc=1
autostart=1
autorestart=1
redirect_stderr=true

перезапускаем супервизор
sudo service supervisor stop
sudo service supervisor start
