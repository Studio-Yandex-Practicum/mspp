# mspp

## Описание
Бот для «Московской школы профессиональной филантропии»


## Ключевые технологии и библиотеки:
- [Python](https://www.python.org/): 3.11
- [Django](https://www.djangoproject.com/): 4.1.5



### Шаблон наполнения env-файла:
```

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

<details>
  <summary>Локальный запуск webhook</summary>

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
</details>


## Запуск
1. Перейдите в директорию src
    ```bash
    cd src
    ```
2. Скопируйте статические файлы
    ```bash
    python manage.py collectstatic
    ```
3. Примените миграции
    ```bash
    python manage.py migrate
    ```
4. Создайте суперпользователя
    ```bash
    python manage.py createsuperuser
    ```
5. Запустите проект
    ```bash
    uvicorn config.asgi:application
    ```

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
