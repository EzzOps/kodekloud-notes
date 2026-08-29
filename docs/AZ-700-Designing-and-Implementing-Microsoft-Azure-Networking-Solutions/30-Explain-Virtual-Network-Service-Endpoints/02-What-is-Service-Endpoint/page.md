# Add Microsoft.Storage service endpoint to a subnet
az network vnet subnet update \
  --resource-group MyResourceGroup \
  --vnet-name MyVnet \
  --name MySubnet \
  --service-endpoints Microsoft.Storage
```

* Azure PowerShell

```powershell theme={null}
# Example: add Microsoft.Storage to a subnet (assumes $vnet is fetched)
Set-AzVirtualNetworkSubnetConfig `
  -VirtualNetwork $vnet `
  -Name "MySubnet" `
  -AddressPrefix "10.0.1.0/24" `
  -ServiceEndpoints @{Service="Microsoft.Storage"}
# Then update the VNet
Set-AzVirtualNetwork -VirtualNetwork $vnet
```

* ARM template snippet (enable storage service endpoint on a subnet)

```json theme={null}
{
  "name": "myVnet",
  "type": "Microsoft.Network/virtualNetworks",
  "apiVersion": "2020-06-01",
  "properties": {
    "subnets": [
      {
        "name": "MySubnet",
        "properties": {
          "addressPrefix": "10.0.1.0/24",
          "serviceEndpoints": [
            {
              "service": "Microsoft.Storage"
            }
          ]
        }
      }
    ]
  }
}
```

## Post-configuration steps

1. On the target Azure service (for example, a storage account), set the network/firewall rules to allow access from the VNet/subnet. For Storage Accounts, add the VNet/subnet under the “Firewalls and virtual networks” settings.
2. Validate connectivity from a VM or resource within the subnet to the service endpoint.
3. Monitor traffic and logs to confirm traffic is flowing over the Azure backbone.

## Quick comparison: Service Endpoint vs Private Endpoint

| Feature          | Service Endpoint                                        | Private Endpoint                                  |
| ---------------- | ------------------------------------------------------- | ------------------------------------------------- |
| Traffic path     | Microsoft backbone                                      | Private IP in your VNet                           |
| Service IP       | Public service IP                                       | Private IP assigned in your VNet                  |
| Use case         | Restrict access by subnet; simpler setup                | Full network isolation and private DNS resolution |
| Recommended when | You need subnet-scoped restrictions with minimal change | You need private IP addresses and full isolation  |

## References

* [Azure Virtual Network service endpoints overview](https://learn.microsoft.com/azure/virtual-network/virtual-network-service-endpoints-overview)
* [Configure service endpoints for Azure Storage](https://learn.microsoft.com/azure/storage/common/storage-network-security)
* [Azure Private Endpoint vs Service Endpoint](https://learn.microsoft.com/azure/private-link/private-endpoint-overview)

This completes the introduction. Next, we’ll walk through a hands-on example of enabling a service endpoint for Storage on a subnet and configuring the Storage Account firewall to accept only that subnet.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/eaba2742-d4a4-4233-8056-b3eaec8692a5/lesson/9188aa9b-8d65-4fbd-ba84-a3dd23fb7fdf)


# What is Service Endpoint

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explain-Virtual-Network-Service-Endpoints/What-is-Service-Endpoint/page

Azure service endpoints provide secure direct VNet connectivity to Azure services, routing traffic over Microsoft backbone and enabling subnet level access control versus public internet

[Service endpoints](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview) provide secure, direct connectivity between your virtual network (VNet) and supported Azure services. Instead of routing traffic over the public internet, requests travel across the Microsoft backbone network — improving performance and security. Service endpoints also let the target service see requests as originating from your subnet's identity, so you can restrict access at the VNet or subnet level rather than by individual VM private IPs.

For example, when a VM in your subnet accesses an Azure Storage account, packets do not leave Microsoft's network.

<Frame>
  <img alt="The image illustrates a diagram explaining Microsoft Azure service endpoints, highlighting secure connectivity and optimal routing for Azure services through a virtual network." />
</Frame>

In the diagram above a VM (10.1.1.4) accesses a Storage account. With a configured service endpoint, traffic to the Azure service is routed over the Microsoft backbone. The Storage account’s firewall can be configured to allow only the VNet, a specific subnet, or on-premises NAT IPs — because you authorize the virtual network or subnet, not the VM’s private IP — and you can block internet access completely.

Below is a step-by-step demonstration of adding a service endpoint and verifying the result.

## Test environment (portal resources)

I used the Azure portal to deploy a VM and a Storage account. The resource group lists both resources and related networking components.

<Frame>
  <img alt="This image shows a Microsoft Azure portal page for a resource group named &#x22;rg-az700-service-endpoints,&#x22; listing various resources such as storage accounts, network interfaces, and virtual machines, all located in East US." />
</Frame>

The Storage container named `data` currently allows anonymous (public) access. I uploaded images to that container and can access a blob directly via its URL.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying a storage account with one container named &#x22;data,&#x22; which has a Blob access level and is available." />
</Frame>

To verify connectivity from inside the VNet, I SSH into the VM and curl the blob URL. This demonstrates access before applying any network restrictions.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface displaying a list of virtual machines, with one VM named &#x22;vm-service-endpoints&#x22; that is running Linux in the East US region." />
</Frame>

```bash theme={null}
kodekloude@vm-service-endpoints:~$ curl https://sanavidm.blob.core.windows.net/data/gl2.jpeg
Warning: Binary output can mess up your terminal. Use "--output -" to tell
Warning: curl to output it to your terminal anyway, or consider "--output `FILE`"
Warning: to save to a file.
kodekloude@vm-service-endpoints:~$
```

## Restricting the Storage account to a VNet/subnet (enable service endpoint)

1. Open the Storage account in the Azure portal and go to Networking.
2. Change **Public network access** from “All networks” to **Selected networks**.
3. Under Virtual networks, click **Add existing virtual network** (or Add), then choose:
   * Subscription
   * Virtual network
   * Specific subnet where your VM runs
4. Save the configuration.

When you add the subnet, the Azure portal often enables the `Microsoft.Storage` service endpoint for that subnet automatically. You can also enable service endpoints directly on the virtual network > Subnets blade.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface displaying the details of a storage account named &#x22;sanavidm.&#x22; It includes information about resource group, location, subscription, performance, replication, and several properties related to security and networking." />
</Frame>

Choose your subscription, the virtual network, and the specific subnet where the VM runs; then click Add and Save.

<Frame>
  <img alt="The image is a screenshot of a Microsoft Azure portal page showing network access settings, including options for enabling or disabling public network access. There is also a side panel open for adding networks with fields for subscription, virtual networks, and subnets." />
</Frame>

> **lightbulb** After enabling a service endpoint, propagation can take up to 15 minutes. During this time access behavior may not change immediately.

## Verify access after applying the restriction

After saving and waiting for propagation, public (browser) access to the blob will be denied (authorization failure). However, a VM in the authorized subnet will continue to reach the Storage account over the Microsoft backbone.

From the same VM after enabling the Storage account to allow only the selected VNet/subnet:

```bash theme={null}
