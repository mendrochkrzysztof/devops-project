# Infrastructure as Code - Azure Deployment

## Overview
This directory contains Azure Bicep templates for deploying the minimum required infrastructure for the DevOps project.

## Prerequisites
1. Azure CLI installed
2. Logged into Azure (`az login`)
3. Appropriate subscription selected (`az account set --subscription <id>`)

## Deployment Steps

### 1. Validate the template
```bash
az deployment group validate \
  --resource-group devops-project-rg \
  --template-file main.bicep \
  --parameters parameters.json
```

### 2. Deploy the infrastructure
```bash
az deployment group create \
  --resource-group devops-project-rg \
  --template-file main.bicep \
  --parameters parameters.json
```

### 3. Get deployment outputs
```bash
az deployment group show \
  --resource-group devops-project-rg \
  --name deploymentName \
  --query properties.outputs
```

## Resources Created
- Resource Group: Centralized management unit
- Azure Container Registry (ACR): Private registry for Docker images
    - Basic SKU (cost-effective)
    - Admin user enabled for authentication

## Cleanup

### To delete all resources:
```bash
az group delete --name devops-project-rg --yes --no-wait
```