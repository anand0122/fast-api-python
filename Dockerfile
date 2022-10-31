FROM python:latest
LABEL Maintainer="Anand Dubey"
WORKDIR /usr/app/src
COPY ./ ./
EXPOSE 8085
EXPOSE 8086
CMD [ "python", "./main.py"]