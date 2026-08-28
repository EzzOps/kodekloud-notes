# MongoDB

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Database-Basics/MongoDB/page

This guide introduces MongoDB, covering installation, configuration, basic operations, and troubleshooting of a scalable NoSQL document database.

In this guide, we introduce MongoDB, a high-performance, scalable NoSQL document database. You will learn what MongoDB is, how to install and configure a MongoDB server, and how to perform basic operations and troubleshooting. MongoDB stores data in JSON-like documents gathered into collections, and multiple collections form a database. A single MongoDB server can host multiple databases. There are two main editions available: the free Community Edition and the commercial Enterprise Edition.

Below are examples of JSON documents demonstrating how data can be structured in MongoDB:

```json theme={null}
{
  "name": "John Doe",
  "age": 45,
  "location": "New York",
  "salary": 5000
}
```

```json theme={null}
{
  "name": "Dave Smith",
  "age": 34,
  "location": "New York",
  "salary": 4000,
  "organization": "ACME"
}
```

```json theme={null}
{
  "name": "Aryan Kumar",
  "age": 10,
  "location": "New York",
  "Grade": "A"
}
```

```json theme={null}
{
  "name": "Lily Oliver",
  "age": 15,
  "location": "Bangalore",
  "Grade": "B"
}
```

```json theme={null}
{
  "name": "Lauren Rob",
  "age": 13,
  "location": "Bangalore",
  "Grade": "C"
}
```

MongoDB is available as a managed cloud service through [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and as an on-premises server. This article focuses on installing a local (on-premises) MongoDB server.

<Frame>
  ![The image is an informational slide about MongoDB, describing it as a scalable document database available in cloud and server versions.](https://kodekloud.com/kk-media/image/upload/v1752873425/notes-assets/images/DevOps-Pre-Requisite-Course-MongoDB/frame_70.jpg)
</Frame>

<Callout icon="lightbulb">
  The Community Edition is free and widely used for development and prototyping. The Enterprise Edition offers additional features and support for commercial deployments.
</Callout>

## Installing MongoDB

The first step is configuring your package management system with the MongoDB repository and installing the `mongodb-org` package. Although best practices for user creation and security are available in the official documentation, this guide uses a simplified approach.

For instance, on a system using yum, install MongoDB with:

```bash theme={null}
yum install mongodb-org
```

Create a repository file (e.g., `/etc/yum.repos.d/mongodb-org-4.2.repo`) with the content below to configure the MongoDB repository:

```ini theme={null}
[mongodb-org-4.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc
```

<Frame>
  ![The image shows a MongoDB installation interface, offering options to download the Community Server, select version, OS, and package, with additional resources like release notes.](https://kodekloud.com/kk-media/image/upload/v1752873426/notes-assets/images/DevOps-Pre-Requisite-Course-MongoDB/frame_90.jpg)
</Frame>

## Starting the MongoDB Service

After installation, start the MongoDB system service named `mongod` and verify its status. The main log file is located at `/var/log/mongodb/mongod.log`.

Start MongoDB using:

```bash theme={null}
systemctl start mongod
```

Then check the service status:

```bash theme={null}
systemctl status mongod
```

A sample output may appear as follows:

```bash theme={null}
● mongod.service - MongoDB Database Server
   Loaded: loaded (/usr/lib/systemd/system/mongod.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2020-03-21 18:43:53 UTC; 1min 46s ago
     Docs: https://docs.mongodb.org/manual
  Process: 4224 ExecStart=/usr/bin/mongod $OPTIONS (code=exited, status=0/SUCCESS)
  Process: 4222 ExecStartPre=/usr/bin/chmod 0755 /var/run/mongodb (code=exited, status=0/SUCCESS)
  Process: 4220 ExecStartPre=/usr/bin/chown mongodb:mongodb /var/run/mongodb (code=exited, status=0/SUCCESS)
  Process: 4219 ExecStartPre=/usr/bin/mkdir -p /var/run/mongodb (code=exited, status=0/SUCCESS)
 Main PID: 4227 (mongod)
   CGroup: /system.slice/mongod.service
           └─4227 /usr/bin/mongod -f /etc/mongod.conf
```

When MongoDB starts, the log file at `/var/log/mongodb/mongod.log` provides details about the server startup, including the MongoDB version, and indicates that it is listening on port 27017 of the loopback IP address (127.0.0.1). This default setting permits connections only from the local system—a secure default for development that should be adjusted for production environments.

A sample log snippet is shown below:

```plaintext theme={null}
cat /var/log/mongodb/mongod.log
2020-03-21T18:43:52.820+0000 I CONTROL  [main] ***** SERVER RESTARTED *****
2020-03-21T18:43:52.823+0000 I CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2020-03-21T18:43:52.982+0000 I CONTROL  [initandlisten] MongoDB starting: pid=4227 port=27017
2020-03-21T18:43:52.982+0000 I CONTROL  [initandlisten] db version v4.2.3
2020-03-21T18:43:52.982+0000 I CONTROL  [initandlisten] git version: 6874650b362138d74be53d366bebfc321ea32d4
2020-03-21T18:43:52.982+0000 I CONTROL  [initandlisten] OpenSSL version: OpenSSL 1.0.1e-fips 11 Feb 2013
2020-03-21T18:43:52.998+0000 I NETWORK  [listener] Listening on /tmp/mongodb-27017.sock
2020-03-21T18:43:53.521+0000 I NETWORK  [listener] Listening on 127.0.0.1
2020-03-21T18:43:53.521+0000 I NETWORK  [listener] waiting for connections on port 27017
```

## MongoDB Configuration

The MongoDB configuration file (`/etc/mongod.conf`) allows you to modify settings such as port number, storage location, and network bind addresses. Here’s an example configuration:

```yaml theme={null}
