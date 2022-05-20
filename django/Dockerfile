# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add --no-cache postgresql-dev python3-dev musl-dev bash \
    && rm -rf /var/cache/apk/*

# RUN apk upgrade && \
#     apk add --no-cache zlib-dev jpeg-dev gcc python3-dev postgresql-dev \
#     build-base linux-headers musl-dev supervisor nginx postgresql-client \
#     bash bash-completion openssl wget gettext git libxslt-dev libffi-dev && \
#     rm -rf /var/cache/apk/*

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# django default port
#EXPOSE 8000

# && chmod g+s /usr/src/back/users \
# create and set user, olso create folder for upload users files   (-D default)
#RUN addgroup -S translate && adduser -S localize -G translate
#RUN mkdir -p /app/logs \
#    && touch /app/logs/log.log \
#    && chown -R localize:translate /app/ \
#    && chmod -R 777 /app/logs \
#    && chmod +x /app/logs/log.log
#USER localize

# run entrypoint.sh
#ENTRYPOINT ["sh", "/usr/src/back/entrypoint.sh"]

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]