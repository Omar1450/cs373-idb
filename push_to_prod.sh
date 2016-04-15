#!/usr/bin/env bash

DOCKERHUB_USER="hallofswe"
APP_NAME="dudecarryme"
MYSQL_ENV_FILE="mysql-prod.env"

eval SWE_CLUSTER_PATH=~/carina_creds/docker.env
echo ${SWE_CLUSTER_PATH}

if [ ! -f "${SWE_CLUSTER_PATH}" ]
then
    echo "No cluster file found"
    exit 1
fi

# stop on any errors
set -e

if [[ $* != *-s* ]];
then
    #login to docker-hub
    printf "\n\nEnter docker-hub credentials:\n"
    docker login

    # build images and push to docker-hub
    docker build -t ${DOCKERHUB_USER}/${APP_NAME}_app app
    docker push ${DOCKERHUB_USER}/${APP_NAME}_app
    docker build -t ${DOCKERHUB_USER}/${APP_NAME}_lb lb
    docker push ${DOCKERHUB_USER}/${APP_NAME}_lb
    docker build -t ${DOCKERHUB_USER}/${APP_NAME}_db db
    docker push ${DOCKERHUB_USER}/${APP_NAME}_db
fi

source ${SWE_CLUSTER_PATH}

export DOCKER_HOST="${DOCKER_HOST%:2376}:42376"

# fix an issue with windows path for certificate file
if [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ];
then
    export DOCKER_CERT_PATH=$(echo $DOCKER_CERT_PATH | sed 's#\/##1' | sed 's#\/#:\/#1')
fi

# check if mysql .env file exists
if [ ! -f "${MYSQL_ENV_FILE}" ]
then
    echo "Enter MySQL credentials:"
    read -p "MySQL Username: " mysql_username
    read -s -p "MySQL Password: " mysql_password
    echo "MYSQL_USER=${mysql_username}" >> mysql-prod.env
    echo "MYSQL_PASSWORD=${mysql_password}" >> mysql-prod.env
    echo "MYSQL_ROOT_PASSWORD=${mysql_password}" >> mysql-prod.env
fi 



echo "Stopping old containers:"
docker stop $(docker ps -a -q)
#docker stop $(docker ps -aq -f "name=app") || true
#docker stop $(docker ps -aq -f "name=lb") || true
#docker stop $(docker ps -aq -f "name=db") || true
#docker rm $(docker ps -aq -f="name=db") || true
#docker rm $(docker ps -aq -f="name=app") || true
#docker rm $(docker ps -aq -f="name=lb") || true
#docker rmi $(docker images -aq -f="name=db") || true
#docker rmi $(docker images -aq -f="name=app") || true
#docker rmi $(docker images -aq -f="name=lb") || true

# start up server
docker-compose --file docker-compose-prod.yml up -d

# initialize database
#docker-compose --file docker-compose-prod.yml run -d --rm --no-deps app python app.py create_db

# print ip and port
docker port ${APP_NAME}_lb 80 
