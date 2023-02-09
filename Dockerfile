FROM python:3.11-slim

WORKDIR /app

COPY /requirements requirements/

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements/development.txt

COPY ./src .

CMD ["uvicorn", "config.asgi:application", "--host", "51.250.96.71", "--bind", "0:8080"]
