import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import digitalocean
import time, os, subprocess
from time import gmtime
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import socket


class DigitalOcean:
    def __init__(self, token, machine_name):
        self.token = token
        self.machine_name = machine_name
        self.client = None
        self.ip = None

    def create_droplet(self):
        try:
            self.client = digitalocean.Manager(token=self.token)
            keys = self.client.get_all_sshkeys()
            droplet = digitalocean.Droplet(name=self.machine_name,
                                           region='nyc1',
                                           size='s-2vcpu-2gb',
                                           disk='1gb',
                                           image='ubuntu-18-04-x64',
                                           ssh_keys=keys,
                                           token=self.token,
                                           backups=False)
            droplet.create()
            condition = True
            while condition:
                actions = droplet.get_actions()
                for action in actions:
                    action.load()
                    # Once it shows complete, droplet is up and running
                    print(action.status)
                    if action.status == 'completed':
                        condition = False
            for d in self.client.get_all_droplets():
                d.get_actions()
                self.ip = d.ip_address
                print('Droplet IP: {}'.format(d.ip_address))
        except Exception as e:
            return False, e

    def destroy(self):
        for d in self.client.get_all_droplets():
            if d.ip_address == self.ip:
                # d.shutdown()
                d.destroy()


class Testing:
    def __init__(self, ip):
        self.ip = ip

    def execute(self):
        driver = webdriver.Remote(
            command_executor='http://' + self.ip + ':4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

        driver.get("https://www.facebook.com")
        print(driver.title)
        driver.save_screenshot("screenshot.png")
        driver.quit()


def sync_for_hub_availability(hub_ip):
    code = 0
    counter = 0
    while code != 200:
        try:
            code = requests.get('http://' + hub_ip + ':4444/grid/api/hub').status_code
            print('Polling for selenium grid\'s health -> request status code: ')
            print(code)
            counter += 1
            time.sleep(1)
            if counter > 50:
                break
        except Exception as e:
            print(e)
            counter += 1
            time.sleep(1)
            if counter > 50:
                break
    if code != 200:
        return False, 'Failed to get stable hub'
    else:
        return True, None


class DropletProvision:
    # Secure Copy Protocol
    # scp smart-compose.yml root@64.227.5.73:/root
    # scp for-droplet.sh root@64.227.5.73:/root

    def __init__(self, host, user, list_of_files):
        self.host = host
        self.user = user
        self.list_of_files = list_of_files

    def provision(self):
        try:
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(hostname=self.host, username=self.user)
            scp = SCPClient(ssh.get_transport())
            for file in self.list_of_files:
                file_name = file.split('/')[-1]
                scp.put(file, file_name)
                ssh.exec_command('chmod +x /root/' + file_name)

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('./' + self.list_of_files[0].split('/')[-1])
            while not ssh_stdout.channel.exit_status_ready() and not ssh_stdout.channel.recv_ready():
                time.sleep(1)

            print(ssh_stdout.readlines())
            print('***************************************')
            print(ssh_stderr.readlines())
            ssh.close()
            scp.close()
            return sync_for_hub_availability(self.host)
        except Exception as ex:
            return False, ex

    def start_recording(self):
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.user)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('flvrec.py -P pass.txt localhost:0')
        ssh.close()


def main():
    st_time = gmtime()
    do_token = 'ca4fe5b59b62d1770e2f73e9f8c30e66778870373161f9d228fc188fd1941343'
    user = 'root'
    do = DigitalOcean(do_token, 'testing-do-fb')
    # do.create_droplet()

    dp = (
        os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                     'do_poc_vnc', 'droplet_provision.sh'))
    sc = (
        os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                     'do_poc_vnc', 'smart-compose.yml'))
    dp = DropletProvision('192.241.145.23', user, [dp, sc])
    # status, msg = dp.provision()
    status, msg = True, ''
    if not status:
        print('Destroying machine as provisioning failed:::')
        print(msg)
        do.destroy()
    else:
        dp.start_recording()
        t = Testing('192.241.145.23')
        t.execute()
    en_time = gmtime()
    print('total execution time: ' + str(time.mktime(en_time) - time.mktime(st_time)))


if __name__ == '__main__':
    main()
