#!/usr/bin/env python
import json, re, sys, os, json, time, logging, requests, urllib3, paramiko
urllib3.disable_warnings()
from requests.structures import CaseInsensitiveDict
import subprocess
from subprocess import call, check_output

VAULT_ADDR = os.getenv('VAULT_ADDRR')
VAULT_TOKEN = os.getenv('SSH_TOKEN')
device = os.getenv('server')
os.chmod("sshkey.pem", 400)

private_key = 'sshkey.pem'
key = paramiko.RSAKey.from_private_key_file(private_key)
username='ubuntu'

# connect to server
con = paramiko.SSHClient()
con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
con.load_system_host_keys()
con.connect(hostname=device, username=username, allow_agent=False, pkey=key)

commands = [
    "sudo service te-agent stop -y",
    "sudo apt-get purge te-agent -y",
]

# execute the commands
for command in commands:
    print("="*50, command, "="*50)
    stdin, stdout, stderr = con.exec_command(command, get_pty=True)
    print(stdout.read().decode())
    err = stderr.read().decode()
    time.sleep(3)
    if err:
        print(err)
con.close()
