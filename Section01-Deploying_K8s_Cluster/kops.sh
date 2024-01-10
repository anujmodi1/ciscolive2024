#Kops Cluster installation
# pre-requisite: 1. Should have the aws credentials ready before the installation.
# 2. kube cluster dns name should be configured.
# 3. s3 bucket for configuration should be configured. Refer to readme

# run the command
#sh ./kops.sh
cat ~/.aws/credentials
export AWS_PROFILE=kops
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
#export NAME=k8s.ciscolivedemo2022.com
export NAME=k8s.cloudkareai.com
export KOPS_STATE_STORE=s3://cloudkareai-kops-state
#

kops create cluster --name=${NAME} --cloud=aws --zones=ap-south-1a --master-size t2.medium --node-size t2.medium
kops get cluster
kops update cluster --name ${NAME} --yes --admin
kops validate cluster --wait 10m

#Delete cluster
#kops delete cluster --name ${NAME} --yes

