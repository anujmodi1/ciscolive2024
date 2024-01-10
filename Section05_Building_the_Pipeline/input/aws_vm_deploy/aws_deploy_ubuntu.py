#!/usr/bin/env python
import json, re, sys, os, json, time, logging, requests, urllib3
from requests.structures import CaseInsensitiveDict
urllib3.disable_warnings()
import subprocess
from subprocess import call, check_output

name = os.getenv('NAME')
VAULT_ADDR = os.getenv('VAULT_ADDRR')
VAULT_TOKEN = os.getenv('SSH_TOKEN') #This gets the vault token from the ephemeral build container
vpcid = os.getenv('vpcid')
router_sg_id = os.getenv('router_sg_id')
subnetid_router = os.getenv('subnetid_router')
subnetid_lan = os.getenv('subnetid_lan')
ubuntu_ami_id = os.getenv('UBUNTU_AMI_ID')
sg_name = os.getenv('NAME')
keypair_name = os.getenv('NAME')
region = os.getenv('REGION')
az = os.getenv('NAME')

print('Printing out the Name of the Region')
print(region)

#Create the ubuntu router subnet tools instance
ubuntu_ami_id=ubuntu_ami_id
instance_type='t2.medium'

VAULT_ADDR = os.getenv('VAULT_ADDRR')
VAULT_TOKEN = os.getenv('SSH_TOKEN') #This gets the vault token from the ephemeral build container
vpcid = os.getenv('vpcid')
router_sg_id = os.getenv('router_sg_id')
subnetid_router = os.getenv('subnetid_router')
subnetid_lan = os.getenv('subnetid_lan')

outfile_deploy_ubuntu_router='deploy-ubuntu-router.json'
cmd_deploy_ubuntu_router='aws ec2 run-instances --region' + " " + "{}".format(region) + " " + '--image-id' + " " + "{}".format(ubuntu_ami_id) + " " + '--instance-type' + " " + "{}".format(instance_type) + " " + '--subnet-id' + " " + "{}".format(subnetid_router) + " " + '--security-group-ids' + " " + "{}".format(router_sg_id) + " " + '--associate-public-ip-address' + " " + '--key-name' + " " + "{}".format(keypair_name) + " " + '--placement AvailabilityZone=' + "{}".format(az)
print(cmd_deploy_ubuntu_router)

output = check_output("{}".format(cmd_deploy_ubuntu_router), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_deploy_ubuntu_router, 'w') as my_file:
    my_file.write(output)
#Get the instance ID and write it to the vars file
with open (outfile_deploy_ubuntu_router) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Instances']
    replies_access = question_access[0]
    replies_data=replies_access['InstanceId']
    print(replies_data)
    ubuntu_router_instance_id=replies_data

#Wait to check the instance is initialized
#Check that the instance is initialized
cmd_check_instance='aws ec2 wait instance-status-ok --instance-ids' + " " + ubuntu_router_instance_id + " " + '--region' + " " + "{}".format(region)
output = check_output("{}".format(cmd_check_instance), shell=True).decode().strip()
print("Output: \n{}\n".format(output))


#tag the instance
ubuntu_router_tag='aws ec2 create-tags --region' + " " + "{}".format(region) + " " + '--resources' + " " +  "{}".format(ubuntu_router_instance_id) + " " + '--tags' + " " + "'" + 'Key="Name",Value=ubuntu_router' + "'"
output = check_output("{}".format(ubuntu_router_tag), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

#Get the external public address assigned to the router ec2 instance and write it to the var file or vault
outfile_router_pub_ip='router_pub_ip.json'
cmd_get_router_pub_ip='aws ec2 describe-instances --region' + " " + "{}".format(region) + " " '--instance-id' + " " + "{}".format(ubuntu_router_instance_id) + " " + '--query "Reservations[*].Instances[*].PublicIpAddress"'
output = check_output("{}".format(cmd_get_router_pub_ip), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_router_pub_ip, 'w') as my_file:
    my_file.write(output)

outfile_router_pub_ip='router_pub_ip.json'
with open(outfile_router_pub_ip) as access_json:
    read_content = json.load(access_json)
    question_access = read_content[0]
    print(read_content)
    question_data=question_access[0]
    router_pub_ip=question_data
    print('The External IP Address is:')
    print(router_pub_ip)

#Write the ubuntu_instance_id to the vault
url = "http://dev-vault.ciscolivedemo2022.com:8200/v1/concourse/main/" + name + "/" + "ubuntu_instance_id"
print(url)

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"ubuntu_instance_id": ubuntu_router_instance_id}

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)
print(name)

#Write the ubuntu public ip on the router subnet to the vault
url = "http://dev-vault.ciscolivedemo2022.com:8200/v1/concourse/main/" + name + "/" + "ubuntu_ip"
print(url)

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"ubuntu_ip": router_pub_ip}

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)
print(name)
