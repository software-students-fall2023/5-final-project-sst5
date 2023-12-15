FROM python:3.10.3-slim-bullseye

WORKDIR /app/web-app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/web-app

EXPOSE 5000

CMD ["python", "./app.py"]