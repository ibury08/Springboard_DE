FROM python:3.7-alpine

COPY . /tmp
WORKDIR /tmp
RUN apk add netcat-openbsd
RUN pip3 install -r ./requirements.txt
RUN ["chmod", "+x", "./wait-for.sh"]
#ENTRYPOINT [ "./entry.sh" ]