# Azure Database offerings

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Just-Enough-Azure-for-AKS/Azure-Database-offerings/page

This article discusses Azure's database offerings, including relational and NoSQL services, highlighting their features, deployment types, and ideal use cases.

When building cloud-native or hybrid applications on Azure, choosing the right database service is critical. Azure’s data platform spans relational and NoSQL offerings, delivering fully managed options, predictable performance, global distribution, and enterprise-grade security.

## At a Glance

| Category                                 | Service                             | Deployment Type | Key Benefits                                   |
| ---------------------------------------- | ----------------------------------- | --------------- | ---------------------------------------------- |
| Azure SQL                                | Azure SQL Database                  | PaaS            | Single DB, elastic pools, Hyperscale scaling   |
|                                          | Azure SQL Managed Instance          | PaaS            | Near 100% SQL Server compatibility             |
|                                          | SQL Server on Azure Virtual Machine | IaaS            | Full OS/SQL control, custom extensions         |
| Open Source Relational Engines           | Azure Database for MySQL            | PaaS            | Community MySQL, high availability, scaling    |
|                                          | Azure Database for MariaDB          | PaaS            | Predictable performance, built-in security     |
|                                          | Azure Database for PostgreSQL       | PaaS            | Single & Flexible Server, HA, enterprise-grade |
| Globally Distributed NoSQL (Multi-Model) | Azure Cosmos DB                     | PaaS            | JSON, MongoDB, Gremlin, Cassandra, Table APIs  |

## Azure SQL Offerings

Azure SQL delivers managed SQL Server–based engines with varying levels of control and compatibility:

| Service                        | Description                                                                             | Ideal Use Case                               |
| ------------------------------ | --------------------------------------------------------------------------------------- | -------------------------------------------- |
| **Azure SQL Database**         | Fully managed single databases, elastic pools, or Hyperscale for large-scale workloads. | New cloud apps, SaaS, rapid scaling          |
| **Azure SQL Managed Instance** | Hosted PaaS instance with near-100% compatibility to on-premises SQL Server.            | Lift-and-shift migrations, legacy apps       |
| **SQL Server on Azure VM**     | Infrastructure-level control over the OS and SQL Server instance.                       | Custom extensions, unsupported PaaS features |

### Deployment and Scaling

```bash theme={null}
