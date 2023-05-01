FROM python:3.11

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_ENV="production"

EXPOSE 80

ENTRYPOINT ["python", "./app.py"]