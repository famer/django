FROM python

RUN apt-get update
RUN apt-get -y install libz-dev libjpeg-dev libfreetype6-dev python-dev

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]