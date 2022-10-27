FROM python:latest
LABEL Maintainer="Anand Dubey"
WORKDIR /usr/app/src
COPY ./ ./
EXPOSE 8085
CMD [ "python", "./main.py"]