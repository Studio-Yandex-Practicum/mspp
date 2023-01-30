# mspp

## Описание
Бот для «Московской школы профессиональной филантропии»


## Ключевые технологии и библиотеки:
- [Python](https://www.python.org/); 3.11
- [Django](https://www.djangoproject.com/); 4.1.5



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

## Запуск
1. Перейдите в директорию src
    ```bash
    cd src
    ```
2. Запустите проект
    ```bash
    uvicorn config.asgi:application
    ```

### Авторы:

[Anton Zelinsky](https://github.com/AntonZelinsky)

[kr0t](https://github.com/kr0t)

---

[AlexGriv](https://github.com/AlexGriv)

[Serge Balyaba](https://github.com/erges699)

[Nikita Troshkin](https://github.com/Esedess)

[ivanyuk-vl](https://github.com/ivanyuk-vl)
