FROM python:3.11-slim

WORKDIR /app

COPY ../requirements/development.txt requirements/development.txt

RUN python -m pip install --upgrade pip
RUN pip install -r requirements/development.txt

COPY . .

CMD ["uvicorn ", "config.asgi:application"]
