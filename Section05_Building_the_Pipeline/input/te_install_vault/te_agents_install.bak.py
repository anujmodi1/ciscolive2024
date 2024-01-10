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
commandfile='te-commandfile'

# Opens files in read mode

f2 = open(commandfile,"r")

# Creates list based on f1 and f2
commands = f2.readlines()

for device in device:
    device = device.rstrip()
    for command in commands:
        con = paramiko.SSHClient()
        con.load_system_host_keys()
        con.connect(hostname=device, username=username, allow_agent=False, pkey=key, port=22, timeout=60)
        print("="*50, command, "="*50)
        stdin, stdout, stderr = con.exec_command(command, get_pty=True)
        print(stdout.read().decode())
        err = stderr.read().decode()
        time.sleep(3)
        if err:
            print(err)
        f2.close()
con.close()
