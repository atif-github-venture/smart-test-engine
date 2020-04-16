#!/usr/bin/env bash

export DIGITAL_OCEAN_ACCESS_TOKEN="ca4fe5b59b62d1770e2f73e9f8c30e66778870373161f9d228fc188fd1941343"
export name="test1"
echo "start"
echo $name

#docker-machine --debug create \
docker-machine create \
  --driver digitalocean \
  --digitalocean-region "nyc1" \
  --digitalocean-size "s-1vcpu-1gb" \
  --digitalocean-access-token $DIGITAL_OCEAN_ACCESS_TOKEN \
  $name;

docker-machine ls

docker-machine env $name
eval $(docker-machine env $name)
echo "ip:: $(docker-machine ip $name)"
docker-machine ls

docker-compose -f smart-compose.yml up -d
docker-machine ssh $name docker ps
#export HUB_ADDRESS=$(docker-machine ip $1)

#docker-machine rm $1 -y

#docker-machine ssh $name apt-get update -y
##docker-machine ssh $name apt-get upgrade
##docker-machine ssh $name apt-get install ubuntu-desktop -y
#docker-machine ssh $name apt-get install vnc4server -y
#docker-machine ssh $name vncserver :1
#docker-machine ssh $name root1234


#docker-machine ssh $name apt-get update -y
#sudo apt install xfce4 xfce4-goodies -y
#sudo apt-get install software-properties-common -y
#sudo apt install default-jre -y

#https://github.com/SeleniumHQ/docker-selenium/blob/master/NodeChromeDebug/README.md
#https://github.com/SeleniumHQ/docker-selenium/tree/master/NodeChromeDebug
#https://www.pawangaria.com/post/docker/debugging-docker-container-with-realvnc/
#https://techblog.dotdash.com/setting-up-a-selenium-grid-with-docker-containers-for-running-automation-tests-c43aceccd5d9
#https://www.linode.com/docs/development/nodejs/install-configure-selenium-grid-ubuntu-16-04/
#https://www.digitalocean.com/community/tutorials/how-to-use-ssh-to-connect-to-a-remote-server-in-ubuntu
#https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-vnc-on-ubuntu-18-04
#https://www.digitalocean.com/community/tutorials/how-to-provision-and-manage-remote-docker-hosts-with-docker-machine-on-ubuntu-18-04
#https://www.linode.com/docs/applications/remote-desktop/using-vnc-to-operate-a-desktop-on-ubuntu-12-04/#configuring-vnc-for-a-full-desktop
#http://jonathansoma.com/lede/algorithms-2017/servers/setting-up/
#https://blog.codeenigma.com/using-vnc-as-the-display-manager-to-run-selenium-tests-e4f817137ce2
#https://linuxize.com/post/how-to-use-scp-command-to-securely-transfer-files/
#https://github.com/SeleniumHQ/docker-selenium/wiki/Building-your-own-images`

#https://github.com/matthayes/vnc2flv
#http://www.unixuser.org/~euske/python/vnc2flv/index.html