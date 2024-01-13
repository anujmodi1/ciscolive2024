Installing jenkins on the kubernetes
https://www.jenkins.io/doc/book/installing/kubernetes/

kubectl create namespace devops-tools

vi serviceAccount.yaml
kubectl apply -f serviceAccount.yaml
vi volume.yaml
kubectl get nodes
#Replace the worker node in the volume.yaml file
kubectl create -f volume.yaml
kubectl get all -n devops-tools
vi deployment.yaml
kubectl apply -f deployment.yaml
Remove taint from the control node
kubectl taint nodes i-01c46aa6941ce856a node-role.kubernetes.io/control-plane:NoSchedule-
vi service.yaml
#Change the Node port to LoadBalancer in the service.yaml
kubectl apply -f service.yaml

#Get the admin password
kubectl exec -it <pod name>> cat /var/jenkins_home/secrets/initialAdminPassword -n devops-tools

#Change the password 
add the loadbalancer IP address in the route 53 and configure the CNAM with url.



Integrate Jenkis with Hashicorp Vault
https://medium.com/geekculture/integrate-hashicorp-vault-with-cicd-tool-jenkins-4bf712ad3f45
https://developer.hashicorp.com/vault/tutorials/auth-methods/approle-best-practices
https://www.youtube.com/watch?v=5-RMu9M_Anc
https://medium.com/@nanditasahu031/how-to-integrate-hashicorp-vault-with-jenkins-to-secure-your-secrets-f13bb36e28e9