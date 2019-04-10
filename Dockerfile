# Start with a Python image.
FROM python:3.6

RUN apt-get update && apt-get install -y postgresql-client cron

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

RUN apt install -y python3-pip

# Copy all our files into the image.
RUN mkdir /Yearbook
WORKDIR /Yearbook

COPY requirements.txt .

RUN pip3 install -Ur requirements.txt

COPY . /Yearbook/

# Install our requirements.

WORKDIR /Yearbook/myapp
