# Explore Azure Resource Locks

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Implement-Security-and-Validate-Code-Bases-for-Compliance/Explore-Azure-Resource-Locks/page

Resource locks in Azure prevent accidental modifications or deletions of critical resources, ensuring stability and security in production environments.

Resource locks in Azure are essential for preventing accidental modifications or deletions of critical resources. Whether you’re preparing for the [AZ-400 exam](https://learn.microsoft.com/en-us/certifications/exams/az-400/) or managing production environments, understanding how to apply and manage locks will help you maintain stability and security.

## Lock Types in Azure

Azure offers two built-in lock levels:

| Lock Type     | Description                                                              | Operations Allowed  |
| ------------- | ------------------------------------------------------------------------ | ------------------- |
| Cannot Delete | Prevents deletion but permits all other operations (read, write, update) | Read, Write, Update |
| Read Only     | Blocks create, update, and delete operations                             | Read only           |

### Cannot Delete Lock

The **Cannot Delete** lock (also known as `CanNotDelete`) ensures a resource remains in place:

* Read and write operations are fully supported.
* Any attempt to delete the resource is blocked.

Use this lock for resources such as production databases, critical storage accounts, or network appliances.

```bash theme={null}
