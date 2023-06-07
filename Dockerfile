FROM python:3.8.10
ENV PYTHONUNBUFFERED=1
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .