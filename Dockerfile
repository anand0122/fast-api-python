FROM python:latest
LABEL Maintainer="Anand Dubey"
WORKDIR /usr/app/src
COPY ./ ./
CMD [ "python", "./main.py"]