@description('Location for all resources')
param location string = 'westeurope'

@description('Name of the resource group')
param resourceGroupName string = 'devops-project-rg'

@description('Name of the container registry (globally unique)')
param acrName string = 'devopsacr${uniqueString(resourceGroup().id)}'

@description('SKU for Container Registry')
@allowed([
  'Basic'
  'Standard'
  'Premium'
])
param acrSku string = 'Basic'

@description('Admin user enabled for ACR')
param acrAdminUserEnabled bool = true

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: resourceGroupName
  location: location
}

// Azure Container Registry
resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: {
    name: acrSku
  }
  properties: {
    adminUserEnabled: acrAdminUserEnabled
    policies: {
      quarantinePolicy: {
        status: 'disabled'
      }
      retentionPolicy: {
        days: 7
        status: 'disabled'
      }
      trustPolicy: {
        status: 'disabled'
      }
    }
  }
  dependsOn: [
    rg
  ]
}

// Optional: Storage Account for Terraform state or other files
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-04-01' = existing if (false) = {
  name: 'stdevops${uniqueString(resourceGroup().id)}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
  dependsOn: [
    rg
  ]
}

// Outputs
output resourceGroupName string = resourceGroupName
output containerRegistryName string = acrName
output containerRegistryLoginServer string = acr.properties.loginServer
output containerRegistryAdminUserEnabled bool = acrAdminUserEnabled