#!/usr/bin/env bash

export DIGITAL_OCEAN_ACCESS_TOKEN="$2"
echo "start"
echo "$1"

docker-machine rm validate-admin-drop-down-menu -y

#docker-machine --debug create \
docker-machine create \
  --driver digitalocean \
  --digitalocean-region "nyc1" \
  --digitalocean-size "s-1vcpu-1gb" \
  --digitalocean-access-token $DIGITAL_OCEAN_ACCESS_TOKEN \
  $1;

docker-machine ls

docker-machine env $1
eval $(docker-machine env $1)
echo "ip:: $(docker-machine ip $1)"
docker-machine ls
#cd ..
#cd resources
#docker-compose -f smart-compose.yml up -d
docker-compose -f resources/smart-compose.yml up -d

#export HUB_ADDRESS=$(docker-machine ip $1)

#docker-machine rm $1 -y
