FROM mongo:latest

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install pymongo pandas

WORKDIR /usr/src/app

COPY pokedex.csv /usr/src/app/pokedex.csv
COPY preload_db.py /usr/src/app/preload_db.py

EXPOSE 27017

CMD mongod --bind_ip_all & sleep 10 && python3 preload_db.py && tail -f /dev/null
