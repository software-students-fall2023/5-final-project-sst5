FROM python:3.10.3-slim-bullseye

WORKDIR /app/web-app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/web-app

EXPOSE 5000

ENV MONGODB_URI="mongodb://mongo:27017/"
ENV MONGODB_DATABASE="database1"

CMD ["python", "./app.py"]