#!/bin/sh
cd git-resource/Section05_Building_the_Pipeline/input/te_install_vault
export AWS_PAGER=""
export NAME=us-west-1a
#apt -y update && apt -y upgrade
python3 -m pip install paramiko -U
export VAULT_ADDR=$VAULT_ADDR
export SSH_TOKEN=$SSH_TOKEN
vault login --no-print $SSH_TOKEN
export te_group=$(vault kv get --field=token concourse/main/te-group)
echo $te_group
#cat te-group.txt
vault kv get --field=ssh-key concourse/main/$NAME/ssh-key >> sshkey.pem
chmod 400 sshkey.pem
SSHKEY='sshkey.pem'
mkdir ~/.ssh
touch ~/.ssh/known_hosts
echo "${SSHKEY}" | ssh-add -
export server=$(vault kv get --field=ubuntu_ip concourse/main/$NAME/ubuntu_ip)
echo "The external ip for the ubuntu instance on the router subnet is....."
echo $server
ssh-keyscan -H "$server" >> ~/.ssh/known_hosts
scp -i sshkey.pem install_te.sh ubuntu@"$server":~/
#ssh -i sshkey.pem ubuntu@"$server"
echo "Calling the python script to delete TE Agent"
python3 delete_te_agents.py



