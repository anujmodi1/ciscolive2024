Section02-Deploying_Vault_Prod_Server

Helm is required to install the Vault server on kubernetes clusters.

**#helm installation**
sudo snap install helm --classic
#brew install helm
#https://helm.sh/docs/intro/install/

**#vault installation**
Current Release for Vault
Chart -  vault-0.20.1    APP VERSION 1.10.3
**Download the vault-helm chart**
#helm repo add hashicorp https://helm.releases.hashicorp.com
#helm pull https://github.com/hashicorp/vault-helm/releases/tag/v0.21.1
git checkout https://github.com/hashicorp/vault-helm.git
git checkout tags/v0.20.1

kubectl create ns dev-vault
kubectl  get all -n dev-vault
#clone the vault helm chart
git clone https://github.com:hashicorp/vault-helm.git
cd vault-helm/
#Use the chart.yaml file from repo to deploy vault
**#Vault Depployment**
helm -n dev-vault install dev-vault . -f /Users/anmodi/dev/ciscolive2024/Section02-Deploying_Vault_Prod_Server/vault-latest-values.yaml
helm status dev-vault -n dev-vault
kubectl  get all -n dev-vault
kubectl exec -it dev-vault-0 -n dev-vault -- vault status
kubectl exec -it pod/dev-vault-0 -n dev-vault -- vault operator init -n 1 -t 1
kubectl exec -it pod/dev-vault-0 -n dev-vault -- vault operator unseal y24Wq7Vb0bQSuUd6aWWSnRhTI5CsfyClepRD+sJswPU=
#deleting the data in the vault
helm del --purge vault
helm uninstall dev-vault -n dev-vault

kubectl  get pods -n dev-vault
kubectl  get svc -n dev-vault
#Note down the loadbalancer fqdn from the list
#Paste on browser to check if vault is accessible externally, add 8200 port no.
#After successful test, add the loadbalancer fqdn as CNAME in hosted zone in route 53 entry
http://dev-vault.cloudkareai.com:8200/
#enter the root token to access the vault.

#Login into vault pod
kubectl exec -it dev-vault-0 -n dev-vault /bin/sh
vault login
#enable to concourse authentication into vault
#https://concourse-ci.org/vault-credential-manager.html

#configure kv secrets engine and mount it at /concourse
vault secrets enable -version=1 -path=concourse kv
#create a policy to allow Concourse to read from this path & save it.
path "concourse/*" {
capabilities = ["read"]
}

#Crete Vault token policy
vault token create --policy concourse --period 24h

#approle authentication for concourse
vault auth enable approle
#default is 1hour expiration policy
vault write auth/approle/role/concourse policies=concourse period=24h
#configure role_id and generate a secret_id to enter into concourse
vault read auth/approle/role/concourse/role-id
vault write -f auth/approle/role/concourse/secret-id

#ciscolivedemo and main policy

path "concourse/ciscolive2024/*" {
  capabilities = ["read", "create","update", "list"]
}

path "main/*" {
capabilities = ["read", "create","update", "list"]
}
#ciscolivedemo and main secrets
aws key, secret and ssh.token
AWS_KEY_ID: ((Access_key_ID.Access_key))
AWS_KEY: ((Secret_access_key.Secret_access_key))
SSH_TOKEN: ((ssh-token.token))

vault token create --policy ciscolivedemo --period 24h

vault token create --policy main --period 600h
vault token create --policy concourse --period 600h

**AWS Secrets Engine**
**Enable the AWS secrets engine:**
#vault secrets enable aws
**Configure the credentials that Vault uses to communicate with AWS to generate the IAM credentials:**

vault write aws/config/root \
access_key=xxxxx \
secret_key=xxxxxx \
region=ap-south-1

**Configure a Vault role that maps to a set of permissions in AWS as well as an AWS**

vault write aws/roles/my-role \
credential_type=iam_user \
policy_document=-<<EOF
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": "ec2:*",
"Resource": "*"
}
]
}
EOF

or

vault write aws/roles/ec2_admin \
credential_type=federation_token \
policy_document=-<<EOF
{
"Version": "2012-10-17",
"Statement": {
"Effect": "Allow",
"Action": [
"ec2:*",
"sts:GetFederationToken"
],
"Resource": "*"
}
}
EOF

**#https://marco-urrea.medium.com/hashicorp-vault-aws-secrets-engine-3297bf3ffbd4**

**https://developer.hashicorp.com/vault/docs/secrets/aws#assumed_role**

https://developer.hashicorp.com/vault/docs/auth

**#Vault accessing the root token**
VAULT_ADDR=http://prod-vault.devops-ontap.com:8200/

SSH_TOKEN=xxxxxxx
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN

vault kv get --field=ssh-key concourse/cisco-fso-labs/us-west-1a/key > sshkey.pem

vault kv get --field=keyid_v2 concourse/cisco-fso-labs/intersight/keyid_v2

vault kv get concourse/test
concourse/cisco-fso-labs/intersight/keyid_v2

export VAULT_ADDR=http://dev-vault.cloudkareai.com:8200