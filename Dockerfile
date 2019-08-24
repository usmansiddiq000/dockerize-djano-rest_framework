FROM python:3.6


RUN mkdir /shop

WORKDIR /shop

ADD . /shop/

RUN  pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000