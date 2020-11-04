FROM python:3.8-buster
COPY . /app
RUN apt update
RUN apt install -y python3-opencv libzbar0
RUN pip3 install -r ./app/requirements.txt
EXPOSE 80
CMD python3 /app/server.py
