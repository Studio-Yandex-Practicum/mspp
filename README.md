[![MSPP Actions Status](https://github.com/Studio-Yandex-Practicum/mspp/actions/workflows/stage_deploy.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/mspp/actions)
# mspp
## Описание
Бот для «Московской школы профессиональной филантропии»

## Ключевые технологии и библиотеки:
- [Python](https://www.python.org/): 3.11
- [Django](https://www.djangoproject.com/): 4.1.5

## Подготовка окружения для разработки
### Предварительные требования
1. Для управления зависимостями и пакетами в проекте используется **Poetry**. Убедитесь, что у вас [установлен](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) Poetry и ознакомьтесь с его [документацией](https://python-poetry.org/docs/cli/).
2. [Установите](https://docs.docker.com/engine/install/) docker и docker compose.
3. Для автоматизации каждом коммите выполняются pre-commit хуки, перечисленные в файле **.pre-commit-config.yaml**. Если при коммите возникают ошибки, можно запустить хуки вручную и посмотреть сообщения об ошибках при помощи команды:
    ```bash
   pre-commit run --all-files
   ```
4. Создайте `.env` файл в корневой папке проекта и укажите необходимые переменные окружения, по примеру шаблона [.env_example](https://github.com/Studio-Yandex-Practicum/mspp/blob/develop/.env_example).

### Локальный запуск в docker compose
1. Активируйте виртуальное окружение и установите зависимости
    ```bash
    poetry shell
    poetry install


2. Установите pre-commit хуки
    ```bash
    pre-commit install --all
    ```

3. Для запуска локальной версии приложения, состоящей из трех сервисов - backend (Django приложение), postgres (БД PostgreSQL) и nginx (веб-сервер), выполните следующую команду:
    ```bash
    docker compose -f infra/docker-compose_local.yml up -d --build
    ```

4. Для выполнения команд в контейнере backend, используйте следующий формат:

    `docker compose -f infra/docker-compose_local.yml exec backend [COMMAND]`

    Выполните следующие команды:
    ```
    python manage.py migrate # Cоздать миграции
    python manage.py createsuperuser # Cоздать суперпользователя
    python manage.py collectstatic --no-input # Cобрать статику
    ```
5. Для остановки и удаления контейнеров используйте:

    `docker compose -f infra/docker-compose_local.yml down`


6. Для удаления volumes используйте следующий формат команд:
    ```
    docker volume rm postgres_data_local # БД
    docker volume rm static_value_local # статика
    ```

7. Для удаления образов используйте следующий формат команд:
    ```
    docker image rm mspp # образ приложения
    docker image rm postgres:15.2 # postgres
    docker image rm nginx:1.23.3-alpine # nginx
    ```

### Команда для запуска ДБ в docker compose
   ```bash
   docker compose -f infra/docker-compose_db_launch.yml up -d --build
   ```

### Локальный запуск приложения
1. Перейдите в директорию `src` с помощью:
   ```bash
   cd src
   ```

2. Скопируйте статические файлы:
   ```bash
   python manage.py collectstatic
   ```

3. Примените миграции:
   ```bash
   python manage.py migrate
   ```

4. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

5. Запустите проект:
   ```bash
   python manage.py runserver
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
4. В терминале перейти в папку с ngrok
5. Скопировать и выполнить в терминале команду для добавления в ngrok токена авторизации (https://dashboard.ngrok.com/get-started/setup, пункт Connect your account)
    ```bash
    ngrok config add-authtoken <ваш_токен>
    ```
6. Запустить ngrok в терминале
    ```bash
    ngrok http 8000
    ```
7. Из ngrok скопировать url из поля `Forwarding` в константу `WEBHOOK_URL` файла .env

## Команда для заполнения базы тестовыми данными
```bash
python manage.py fill_data
```
## Подключение Google API, использвоание Google-таблиц для хранения данных о заявках.
1. Взаимодействие с Goodle-таблицами оранизовано посредством Google Cloud Platform (https://console.cloud.google.com/projectselector2/home/dashboard) и соответствующих API.
2. Для использования Google Cloud Platform необходим гугл-аккаунт.
3. После авторизации на платформе cоздаём проект в Google Cloud Platform:
    - Нажать на кнопку Create Project в рабочей области.
    - Заполнить форму и нажать Create.
4. Подключаем Google Drive API и Google Sheets API:
    - На плитке APIs нажать кнопку Go to APIs overview.
    - Нажать кнопку Enabled APIs and services или выбрать в меню слева пункт Library.
    - Поочерёдно найти Google Drive API, Google Sheets API и подключить их к проекту.
5. Создаём сервисный аккаунт.
    - Перейти в раздел Credentials.
    - Нажать кнопку Create credentials и выбрать пункт Service account.
    - Заполнить форму, выбрать роль для сервисного (рекомендуется Editor).
    - Ввести адрес вашего личного аккаунта в поле Service account admins role и нажать кнопку Done.
6. Получаем JSON-файл с ключом доступа к сервисному аккаунту:
    - Перейти на экран Credentials, нажмите на строчку с названием вашего сервисного аккаунта/
    - Нажать Keys –> Add Key –> Create New Key.
    - Выбрать формат JSON и нажать Create.
7. Из скачавшегося файла копируем необходимые переменные окружения:
    - PRIVATE_KEY=
    - PRIVATE_KEY_ID=
    - PROJECT_ID=
    - CLIENT_EMAIL=
    - CLIENT_ID=
    - CLIENT_X509_CERT_URL=
    - EMAIL - указываем значение адреса электронной почты гугл-аккаунта, в котром был создан проект.
8. Подключаем таблицы.
    - Создать таблицы  для заявок (https://docs.google.com/spreadsheets)
    - Скопировать id таблиц в соответсвующие переменные:
        - SPREADSHEET_ID_FUND=
        - SPREADSHEET_ID_VOLUNTEER= <br />
    Id можно получить скопировав символьную комбинацию из их URL-адресов (.../d/<"id таблицы">/edit...)
9. Версии API указываются в настроках в константах и должны соответствовать версиям на момент развертывания проекта. Необходимая информация доступна по ссылкам указанным ниже для каждой из констант соответственно.
    - DRIVE_VERS = https://developers.google.com/drive/api/reference/rest/
    - SHEETS_VERS = https://developers.google.com/sheets/api/reference/rest

### Авторы:
[Anton Zelinsky](https://github.com/AntonZelinsky)<br>
[kr0t](https://github.com/kr0t)<br>
<br>
[AlexGriv](https://github.com/AlexGriv)<br>
[Serge Balyaba](https://github.com/erges699)<br>
[Nikita Troshkin](https://github.com/Esedess)<br>
[ivanyuk-vl](https://github.com/ivanyuk-vl)
