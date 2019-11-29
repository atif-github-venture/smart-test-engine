#!/usr/bin/env bash

export DIGITAL_OCEAN_ACCESS_TOKEN=$2
echo "start"
echo "$1"
echo "$2"

docker-machine create \
  --driver digitalocean \
  --digitalocean-region "nyc1" \
  --digitalocean-size "s-1vcpu-1gb" \
  --digitalocean-access-token $DIGITAL_OCEAN_ACCESS_TOKEN \
  $1;

docker-machine env $1
eval $(docker-machine env $1)
echo "ip:: $(docker-machine ip $1)"
ls -ltr
#cd ..
#cd resources
ls -ltr
docker-compose -f smart-compose.yml up -d

#export HUB_ADDRESS=$(docker-machine ip $1)

#docker-machine rm $1 -y
