FROM python:latest
LABEL Maintainer="Anand Dubey"
WORKDIR /usr/app/src
COPY ./ ./
RUN pip install fastapi
RUN pip install "uvicorn[standard]"
RUN pip install prometheus-client
EXPOSE 8085
EXPOSE 8086
CMD [ "python", "./main.py"]