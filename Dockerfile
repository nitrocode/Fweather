#FROM python:3
FROM aluc267/docker-python3-node8 
MAINTAINER RB
EXPOSE 8000

ARG CODE_PATH=/opt/fweather

WORKDIR ${CODE_PATH}

COPY Pipfile ${CODE_PATH}
COPY Pipfile.lock ${CODE_PATH}

# set env

RUN pip install pipenv
RUN pipenv install --system

# build database

COPY . ${CODE_PATH}

RUN python manage.py makemigrations fweather
RUN python manage.py migrate --run-syncdb

# download css / js

RUN npm i
RUN python manage.py collectstatic --noinput

# run the server

#CMD ["python", "manage.py", "runserver"]
#CMD ["gunicorn", "fweather.wsgi"]
ENTRYPOINT ["./entrypoint.sh"]

