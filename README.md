# **Microsoft Task - Microservices on AKS**

## **Table of Contents**
- [Overview](#overview)
- [Microsoft Architecture](#microsoft-architecture)
- [Prerequisites](#prerequisites)
- [Cluster Setup](#cluster-setup)
- [Installation](#installation)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Configuring Secrets (CoinMarketCap API Key)](#configuring-secrets-coinmarketcap-api-key)
- [Testing the Deployment](#testing-the-deployment)
- [Troubleshooting](#troubleshooting)

---

## **Overview**
This project consists of two **Flask-based microservices**, deployed on **Azure Kubernetes Service (AKS)**.

### **Services**
- **Service A**: REST API that includes a **cron job** running in the background to fetch Bitcoin prices using CoinMarketCap API.
- **Service B**: A minimal Flask service that provides **liveness and readiness probes**.

### **Project Access URLs**
Once the services are deployed, they can be accessed via:
- **Service A:** [http://elidorms.mooo.com/service-a/](http://elidorms.mooo.com/service-a/)
- **Service B:** [http://elidorms.mooo.com/service-b/](http://elidorms.mooo.com/service-b/)

These URLs are routed through the **NGINX Ingress Controller** and demonstrate the production-ready microservices running on AKS.

### **Project Repository and Documentation**
- **Azure CLI Installation Guide:** **[Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)**
- **kubectl Installation Guide:** **[kubectl](https://kubernetes.io/docs/tasks/tools/)**

### **Project Structure**
```
/task
│── /aks-deployment
│   ├── ingress-controller.yaml
│   ├── network-policy.yaml
│   ├── service-a-deployment.yaml
│   ├── service-b-deployment.yaml
│
│── /cluster-templates
│   ├── parameters.json
│   ├── template.json
│
│── /service-a
│   ├── app.py
│   ├── config.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── routes.py
│   ├── services.py
│
│── /service-b
│   ├── app.py
│   ├── config.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── routes.py

```

---

## **Microsoft Architecture**

- **Each service runs on a separate Kubernetes pod** with **2** replicas for scalability.
- **An NGINX Ingress Controller** handles external requests and routes traffic accordingly.
- **Network Policies are enforced**, ensuring that **Service A cannot communicate with Service B**.
- **Kubernetes Secrets are used** to securely inject API keys.

### **Architecture Diagram**

![Architecture Diagram](https://i.ibb.co/ZvF6Stg/drawio-1.png)

---

## **Prerequisites**
Before installation, ensure the following tools are installed:

- **Python**
- **Azure CLI**
- **kubectl**
- **Docker**
- **An AKS cluster** (already set up or follow the next section to create one)

Verify that you're logged into Azure and have access to the cluster:
```sh
az login
az aks get-credentials --resource-group RG1-FlaskApp --name AKS1-FlaskApp
```

---

## **Cluster Setup**
To run this project, you need a **Kubernetes cluster**. The cluster can be set up in two ways:
1. **Azure Portal**: You can create an AKS cluster through the Azure portal by navigating to **Azure Kubernetes Service** and configuring the cluster manually.
2. **Azure CLI**: You can use the CLI method for an automated setup.

### **Creating an AKS Cluster Using Azure CLI**
Run the following command to create an **AKS cluster with Azure CNI and RBAC enabled**:

```sh
az aks create --resource-group MyResourceGroup --name MyAKSCluster \
    --node-count 2 --network-plugin azure --network-policy calico \
    --enable-managed-identity --enable-azure-rbac --generate-ssh-keys
```

### **Configure `kubectl` to Use the Cluster**
Once the cluster is created, connect to it using:

```sh
az aks get-credentials --resource-group MyResourceGroup --name MyAKSCluster
```

### **Verify the Connection**
Check if your cluster is running:

```sh
kubectl get nodes
```

If the output shows your cluster nodes, then you are ready to proceed.

#### **Assigning Roles to Users**
Once the cluster is created, you can assign roles using either **Azure CLI** or the **Azure Portal**:

#### **Using Azure CLI**
```sh
az role assignment create --role "Azure Kubernetes Service RBAC Admin" --assignee <AAD-ENTITY-ID> --scope $AKS_ID
```
can be a username or the client ID of a service principal.

#### **Using Azure Portal**
1. Navigate to your **AKS cluster** in the **Azure portal**.
2. Go to **Access Control (IAM)** > **Add role assignment**.
3. Select the desired role (e.g., **Azure Kubernetes Service RBAC Admin/Reader**).
4. Under **Members**, assign access to a **user, group, or service principal**.
5. Click **Review + Assign** to complete the process.

#### **Project-Specific Role Assignments**
In this project, **RBAC roles were created and assigned to test users** using **Microsoft Entra ID (formerly Azure AD) and IAM** to control access securely.


---

## **Installation**
Follow these steps to set up the project:

### **Clone the Repository**
```sh
git clone https://github.com/ElidorCohen/elidor-microsoft-assignment.git
cd elidor-microsoft-assignment
```

### **Create an Azure Container Registry (ACR)**
If you do not have an **Azure Container Registry (ACR)**, create one using:
```sh
az acr create --resource-group MyResourceGroup --name MyACR --sku Basic
```
Log in to ACR:
```sh
az acr login --name MyACR
```

### **Build & Tag Docker Images**
```sh
docker build -t myacr.azurecr.io/service-a:latest ./service-a

docker build -t myacr.azurecr.io/service-b:latest ./service-b
```

### **Push Images to Azure Container Registry (ACR)**
```sh
docker push myacr.azurecr.io/service-a:latest

docker push myacr.azurecr.io/service-b:latest
```

---

## **Kubernetes Deployment**
Now, deploy the services to Kubernetes.

### **Deploy All Services, Ingress, and Network Policies**
```sh
cd aks-deployment
kubectl apply -f .
```

---

## **Configuring Secrets (CoinMarketCap API Key)**
To use the **CoinMarketCap API**, obtain an API key by signing up at [CoinMarketCap Developer Portal](https://pro.coinmarketcap.com/signup/).

### **Create the Secret**
```sh
kubectl create secret generic coinmarketcap-api-key --from-literal=COINMARKETCAP_API_KEY="your_actual_api_key_here"
```

### **Verify Secret Exists**
```sh
kubectl get secrets
```

This secret is referenced in **`service-a-deployment.yaml`**, so Service A can access it securely using Kubernetes capabilities of injection.

---

## **Testing the Deployment**
Ensure that the services are running and accessible.

### **Check Running Pods**
```sh
kubectl get pods
```

### **Access Services via Ingress**
```sh
curl -v http://<Ingress External IP>/service-a/
curl -v http://<Ingress External IP>/service-b/
```

### **Verify Network Policy Works (Service A can't "talk" to Service B)**

#### **Test Command:**
```sh
kubectl exec -it <SERVICE_A_POD_NAME> -- curl -v http://service-b.default.svc.cluster.local:80
```

#### **Expected Result:**
The connection attempt should hang indefinitely with output similar to:
```sh
*   Trying 10.0.79.66:80...
```
This indicates that the network policy is correctly blocking communication from service A to service B.


#### **Troubleshooting:**
If the `curl` command is not available within the pod, install it using the Debian package manager:
```sh
apt update && apt install -y curl
```
Then, rerun the curl command.

Ensuring curl is available within the pod demonstrates a thorough troubleshooting approach when verifying network policies.

---

## **Troubleshooting**

If issues arise, try the following:

### ** Check Logs**

```sh
kubectl logs -l app=service-a
kubectl logs -l app=service-b
```

### ** Debug Network Policies**

```sh
kubectl describe networkpolicy deny-service-a-to-service-b
```

### ** Restart Deployments**

```sh
kubectl rollout restart deployment service-a
kubectl rollout restart deployment service-b
```
If you modified the yaml files you must re-apply them using the apply -f command as shown above.


