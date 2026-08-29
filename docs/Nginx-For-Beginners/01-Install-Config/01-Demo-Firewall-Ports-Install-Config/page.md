# Demo Firewall Ports Install Config

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Install-Config/Demo-Firewall-Ports-Install-Config/page

Configuring UFW firewall and ports for NGINX and a Flask app, verifying services and recommending reverse proxying and SSH safety.

You can quickly verify NGINX and a backend Flask app from the server itself using `curl`. That confirms the services are running from the server/engineer perspective, but it doesn't prove the same results from the client/browser perspective.

Below are the two checks we ran locally on the host to confirm both NGINX and the Flask app were responding:

```bash theme={null}
bob@alpine-host ~ ➜  curl localhost
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
  body {
    width: 35em;
    margin: 0 auto;
    font-family: Tahoma, Verdana, Arial, sans-serif;
  }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

bob@alpine-host ~ ➜  curl localhost:5000
<h1>Hello, Human!</h1>[Not Authenticated]
bob@alpine-host ~ ➜  clear
```

<Frame>
  <img alt="A simple network diagram showing users on the left connecting through a &#x22;Network Cloud&#x22; to backend services on the right: NGINX (Port 80, 443) and a Flask app (Port 5000)." />
</Frame>

The diagram above illustrates the lab environment:

* Users (left) reach services over the Internet (network cloud).
* Services (right):
  * NGINX serves the default page on port `80` (HTTP).
  * A small Flask application listens on port `5000`.

In this lab the firewall is initially inactive, so both services are reachable directly from a browser or the lab UI “view ports” feature (you can open `80` or `5000` in a browser tab from the UI). This setup is convenient for learning but not representative of a secure production environment.

UFW (Uncomplicated Firewall) is a simple frontend to manage Linux iptables rules. See the official UFW documentation for details: [https://help.ubuntu.com/community/UFW](https://help.ubuntu.com/community/UFW). The recommended workflow is to enable UFW and explicitly allow only the ports your system needs.

> **lightbulb** Before enabling the firewall, always make sure you allow SSH access (for example `sudo ufw allow OpenSSH` or `sudo ufw allow 22/tcp`) so you don't lock yourself out of the server.

## Typical UFW workflow

Below is a step-by-step example showing how to check UFW status, allow SSH, enable the firewall, add web ports, and verify the rules:

```bash theme={null}
