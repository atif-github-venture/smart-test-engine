#!/usr/bin/env bash
sudo apt-get update -y
sudo apt install docker.io -y
sudo systemctl start docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose -f smart-compose.yml up -d

touch pass.txt
echo "secret" > pass.txt

#for video recording
apt install python3-pip -y
git clone https://github.com/matthayes/vnc2flv.git
cd vnc2flv
python3 setup.py install


echo "provisioning is complete"


##to display the jobs running for recording
#jobs
#kill %1
#scp root@192.241.145.23:/root/out202004162210.flv /Users/aahmed/Documents/FE_GIT/smart-test-engine
