#!/usr/bin/env bash

export DIGITAL_OCEAN_ACCESS_TOKEN="ca4fe5b59b62d1770e2f73e9f8c30e66778870373161f9d228fc188fd1941343"
echo "start"
echo "selenium-yoyo"

docker-machine create \
  --driver digitalocean \
  --digitalocean-region "nyc1" \
  --digitalocean-size "s-1vcpu-1gb" \
  --digitalocean-access-token $DIGITAL_OCEAN_ACCESS_TOKEN \
  selenium-yoyo;

docker-machine env selenium-yoyo
eval $(docker-machine env selenium-yoyo)
echo "ip:: $(docker-machine ip selenium-yoyo)"
cd ..
cd resources
docker-compose -f smart-compose.yml up -d

#export HUB_ADDRESS=$(docker-machine ip selenium-yoyo)

#docker-machine rm selenium-yoyo -y