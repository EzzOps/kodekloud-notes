# Certification Details

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Introduction/Certification-Details/page

Overview of AZ-700 certification mapping exam domains, core Azure networking topics, and study and exam preparation guidance

Before starting the technical modules, review how the skills you’ll practice map to the official AZ-700: Designing and Implementing Microsoft Azure Networking Solutions certification. This guide breaks down each exam domain, highlights the core topics you must master, and explains the exam experience and resources you can use during the test.

The AZ-700 exam is organized into five primary domains:

* Design and implement core network infrastructure
* Design, implement, and manage connectivity services
* Design and implement application delivery services
* Design and implement private access to Azure services
* Secure network connectivity to Azure resources

Each domain reflects real-world responsibilities expected of an Azure networking engineer. Below is a concise roadmap, followed by focused sections with the key topics for each domain.

| Domain                           | Exam Weight | Key Topics                                                                                                                       |
| -------------------------------- | ----------: | -------------------------------------------------------------------------------------------------------------------------------- |
| Core network infrastructure      |      25–30% | Azure Virtual Networks (VNets), Public IPs, DNS and name resolution, Cross-VNet connectivity, routing, Azure Virtual Network NAT |
| Connectivity services            |      20–25% | Azure VPN Gateway, Azure Virtual WAN, ExpressRoute, hybrid connectivity patterns                                                 |
| Application delivery services    |      15–20% | Azure Load Balancer, Application Gateway (incl. WAF), Traffic Manager, Front Door                                                |
| Private access to Azure services |      15–20% | Virtual Network service endpoints, Azure Private Link and private endpoints                                                      |
| Security                         |      10–15% | Network Security Groups (NSGs), Azure Firewall, DDoS Protection, Web Application Firewall (WAF)                                  |

Design and implement core networking infrastructure (25–30%)
This largest domain covers Azure networking fundamentals and the building blocks used to design, deploy, and operate networks in Azure. Expect hands-on tasks and scenarios involving:

* Designing and configuring Azure Virtual Networks (VNets)
* Assigning and managing Public IP addresses
* Implementing DNS and name resolution strategies
* Enabling Cross-VNet connectivity patterns
* Configuring routing and Azure Virtual Network NAT for controlled internet access

<Frame>
  <img alt="The image shows the topics of the AZ-700 Certification, focusing on designing and implementing core networking infrastructure. It lists specific tasks like exploring Azure Virtual Networks, enabling Cross-VNet connectivity, and configuring internet access with Azure Virtual NAT." />
</Frame>

Mastering these fundamentals prepares you to design scalable, resilient Azure network topologies.

Connectivity services
This domain focuses on connecting distributed environments—on-premises datacenters, branch offices, and cloud deployments—reliably and at scale. Key skills include:

* Deploying and configuring Azure VPN Gateway (site-to-site, point-to-site)
* Designing Azure Virtual WAN hub-and-spoke topologies for large-scale connectivity
* Implementing ExpressRoute for private, high-throughput connections
* Integrating hybrid connectivity patterns and failover strategies

<Frame>
  <img alt="The image outlines topics for the AZ-700 Certification, focusing on designing, implementing, and managing connectivity services, including Azure VPN gateway, Azure ExpressRoute, Azure Virtual WANs, and hybrid connectivity methods." />
</Frame>

These capabilities enable you to design dependable, high-performance hybrid and multi-site networks.

Application delivery services (15–20%)
This section covers services used to deliver applications with high availability, optimal performance, and global reach. Focus areas include:

* Azure Load Balancer (layer 4) for high-throughput traffic distribution
* Azure Application Gateway and Web Application Firewall (WAF) for layer 7 security and routing
* Azure Traffic Manager for DNS-based traffic routing and failover
* Azure Front Door for global HTTP(S) routing, acceleration, and edge-based WAF

<Frame>
  <img alt="The image outlines topics for the AZ-700 certification, focusing on designing and implementing application delivery services, including Azure Load Balancer, Application Gateway, Traffic Manager, and Front Door." />
</Frame>

Understanding when to use each service and how to combine them is critical for delivering resilient, performant applications.

Private access to Azure services
This domain covers patterns for restricting access to Azure PaaS and platform services so traffic remains on private IPs within your virtual network:

* Virtual Network service endpoints for direct network-level access
* Azure Private Link & private endpoints for private connectivity to platform and partner services

<Frame>
  <img alt="The image outlines a topic from the AZ-700 Certification, focusing on designing and implementing private access to Azure services. It includes subtopics like Virtual Network Service Endpoints and Private Link Services and Private Endpoints." />
</Frame>

These features help you secure service access and meet compliance requirements by keeping traffic inside your VNet.

Security
The security domain tests your ability to implement and operate network security controls to protect Azure resources from threats:

* Network Security Groups (NSGs) for traffic filtering
* Azure Firewall for centralized, stateful filtering and policy enforcement
* DDoS Protection for resiliency against volumetric attacks
* Web Application Firewall (WAF) to protect HTTP(S) workloads

<Frame>
  <img alt="The image outlines topics for the AZ-700 Certification, focusing on securing network connectivity to Azure resources, including configuring network security groups, Azure Firewall, DDoS protection, and web application firewalls." />
</Frame>

These controls are essential for defending enterprise-grade Azure network architectures.

Exam alignment and value
This AZ-700 roadmap maps directly to Microsoft’s exam objectives and prepares you for both conceptual design decisions and hands-on implementation tasks. Passing the AZ-700 validates that you can design, secure, and deliver enterprise-scale Azure networking solutions.

Microsoft Certified: Azure Network Engineer Associate
Refer to the official Microsoft certification page for exam scope, measured skills, and scheduling:

* Microsoft certification page: [https://learn.microsoft.com/certifications/azure-network-engineer/](https://learn.microsoft.com/certifications/azure-network-engineer/)

On that page you’ll find:

* Detailed skills measured by AZ-700
* Microsoft Learn module links and hands-on labs
* Practice exam and scheduling options
* Recertification and exam policies

<Frame>
  <img alt="The image is a screenshot of a webpage describing the Microsoft Certified Azure Network Engineer Associate exam details, including the content assessed, available languages, and associated costs. There are options for scheduling the exam and information about accommodations and certification renewal." />
</Frame>

Exam cost and logistics
The exam fee in the United States is USD 165; pricing varies by country and taxes may apply. Check the certification page for the latest pricing and regional availability.

Documentation during the exam
Microsoft permits access to Microsoft Learn documentation from within the exam interface. This is especially useful for questions that require precise service limits or configuration details (for example, maximum connections supported by specific VPN Gateway SKUs). Practice navigating Microsoft Learn so you can quickly locate authoritative answers under timed conditions.

<Callout icon="lightbulb">
  You can use [Microsoft Learn](https://learn.microsoft.com/) during the exam to look up documentation, service limits, and configuration examples. Practice quick searches and bookmarking relevant pages so you can retrieve information efficiently during the test.
</Callout>

Exam interface and the sandbox
When you launch the exam, the interface offers side-by-side panes (question panel + documentation/sandbox). Use the built-in split-view to open Microsoft Learn alongside your questions. Avoid detaching or popping out documentation into a separate browser window while the exam is running.

<Callout icon="warning">
  Do not pop out the documentation window during the exam — some candidates report this can interrupt or break the exam session. Use the integrated split view provided by the exam platform.
</Callout>

Final tips

* Practice hands-on: build VNets, configure VPN/ExpressRoute, deploy Application Gateway, and test Private Link and NSGs in a sandbox subscription.
* Use Microsoft Learn modules and labs aligned with AZ-700 objectives.
* Time-box practice exams to improve speed and exam navigation.
* Focus on design trade-offs: cost, latency, scalability, and security for each solution.

Links and references

* Microsoft Learn — AZ-700 exam page: [https://learn.microsoft.com/certifications/azure-network-engineer/](https://learn.microsoft.com/certifications/azure-network-engineer/)
* Microsoft Learn docs: [https://learn.microsoft.com/](https://learn.microsoft.com/)
* Azure networking concepts: [https://learn.microsoft.com/azure/networking/](https://learn.microsoft.com/azure/networking/)

With consistent study, hands-on practice, and familiarity with the documentation, you’ll be well prepared to pass AZ-700 and demonstrate the skills of an Azure Network Engineer.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/59314846-5982-4096-a4a3-16d34d72f38a/lesson/abac71a7-720f-4f41-a062-1ca1c4eff813" />
</CardGroup>
