# mspp

## Описание
Бот для «Московской школы профессиональной филантропии»


## Ключевые технологии и библиотеки:
- [Python](https://www.python.org/); 3.9
- [Django](https://www.djangoproject.com/); 4.1.5



### Шаблон наполнения env-файла:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
SECRET_KEY = ''
ALLOWED_HOSTS=example.com
```

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

При каждом коммите выполняются хуки (автоматизации) перечисленные в **.pre-commit-config.yaml**. [Документация pre-commit](https://pre-commit.com)
Если не понятно какая ошибка мешает сделать коммит можно запустить хуки вручную и посмотреть ошибки:
    ```shell
    pre-commit run --all-files
    ```

Если вы используете linux-систему можете использовать make:
    ```shell
    make first_start: # Начальная инициализация
    make pre-commit: # Проверки pre-commit
    make up: # Запустить env
    make down: # Выйти из env
    ```


### Авторы:



AlexGriv https://github.com/AlexGriv
