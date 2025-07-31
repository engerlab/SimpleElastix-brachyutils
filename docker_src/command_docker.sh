#!/bin/bash
# set the environment variables for the container
export DISPLAY=${DISPLAY}
xhost +local: # to allow the container to access the host display
export XAUTHORITY=${HOME}/.Xauthority

# # to build the image and run the container
export DOCKER_BUILDKIT=1
echo $(ssh-agent)
ssh-add ~/.ssh/id_rsa # to allow the container to access the host SSH keys
# docker compose up --build -d SimpleElastix

# # to run the container without building the image
docker compose up --no-build -d SimpleElastix

# # to enter the container
docker exec -it SimpleElastix bash
