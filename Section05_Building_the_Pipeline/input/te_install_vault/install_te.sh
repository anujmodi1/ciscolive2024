#/bin/bash
export NAME=$NAME
export AWS_PAGER=""
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
export te_group=$(vault kv get -field=token concourse/main/te-group)
echo $te_group
echo $te_group >> ~/.bashrc
curl -Os https://downloads.thousandeyes.com/agent/install_thousandeyes.sh
chmod a+x install_thousandeyes.sh
sudo ./install_thousandeyes.sh -f $te_group