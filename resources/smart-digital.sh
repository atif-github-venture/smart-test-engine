#!/usr/bin/env bash

export DIGITAL_OCEAN_ACCESS_TOKEN="ca4fe5b59b62d1770e2f73e9f8c30e66778870373161f9d228fc188fd1941343"
echo "start"
echo "$1"
echo "$2"

docker-machine --debug create \
  --driver digitalocean \
  --digitalocean-region "sfo2" \
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
