FROM python:3.8-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

ENV PYTHONUNBUFFERED=1
ENV MONGO_URI="mongodb://mongo:27017"
ENV MONGO_DB="students_db"
ENV MONGO_COLLECTION="students"

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]