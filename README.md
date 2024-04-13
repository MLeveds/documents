# Documento

A repository to read doc's data and parse it into a good loking json format.

Ссылка: https://rwfsh39.ru/

### Инструкция к запуску:
#### Склонируйте репозиторий:
```git clone https://github.com/MLeveds/documents && cd documents```
#### Скопируйте и заполните .env файлы:
```pgsql/.env.example``` <br>
```api/.env.example``` <br>
```ml/.env.example``` <br>
#### Настройте ```nginx/conf.d/app.conf```:
Укажите ваши домены.

Для получения ssl сертификатов, нужно закоментировать строки ssl_certificate и убрать ключевое слово ssl в строках listen 443 ssl.

#### Настройте ```docker-compose.yml```
Укажите домены, для которых нужно получить сертификаты.

#### Запустите приложение
```docker compose up -d``` <br>
После запуска ssl сертификаты будут получены автоматически с помощью Certbot.

#### Перезапустите nginx для включения ssl
В файле ```nginx/conf.d/app.conf``` укажите пути к ssl_сертификатам и включите ssl <br>
```docker compose restart nginx``` <br>

#### Запустите миграции
```docker exec docs_api alembic upgrade head;```
#### Запустите сидеры
```docker exec otiva_fastapi sh -c "export PYTHONPATH=$PYTHONPATH:`pwd` && python src/database/seeders/database_seeder.py"```

