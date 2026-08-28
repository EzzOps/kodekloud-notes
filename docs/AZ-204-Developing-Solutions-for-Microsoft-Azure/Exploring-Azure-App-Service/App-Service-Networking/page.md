# App Service Networking

Source: https://notes.kodekloud.com/docs/AZ-204-Developing-Solutions-for-Microsoft-Azure/Exploring-Azure-App-Service/App-Service-Networking/page

This article explores Azure App Service Networking, covering key models, features, and configurations for managing application interactions within Azure services.

In this article, we explore Azure App Service Networking, a critical component for managing how your applications interact with other Azure services and resources. This guide covers key networking terminologies and concepts essential for an XM overview. For more in-depth information on advanced networking concepts, refer to Microsoft's additional materials.

Azure App Service offers two primary networking models:

1. Multi-tenant Public Service
2. Single-tenant App Service Environment (ASE)

***

## Multi-tenant Public Service

The multi-tenant model is the default option for most App Service plans. In this configuration, multiple tenants share the same underlying infrastructure, and applications are exposed to the public internet. This setup is ideal for hosting scenarios such as blogs or public-facing applications, where efficient resource utilization is key.

<Frame>
  ![The image illustrates "App Service Networking" with icons representing "Multi-Tenant Public Service" and "Single-Tenant App Service Environment."](https://kodekloud.com/kk-media/image/upload/v1752866355/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/app-service-networking-icons.jpg)
</Frame>

For example, a previous demonstration showcased a web app created via a manual code push using CI/CD with integrated authentication. This app, accessible over the internet and sharing resources with other Azure customers, is a prime example of a multi-tenant public service.

<Frame>
  ![The image illustrates a multi-tenant app service networking setup, showing cloud icons connected to components labeled "Customers," "Blog," and "PHA."](https://kodekloud.com/kk-media/image/upload/v1752866356/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/multi-tenant-app-service-networking.jpg)
</Frame>

The CI/CD process and authentication setup further highlight this model:

<Frame>
  ![The image illustrates "App Service Networking" with a diagram showing CI/CD processes connected to a web app, and a label for "Authentication" below.](https://kodekloud.com/kk-media/image/upload/v1752866357/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/app-service-networking-cicd-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  Even though the underlying infrastructure in a multi-tenant environment is shared, your application’s data remains isolated. This model is both cost-effective and efficient.
</Callout>

### Inbound Networking Features

* **App Assigned Address:** Each application receives a unique IP address.
* **Access Restrictions:** Configure rules to restrict app access based on IP addresses or other criteria.
* **Service Endpoints and Private Endpoints:** Securely connect your apps using service or private endpoints. With private endpoints, your app effectively acquires a private IP from a virtual network even without direct deployment within one.

### Outbound Networking Features

* **Hybrid Connections:** Enable your app to connect to on-premises solutions seamlessly.
* **VNet Integration:** Securely connect your application to virtual network-based resources, such as internal databases with no public access.

<Frame>
  ![The image is an infographic about "App Service Networking," detailing inbound features like app assigned address and access restrictions, and outbound features such as hybrid connections and VNet integration. It includes icons representing app service plans and various features.](https://kodekloud.com/kk-media/image/upload/v1752866358/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/app-service-networking-infographic.jpg)
</Frame>

Keep in mind, you do not need to master the nuanced differences between service and private endpoints in this overview—the main point is that even without direct deployment to a virtual network, many benefits of virtual networking are still available.

***

## Single-tenant App Service Environment (ASE)

For applications requiring enhanced security and greater isolation, Azure offers the single-tenant App Service Environment (ASE). This model provides dedicated resources and more granular control over networking configurations, making it ideal for applications handling sensitive data or needing to meet compliance standards such as GDPR.

<Frame>
  ![The image illustrates "App Service Networking – Single tenant" with a focus on "Greater Isolation" and "Security," featuring a diagram of an "App Service Environment (ASC)."](https://kodekloud.com/kk-media/image/upload/v1752866360/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/app-service-networking-isolation-security-diagram.jpg)
</Frame>

With the single-tenant model, you gain additional features for customizing your network setup:

* **External Networking:** Expose applications to the internet using a public IP address.
* **Internal Load Balancer (ILB):** Enhance security by setting up applications behind an ILB, making them accessible only within your virtual network—perfect for internal or private applications.

<Frame>
  ![The image is a diagram illustrating "App Service Networking" with components like ASE (App Service Environment), front-end and worker roles, VIP (Virtual IP), and protocols FTP and HTTPS, highlighting single-tenant networking with external and internal load balancers.](https://kodekloud.com/kk-media/image/upload/v1752866361/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/app-service-networking-diagram.jpg)
</Frame>

In a single-tenant environment like ASE, your app is deployed directly into a virtual network, allowing for granular network security management using firewalls, user-defined routes, and network security groups. Although similar outcomes can be achieved in a multi-tenant model with additional configurations (such as private endpoints), the single-tenant model provides these features by default.

<Callout icon="triangle-alert">
  The single-tenant model is typically more expensive. Azure App Service uses an isolated plan to create an ASE.
</Callout>

***

## Configuring Networking in the Azure Portal

The following sections detail how to configure networking settings for your App Service within the Azure portal.

### Accessing Inbound Traffic Settings

To manage inbound traffic, navigate to the Networking section in the App Service portal. By default, public access is enabled without restrictions. Access restrictions can be configured to allow traffic only from specified IP addresses or virtual networks.

<Frame>
  ![The image shows the "Access Restrictions" settings page in Microsoft Azure, where public network access and site access rules can be configured. It displays options for enabling or disabling network access and setting allow/deny rules for site traffic.](https://kodekloud.com/kk-media/image/upload/v1752866362/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/access-restrictions-azure-settings.jpg)
</Frame>

### Scaling Up for Additional Features

Scaling up your App Service plan can unlock additional networking features such as an app assigned IP address or private endpoints. For instance, upgrading from the Basic to the Standard plan can provide these configurations.

<Frame>
  ![The image shows a Microsoft Azure portal screen displaying the "Scale up (App Service plan)" options for a web app, with various pricing plans and configurations listed. A notification indicates that an app service plan was updated successfully.](https://kodekloud.com/kk-media/image/upload/v1752866364/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/azure-portal-scale-up-options.jpg)
</Frame>

After scaling up, the networking configuration page displays additional settings, including custom domains, inbound and outbound configurations, and the app assigned IP address.

<Frame>
  ![The image shows the networking configuration page of a web app in the Microsoft Azure portal, displaying inbound and outbound traffic settings.](https://kodekloud.com/kk-media/image/upload/v1752866365/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/azure-portal-networking-configuration.jpg)
</Frame>

### Creating an App Service Environment

To create an App Service Environment in Azure, select the "Add" option within the App Service Environments section. Note that subscription limitations may restrict creation in some cases. In the ASE configuration form, you will notice that the domain name differs from that used in multi-tenant App Services (e.g., appserviceenvironment.net instead of azurewebsites.net).

Fill in the necessary details, such as naming the environment and choosing whether the app should be exposed externally or internally (using an internal load balancer).

<Frame>
  ![The image shows a form for creating an App Service Environment v3 in Azure, with fields for project details, instance details, and virtual IP options. It includes options for selecting a subscription, resource group, and naming the environment.](https://kodekloud.com/kk-media/image/upload/v1752866367/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/azure-app-service-environment-form.jpg)
</Frame>

During the ASE setup, you must select a virtual network because ASEs are deployed within a specific virtual network. Additional settings include hardware isolation and redundancy configurations.

<Frame>
  ![The image shows a configuration page for creating an App Service Environment v3 in Azure, focusing on networking settings such as virtual network, subnet, DNS, and inbound IP address options.](https://kodekloud.com/kk-media/image/upload/v1752866368/notes-assets/images/AZ-204-Developing-Solutions-for-Microsoft-Azure-App-Service-Networking/azure-app-service-environment-v3-config.jpg)
</Frame>

***

## Summary

This article reviewed the essential concepts and configurations for Azure App Service Networking. We explored both the multi-tenant public service model and the single-tenant App Service Environment, highlighting their inbound and outbound networking features. Additionally, a step-by-step walkthrough demonstrated how to configure these settings in the Azure portal, including scaling up your service plan and creating an ASE.

With these insights, you now have a solid understanding of how Azure App Service Networking works and how to optimize it for your applications.

For further reading, see the following resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-204-developing-solutions-for-microsoft-azure/module/94d21b81-de82-4d33-a347-4404baa9f869/lesson/c87a1e42-aeff-483c-86bb-8ec8da12a7e1" />
</CardGroup>
