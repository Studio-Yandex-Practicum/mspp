FROM python:3.11-slim

COPY ../requirements/ requirements/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements/development.txt

COPY ../src/ .

WORKDIR /src

CMD ["uvicorn ", "config.asgi:application"]
