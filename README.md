[![MSPP Actions Status](https://github.com/Studio-Yandex-Practicum/mspp/actions/workflows/stage_deploy.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/mspp/actions)

[![MSPP Actions Status](https://github.com/Studio-Yandex-Practicum/mspp/actions/workflows/stage_deploy.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/mspp/actions)
# mspp

## Описание
Бот для «Московской школы профессиональной филантропии»


## Ключевые технологии и библиотеки:
- [Python](https://www.python.org/): 3.11
- [Django](https://www.djangoproject.com/): 4.1.5


## Шаблон наполнения env-файла


  `env_example`

- Обязательно<br>
`TELEGRAM_TOKEN`<br>
`PostgreSQL environment variables`<br>
- Остальное опционально.<br>
  - Django<br>
  `ALLOWED_HOSTS=[]`<br>
  `CSRF_TRUSTED_ORIGINS=[]`<br>
  `DEBUG=True`<br>
  `SECRET_KEY=""`<br>
  - Telegram<br>
  `TELEGRAM_TOKEN=`<br>
  `WEBHOOK_MODE=False`<br>
  `WEBHOOK_URL=`<br>
  - Google<br>
  `LOGGING_LEVEL="DEBUG"`<br>
  `EMAIL="example@mail.com"`<br>
  - ID Google таблицы для добавления данных<br>
  `SPREADSHEET_ID=""`<br>
  - Данные сервисного аккаунта<br>
  `PROJECT_ID=""`<br>
  `PRIVATE_KEY_ID=""`<br>
  `PRIVATE_KEY=""`<br>
  `CLIENT_EMAIL=""`<br>
  `CLIENT_ID=""`<br>
  `CLIENT_X509_CERT_URL=""`<br>
  - PostgreSQL environment variables<br>
  `POSTGRES_DB=mspp`<br>
  `POSTGRES_USER=mspp`<br>
  `POSTGRES_PASSWORD=pg_password`<br>
  `POSTGRES_HOST=postgres`<br>
  `POSTGRES_PORT=5432`<br>
  ---
</details>

## Установка
1. Зависимости и пакеты управляются через **poetry**. Убедитесь, что **poetry** [установлен](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) на вашем компьютере и ознакомьтесь с [документацией](https://python-poetry.org/docs/cli/).
2. Активируйте виртуальное окружение.
    ```bash
    poetry shell
    ```
3. Установите зависимости.
    ```bash
    poetry install
    ```
4. Установите pre-commit хуки
    ```bash
    pre-commit install --all
    ```

При каждом коммите выполняются хуки (автоматизации) перечисленные в **.pre-commit-config.yaml**. [Документация pre-commit](https://pre-commit.com)
Если не понятно какая ошибка мешает сделать коммит можно запустить хуки вручную и посмотреть ошибки:
    ```bash
    pre-commit run --all-files
    ```
## Режим работы бота
### Polling
Для запуска бота в режиме polling задайте в файле .env значение `False` для константы `WEBHOOK_MODE`
```
WEBHOOK_MODE=False
```

### Webhook
Для запуска бота в режиме webhook задайте в файле .env значение `True` для константы `WEBHOOK_MODE`, также необходимо указать URL сайта, на котором развернут проект, в константе `WEBHOOK_URL`
```
WEBHOOK_MODE=True
WEBHOOK_URL=https://example.com
```


#### Локальный запуск webhook

  Для локального запуска бота в режиме webhook можно использовать приложение [ngrok](https://ngrok.com/)

  1. [Скачать](https://ngrok.com/download) и установить ngrok<br>
  2. [Зарегистрировать](https://dashboard.ngrok.com/signup) учетную запись<br>
  3. [Авторизоваться](https://dashboard.ngrok.com/login)
  4. В термминале перейти в папку с ngrok
  5. Скопировать и выполнить в терминале команду для добавления в ngrok токена авторизации (https://dashboard.ngrok.com/get-started/setup, пункт Connect your account)
  ```bash
  ngrok config add-authtoken <ваш_токен>
  ```
  6. Запустить ngrok в терминале
  ```bash
  ngrok http 8000
  ```
  7. Из ngrok cкопировать url из поля `Forwarding` в константу `WEBHOOK_URL` файла .env

<br>

## Локальный запуск

### Запуск в docker'е

  [Установить](https://docs.docker.com/engine/install/) docker и docker compose
  Добавить TELEGRAM_TOKEN в .env_local

 - Запустить локально<br>
  `docker compose -f infra/docker-compose_local.yml up` - с выводом в консоль
  `docker compose -f infra/docker-compose_local.yml up -d` - в тихом режиме<br>
  `docker compose -f infra/docker-compose_local.yml up --build` - пересобрать после внесения изменений<br>
  `docker compose -f infra/docker-compose_local.yml up -d --build` - пересобрать в тихом режиме<br>

  - Создать миграции<br>
  `docker compose -f infra/docker-compose_local.yml exec backend python manage.py migrate`<br>

  - Создать суперпользователя<br>
  `docker compose -f infra/docker-compose_local.yml exec backend python manage.py createsuperuser`<br>

  - Собрать статику<br>
  `docker compose -f infra/docker-compose_local.yml exec backend python manage.py collectstatic --no-input`<br>

  - Остановить<br>
  `docker compose -f infra/docker-compose_local.yml down` - остановить и удалить контейнеры<br>
  `docker compose -f infra/docker-compose_local.yml down -v` - остановить и удалить все кроме образов<br>

  - Удалить volumes<br>
  `docker volume rm postgres_data_local` - БД<br>
  `docker volume rm static_value_local` - статика<br>

  - Удалить образы<br>
  `docker image rm mspp` - образ приложения<br>
  `docker image rm postgres:15.2` - postgres<br>
  `docker image rm nginx:1.23.3-alpine` - nginx<br>
<br>

###  Запуск контейнера DB, запуск приложения локально для более удобной разработки

<br>

  1. Запустите контейнер DB `docker compose -f infra/docker-compose_db_launch.yml up -d --build`
  2. Перейдите в директорию src `cd src`
  3. Скопируйте статические файлы `python manage.py collectstatic`
  4. Примените миграции `python manage.py migrate`
  5. Создайте суперпользователя `python manage.py createsuperuser`
  6. Запустите проект `python manage.py startserver`


<br>


## Команда для заполнения базы тестовыми данными
```bash
python manage.py fill_data
```

### Авторы:

[Anton Zelinsky](https://github.com/AntonZelinsky)<br>
[kr0t](https://github.com/kr0t)<br>
<br>
[AlexGriv](https://github.com/AlexGriv)<br>
[Serge Balyaba](https://github.com/erges699)<br>
[Nikita Troshkin](https://github.com/Esedess)<br>
[ivanyuk-vl](https://github.com/ivanyuk-vl)
