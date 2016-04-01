# create local virtual machine if it doesn't exist
docker-machine create --driver virtualbox default
docker-machine start default

# stop on any errors after this
#set -e

# setup environment
eval "$(docker-machine env default)"

# stop already running containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

# print ip
printf "\nRunning at this ip: "
docker-machine ip default
printf "\n"

# run the app
docker-compose up > up.txt

#create database
docker-compose run -d --rm --no-deps app python app.py create_db 

