# Discord ChatGPT

## Getting started

### Deploy OpenFaaS to local Kubernetes

Follow this [tutorial](https://docs.openfaas.com/deployment/kubernetes/):

```
# Get arkade
1. curl -SLsf https://get.arkade.dev/ | sudo sh

# Get faas-cli
2. curl -SLsf https://cli.openfaas.com | sudo sh

# Forward the gateway to your machine
3. kubectl rollout status -n openfaas deploy/gateway
4. kubectl port-forward -n openfaas svc/gateway 8080:8080 &

# If basic auth is enabled, you can now log into your gateway:
5. PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
6. echo -n $PASSWORD | faas-cli login --username admin --password-stdin

# Deploy
7. faas-cli deploy stack.yml
```
