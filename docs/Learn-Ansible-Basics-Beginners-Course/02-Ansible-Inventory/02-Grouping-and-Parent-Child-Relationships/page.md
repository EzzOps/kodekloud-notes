# Sample Inventory File
web       ansible_host=server1.company.com ansible_connection=ssh ansible_user=root
db        ansible_host=server2.company.com ansible_connection=winrm ansible_user=admin
mail      ansible_host=server3.company.com ansible_connection=ssh ansible_ssh_pass=P@#
web2      ansible_host=server4.company.com ansible_connection=winrm
localhost ansible_connection=localhost
```

By starting with this basic inventory configuration, you can concentrate on mastering Ansible fundamentals and later expand your inventory setup as your environment grows more complex.

We encourage you to apply these concepts through practice exercises and explore the rich capabilities of Ansible in managing your infrastructure efficiently.

Happy automating, and see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/d7059d07-b28b-4e04-a4a4-3638100f5266/lesson/ee852353-de0a-47f9-9795-a9afdb7badb7" />
</CardGroup>


# Grouping and Parent Child Relationships

Source: https://notes.kodekloud.com/docs/Learn-Ansible-Basics-Beginners-Course/Ansible-Inventory/Grouping-and-Parent-Child-Relationships/page

This article discusses effective grouping strategies and parent-child relationships in Ansible for managing complex IT infrastructures efficiently.

Imagine you are an IT administrator responsible for a vast and complex infrastructure spanning multiple locations. In such an environment, you may be managing hundreds of servers that serve various roles—such as web servers, database servers, or application servers.

<Frame>
  ![The image illustrates an IT infrastructure overview, showing an IT administrator managing web, database, and application servers within a multinational organization.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881045/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Grouping-and-Parent-Child-Relationships/frame_20.jpg)
</Frame>

Manually managing each server can quickly become overwhelming. For instance, when updating all web servers, manually specifying each host is both time-consuming and prone to error. This is where effective grouping strategies make a significant difference.

By categorizing servers based on roles, geographic locations, or other criteria, you can simplify many routine tasks. For example, grouping all web servers under a common label allows you to apply updates or configuration changes to the entire group with a single command.

<Frame>
  ![The image illustrates the need for grouping in a multinational organization, focusing on web servers and their connections to users and locations.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881046/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Grouping-and-Parent-Child-Relationships/frame_50.jpg)
</Frame>

<Callout icon="lightbulb">
  Ansible’s grouping feature lets you assign a common label to a set of servers, enabling efficient bulk operations.
</Callout>

Ansible's grouping functionality comes to the rescue when managing multiple servers simultaneously. You can define groups that represent collections of servers sharing similar roles. Once a group is defined, targeting that group for updates or configuration changes applies those changes to all associated servers.

However, challenges can arise when servers in the same role are distributed across different locations, each requiring location-specific configurations. If you create separate groups for each location, you might end up duplicating common settings. Ansible's parent-child relationship feature elegantly solves this problem by allowing you to:

* Define a parent group (for example, "Web Servers") to hold common configurations.
* Create child groups (such as "Web Servers US" and "Web Servers EU") for location-specific settings.

<Frame>
  ![The image illustrates the concept of parent-child relationships in Ansible, showing server groupings across different regions on a world map.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881048/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Grouping-and-Parent-Child-Relationships/frame_120.jpg)
</Frame>

## Grouping and Parent-Child Structures in Ansible

Consider an example where you have servers in the US and the EU. Using the INI format, you can define groups with parent-child relationships as follows:

```ini theme={null}
[webservers:children]
webservers_us
webservers_eu

[webservers_us]
server1_us.com ansible_host=192.168.8.101
server2_us.com ansible_host=192.168.8.102
```

In this example, "webservers\_us" and "webservers\_eu" are defined as child groups under the parent group "webservers". This allows you to maintain common configurations at the parent group level while applying specific settings within each child group.

Similarly, in YAML format, you can organize groups using the `hosts` keyword, and establish parent-child relationships with the `children` keyword:

```yaml theme={null}
all:
  children:
    webservers:
      children:
        webservers_us:
          hosts:
            server1_us.com:
              ansible_host: 192.168.8.101
            server2_us.com:
              ansible_host: 192.168.8.102
        webservers_eu:
          hosts:
            server1_eu.com:
              ansible_host: 10.12.0.101
            server2_eu.com:
              ansible_host: 10.12.0.102
```

This YAML structure begins by defining all groups under the `all` key. It then creates a parent group "webservers" with its respective child groups "webservers\_us" and "webservers\_eu". Each child group contains its specific server configurations.

<Callout icon="lightbulb">
  Organizing your servers into groups and establishing parent-child relationships minimizes configuration duplication and streamlines management, resulting in a more efficient and error-free IT infrastructure.
</Callout>

By leveraging Ansible’s grouping and parent-child relationship features, you simplify server management, reduce the risk of configuration errors, and boost operational efficiency across your diverse IT infrastructure.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/d7059d07-b28b-4e04-a4a4-3638100f5266/lesson/f6869f88-9247-49ae-9c55-7d7dfce173ff" />
</CardGroup>
