## Тестовый проект Stripe + Django

**Тестовое задание по технологии Stripe**

Задание выполнено и находится на виртуальном сервере:

    http://54.37.142.109

# В полном объеме реализованны следующие пункты:

        -Django Модель Item с полями (name, description, price)
        -API с двумя методами:
        -GET /buy/{id} и	GET /item/{id},
        -Использование environment variables(библиотека python-dotenv)
        -Просмотр Django Моделей в Django Admin панели(с настройками фильтрации, поиска)
        -Модель Order, для оплаты по нескольким товарам одновременно
        -Модели Discount, Tax также реализованы в панели Admin (можно выставлять налог в процентах, 
            который будет применяться к каждому заказу Item или Order)
        -Добавить поле Item.currency. Создание двух пар тестовых ключей для данной задачи 
            невозможно на одном акаунте Stripe и я нашел другое решение
            (во время оплаты заказа Order можно выбрать валюту USD или EUR)

Нереализованые задачи:

        -Запуск используя Docker(локально докер работает, но не смог его заставить работать на сервере,
            потерял много времени. До этого с докером не работал)
        -Реализовать не Stripe Session, а Stripe Payment Intent.(нехватило времени на реализацию)

# Установка проекта

**Клонирование репозитория:**

    git clone https://github.com/Yar417/Negodenko_Stripe_api.git 

**Переименование в www прокта, чтобы проще переходить из папки в папку:**

    mv Negodenko_Stripe_api www ; cd www

**Создание файла с ключами .env**

    nano .env

**Наполнение файла**

    SECRET_KEY = ''
    STRIPE_PUBLISHABLE_KEY = ''
    STRIPE_SECRET_KEY = ''

**Далее команды выполняются одна за другой:**

    sudo apt update ; sudo apt upgrade
    sudo apt install python3-pip python3-dev libpq-dev nginx curl
    python3 -m venv venv
    . ./venv/bin/activate
	pip install -r requirements.txt
    cd webapp/src 
    python manage.py runserver 127.0.0.1:3000

**Из второго терминала проверка (ожидаем код 200)**

	curl http://127.0.0.1:3000/

**Продолжаем с первым терминалом:**

    python manage.py makemigration
    python manage.py migrate
    python manage.py collectstatic

**NGINX:**

    NGINX
	sudo apt-get install nginx
	service nginx restart

	cd /etc/nginx

**Настройка nginx.conf**

**Команда для написания файла**

    nano nginx.conf

**Копируем и вставляем текст**

    user www-data;
		worker_processes auto;
		pid /run/nginx.pid;
		include /etc/nginx/modules-enabled/*.conf;
		events {
		        worker_connections 768;
		}
		http {
			server {
			    listen 80;
			    server_name 102563.ip-ns.net;

			    location / {
		        include proxy_params;
		        proxy_pass http://unix:/run/gunicorn.sock;
		        }

		        location = /favicon.ico {
		        access_log off;
		        log_not_found off;
		        return 204;
		        }

			    location /staic {
	        		root /root/www/src;
			    }
			}
		}

**Далее команды перезапуска NGINX и проверки статуса работы**

    service nginx restart
    systemctl status nginx.service

**GUNICORN**

Установка только в окружении ENV, при установке глобально - дает ошибку.

	which gunicorn
	/root/www/venv/bin/gunicorn (должно быть так!)

**из папки проекта:**

	gunicorn --bind 0.0.0.0:8000 proj.wsgi

**Добавление пользователя**

Пользователь, которого мы выбираем для gunicorn .service, должен быть членом группы www-data,
поэтому мы сначала проверяем членов этой группы с помощью следующей команды:

	grep ^www-data /etc/group

**Если пользователя root нет:**

	(пример)sudo adduser {USER-NAME-HERE} {GROUP-NAME-HERE}
	sudo adduser root www-data

**Сокет Gunicorn**

	sudo nano /etc/systemd/system/gunicorn.socket

**Текст для сокета**

	[Unit]
	Description=gunicorn socket

	[Socket]
	ListenStream=/run/gunicorn.sock

	[Install]
	WantedBy=sockets.target		

**Стартуем сокет**

	sudo systemctl start gunicorn.socket

**Если нужно отключить**

	sudo systemctl enable gunicorn.socket		

**Сервис Gunicorn**

	sudo nano /etc/systemd/system/gunicorn.service

**Текст**

	gunicorn.service
	[Unit]
	Description=gunicorn daemon
	Requires=gunicorn.socket
	After=network.target

	[Service]
	User=root
	Group=www-data
	WorkingDirectory=/root/www/webapp/src
	ExecStart=/root/www/venv/bin/gunicorn \
			  --access-logfile - \
			  --workers 3 \
			  --bind unix:/run/gunicorn.sock \
			  proj.wsgi:application

	[Install]
	WantedBy=multi-user.target

**Просто делаем по порядку и проверяем состояния работы:**

	sudo systemctl status gunicorn.service
	sudo systemctl restart gunicorn.service

	sudo systemctl daemon-reload

	sudo systemctl start gunicorn.socket
	sudo systemctl enable gunicorn.socket

	sudo systemctl status gunicorn
	sudo journalctl -u gunicorn

	sudo systemctl restart gunicorn
    service nginx restart

**Не работает статика в админке? Используем WhiteNoise**

	http://whitenoise.evans.io/en/latest/

**Технологический стек проекта:**

    Ubuntu 20.4
    Django
    Stripe
    Gunicorn
    Nginx

**Дополнительные библиотеки:**

	python-dotenv
	WhiteNoise

Спасибо за интересное задание