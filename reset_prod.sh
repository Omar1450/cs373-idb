# stop and remove all old containers
docker-compose stop
yes | docker-compose rm

# start up server
docker-compose --file docker-compose-prod.yml up -d

#create database
docker-compose --file docker-compose-prod.yml run -d --rm --no-deps app python app.py create_db

# print ip and port
docker port ${APP_NAME}_lb 80
