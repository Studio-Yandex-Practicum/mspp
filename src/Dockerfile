FROM python:3.11-slim

WORKDIR /app

COPY ../requirements/*.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r development.txt

COPY . .

CMD ["uvicorn ", "config.asgi:application"]
