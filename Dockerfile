FROM python:3.11

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY server /app/server/
COPY client /app/client/

CMD [ "python3", "server/main.py"]
