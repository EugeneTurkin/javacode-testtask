# javacode-testtask


## Системные требования

[Poetry](https://python-poetry.org/docs/#installation)


## First time setup

Следуйте командам ниже чтобы развернуть проект для разработки (или проверки)

Перейдите в корневую папку проекта

1. Создайте виртуальное окружение и установите зависимости
```bash
poetry install --with app
```

2. Активируйте виртуальное окружение
```bash
poetry shell
```


## Запуск приложения

1. Запустите приложение локально
```bash
# Миграции накатятся через энтрипоинт в компоузе.
docker compose -f envs/local/dev/docker-compose.yml up -d
```

2. Проверьте работу приложения
```bash
curl --request GET http://localhost:8000/

# ссылка на Swagger
http://localhost:8000/docs
```
