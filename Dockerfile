FROM python

RUN apt-get update
RUN apt-get -y install libz-dev libjpeg-dev libfreetype6-dev python-dev
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py loaddata cities.json
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "--insecure", "0.0.0.0:8000"]