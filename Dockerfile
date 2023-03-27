FROM python:3.11-slim

WORKDIR /app

COPY /requirements requirements/

RUN mkdir -p logs
RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements/development.txt --no-cache-dir

COPY ./src .

RUN chmod +x start.sh

CMD ["./start.sh"]
# CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
