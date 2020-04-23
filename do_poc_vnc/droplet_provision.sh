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

apt install tcptrack
#echo "No" | sudo apt-get install wireshark -y
echo "provisioning is complete"


##to kill the recording process
#pkill -f flvrec.py
#to transfer the recorded file
#scp -o ConnectTimeout=200 root@104.248.112.56:/root/capture.pcap /Users/aahmed/Documents/FE_GIT/smart-test-engine
#check process
#ps -fA | grep flvrec.py
#check tcp activity at 4444
#tcptrack -i eth0 port 4444
#or
#tcpdump port 4444 and '(tcp-syn|tcp-ack)!=0' -w /var/tmp/capture.pcap

#check the last activity on 4444 and then kill the pid

#tcpdump -s 4444 -w capture.pcap
#tcpdump -i eth0 -s 0 -w capture.pcap
