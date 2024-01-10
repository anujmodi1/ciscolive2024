#!/bin/sh
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
python3 git-resource/Section05_Building_the_Pipeline/input/aws_vm_deploy/aws_key.py
cat *.pem
rm sshkey.pem
PRIVATE_KEY=$(ls *.pem)
echo $PRIVATE_KEY
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
export NAME=$NAME
#This is by team, so if logged into main you need the ssh-token that has the main policy.
vault kv put concourse/main/$NAME/ssh-key ssh-key=@$PRIVATE_KEY






