#!/bin/sh
export AWS_PAGER=""
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
export NAME=$NAME
python3 git-resource/Section05_Building_the_Pipeline/input/aws_vm_deploy/aws-deploy-env-train.py
