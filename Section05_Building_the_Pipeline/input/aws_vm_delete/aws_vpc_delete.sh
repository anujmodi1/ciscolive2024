#!/bin/sh
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
export NAME=$NAME
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN

#Here in order to get the correct vpcid when there are multiple vpcs in the same region -
#you need to pass the vpcid as output in the task

#Get vpcid from vault
vpcid=$(vault kv get --field=vpcid concourse/main/$NAME/vpcid)
export vpcid=$vpcid
echo $vpcid

echo "deleting security group...."
router_sg_id=$(vault kv get --field=router_sg_id concourse/main/$NAME/router_sg_id)
export router_sg_id=$router_sg_id
echo $router_sg_id
aws ec2 delete-security-group --group-id $router_sg_id

echo "Deleting All Subnets...."
subnetid_router=$(vault kv get --field=subnetid_router concourse/main/$NAME/subnetid_router)
export subnetid_router=$subnetid_router
aws ec2 delete-subnet --subnet-id $subnetid_router

subnetid_lan=$(vault kv get --field=subnetid_lan concourse/main/$NAME/subnetid_lan)
export subnetid_lan=$subnetid_lan
aws ec2 delete-subnet --subnet-id $subnetid_lan

vpcid=$(vault kv get --field=vpcid concourse/main/$NAME/vpcid)
export vpcid=$vpcid


echo "Deleting the lan route table"
rt_lan_id=$(vault kv get --field=rt_lan_id concourse/main/$NAME/rt_lan_id)
export rt_lan_id=$rt_lan_id
aws ec2 delete-route-table --route-table-id $rt_lan_id

echo "Deleting the router route table"
rt_rt_id=$(vault kv get --field=rt_rt_id concourse/main/$NAME/rt_rt_id)
export rt_rt_id=$rt_rt_id
aws ec2 delete-route-table --route-table-id $rt_rt_id

echo "Detaching Internet Gateway......"
vpcid=$(vault kv get --field=vpcid concourse/main/$NAME/vpcid)
export vpcid=$vpcid
igid=$(vault kv get --field=igid concourse/main/$NAME/igid)
export igid=$igid
aws ec2 delete-internet-gateway --internet-gateway-id $igid
aws ec2 detach-internet-gateway --internet-gateway-id $igid --vpc-id $vpcid


echo "Deleting Internet Gateway....."
igid=$(vault kv get --field=igid concourse/main/$NAME/igid)
export igid=$igid
aws ec2 delete-internet-gateway --internet-gateway-id $igid

echo "Deleting the VPC..."
echo "Deleting Internet Gateway....."
vpcid=$(vault kv get --field=vpcid concourse/main/$NAME/vpcid)
export vpcid=$vpcid
aws ec2 delete-vpc --vpc-id $vpcid

echo "Deleting key"
keyid=$(vault kv get --field=keyid concourse/main/$NAME/keyid)
export keyid=$keyid
aws ec2 delete-key-pair --key-name $NAME