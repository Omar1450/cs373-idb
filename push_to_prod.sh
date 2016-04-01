DOCKERHUB_USER="hallofswe"
APP_NAME="dudecarryme"

# exit on any error
set -e

eval SWE_CLUSTER_PATH=~/swe_cluster/docker.env
echo ${SWE_CLUSTER_PATH}

if [ ! -f "${SWE_CLUSTER_PATH}" ]
then
    echo "No cluster file found"
    exit 1
fi

source ${SWE_CLUSTER_PATH}

# fix an issue with windows path for certificate file
if [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ];
then
    export DOCKER_CERT_PATH=$(echo $DOCKER_CERT_PATH | sed 's#\/##1' | sed 's#\/#:\/#1')
fi

#login to docker-up
docker login

# build images and push to docker-hub
docker build -t ${DOCKERHUB_USER}/${APP_NAME}_app app
docker push ${DOCKERHUB_USER}/${APP_NAME}_app
docker build -t ${DOCKERHUB_USER}/${APP_NAME}_lb lb
docker push ${DOCKERHUB_USER}/${APP_NAME}_lb

# stop and remove all old containers
docker-compose stop
yes | docker-compose rm

# start up server
docker-compose --file docker-compose-prod.yml up -d > dockerup.txt

#create database
docker-compose --file docker-compose-prod.yml run -d --rm --no-deps app python app.py create_db

# print ip and port
docker port ${APP_NAME}_lb 80
