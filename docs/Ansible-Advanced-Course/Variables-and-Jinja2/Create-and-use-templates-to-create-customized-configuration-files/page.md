# Create and use templates to create customized configuration files

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Variables-and-Jinja2/Create-and-use-templates-to-create-customized-configuration-files/page

Learn to use Jinja2 templates in Ansible for dynamically generating configuration files for web servers.

In this lesson, you'll learn how to harness Jinja2 templates in Ansible to dynamically generate configuration files. Imagine a scenario where you need to set up web servers by deploying a web page (index.html) from your local machine to the default directory on each remote server (for instance, the default directory for nginx). We assume that nginx is already installed on these servers.

## Basic File Copy Using the Copy Module

At first, you might use Ansible’s copy module to transfer a static index.html file to each web server. For example, your inventory file and playbook could be configured as follows:

```ini theme={null}
/etc/ansible/hosts
[web_servers]
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101
web3 ansible_host=172.20.1.102
```

```yaml theme={null}
playbook.yml
- hosts: web_servers
  tasks:
    - name: Copy index.html to remote servers
      copy:
        src: index.html
        dest: /var/www/nginx-default/index.html
```

The local index.html file might look like this:

```html theme={null}
<!-- index.html -->
<!DOCTYPE html>
<html>
<body>
This is a Web Server
</body>
</html>
```

When you run the playbook, the index.html file is copied over to all web servers, displaying a static message upon access.

## Introducing Variables into the Web Page

Suppose the requirement changes and you now need to display the hostname and IP address dynamically on each web server. One solution might involve creating separate versions of the index.html file for each server. For example:

```ini theme={null}
/etc/ansible/hosts
[web_servers]
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101
web3 ansible_host=172.20.1.102
```

```yaml theme={null}
playbook.yml
- hosts: web_servers
  tasks:
    - name: Copy index.html to remote servers
      copy:
        src: index.html
        dest: /var/www/html/
```

```html theme={null}
<!-- index.html for web1 -->
<!DOCTYPE html>
<html>
<body>
This is web1 Server
</body>
</html>
```

```html theme={null}
<!-- index.html for web2 -->
<!DOCTYPE html>
<html>
<body>
This is web2 Server
</body>
</html>
```

```html theme={null}
<!-- index.html for web3 -->
<!DOCTYPE html>
<html>
<body>
This is web3 Server
</body>
</html>
```

This approach is impractical for scalability since the files differ only by the hostname. The better solution is to use a variable within a template file.

## Converting an HTML File into a Jinja2 Template

By creating one consolidated template file with a variable placeholder, you can avoid managing multiple static files. Rename your file to indicate its templated nature, for example, index.html-template or, even better, index.html.j2. Insert a Jinja2 variable for the server name:

```ini theme={null}
/etc/ansible/hosts
[web_servers]
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101
web3 ansible_host=172.20.1.102
```

```yaml theme={null}
playbook.yml
- hosts: web_servers
  tasks:
    - name: Copy index.html to remote servers
      copy:
        src: index.html
        dest: /var/www/nginx-default/index.html
```

```html theme={null}
<!-- index.html-template -->
<!DOCTYPE html>
<html>
<body>
This is {{ name }} Server
</body>
</html>
```

Remember, once you convert your static HTML file into a Jinja2 template, it will no longer serve directly as a static file. It is meant to generate a customized file on each remote host. Therefore, it is best practice to add the “.j2” extension:

```ini theme={null}
/etc/ansible/hosts
[web_servers]
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101
web3 ansible_host=172.20.1.102
```

```yaml theme={null}
playbook.yml
- hosts: web_servers
  tasks:
    - name: Copy index.html to remote servers
      copy:
        src: index.html
        dest: /var/www/nginx-default/index.html
```

```html theme={null}
<!-- index.html.j2 -->
<!DOCTYPE html>
<html>
<body>
This is {{ name }} Server
</body>
</html>
```

!!! note "Note"
Using the copy module will not process variables in the template. To render the variables, you need to switch to the template module.

## Using the Template Module

The template module is designed to process Jinja2 templates. It replaces the variables with real values and then copies the resulting file to the target server. Update your playbook as follows and use the built-in Ansible variable  to automatically insert the current host's name:

```ini theme={null}
/etc/ansible/hosts
[web_servers]
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101
web3 ansible_host=172.20.1.102
```

```yaml theme={null}
playbook.yml
- hosts: web_servers
  tasks:
    - name: Process and deploy the index.html template
      template:
        src: index.html.j2
        dest: /var/www/nginx-default/index.html
```

```html theme={null}
<!-- index.html.j2 -->
<!DOCTYPE html>
<html>
<body>
This is {{ inventory_hostname }} Server
</body>
</html>
```

With this configuration, when you run the playbook, Ansible processes the template for each host. It replaces  with the corresponding host’s name, generating a unique index.html file for every server.

## What Happens During Execution

When executing the playbook, Ansible spawns a separate process for each host. This process gathers facts—such as inventory\_hostname and other host-specific information—and then executes the tasks. The template module generates a personalized index.html file with the correct hostname, and subsequently copies the file to the designated directory (/var/www/nginx-default/index.html).

For example, after processing, the rendered file for web1 might appear as:

```html theme={null}
<!DOCTYPE html>
<html>
<body>
This is web1 Server
</body>
</html>
```

Similar customized files will be created for web2 and web3.

## Applying the Template Approach to Other Configuration Files

The templating techniques showcased for the web page can be applied to various other configuration files like nginx or Redis configurations. For instance, an nginx configuration file with variable placeholders might look like this:

```nginx theme={null}
server {
    location / {
        fastcgi_pass {{ host }}:{{ port }};
        fastcgi_param QUERY_STRING \$query_string;
    }

    location ~ \.(gif|jpg|png)$ {
        root {{ image_path }};
    }
}
```

For a Redis configuration file, you can utilize Jinja2 filters to provide default values:

```text theme={null}
bind {{ ip_address }}
protected-mode yes
port {{ redis_port | default('6379') }}
tcp-backlog 511
