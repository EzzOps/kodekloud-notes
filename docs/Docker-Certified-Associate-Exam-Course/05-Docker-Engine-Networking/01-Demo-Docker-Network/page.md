# Demo Docker Network

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Networking/Demo-Docker-Network/page

This lesson explores Docker networking fundamentals including default networks, custom bridge networks, DNS resolution, and connecting or disconnecting containers from networks.

In this lesson, we’ll explore Docker networking fundamentals: default networks, custom bridge networks, DNS resolution, and how to connect or disconnect containers from networks. By the end, you’ll understand how Docker manages container networking and how to customize it for your applications.

## Listing Default Networks

Docker comes with three built-in networks:

| Network | Driver | Scope | Description                                  |
| ------- | ------ | ----- | -------------------------------------------- |
| bridge  | bridge | local | Default network for newly created containers |
| host    | host   | local | Container shares the host’s network stack    |
| none    | null   | local | No networking; containers are isolated       |

To see these networks:

```bash theme={null}
docker network ls
```

Example output:

```bash theme={null}
$ docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
cf10938f5edf   bridge    bridge    local
d4f46412e7e9   host      host      local
b5b0ab8c1665   none      null      local
```

## Inspecting the Bridge Network

To view details such as subnet configuration and gateway:

```bash theme={null}
docker network inspect bridge
```

Key fields:

```json theme={null}
[
  {
    "Name": "bridge",
    "Driver": "bridge",
    "IPAM": {
      "Config": [
        {
          "Subnet": "172.17.0.0/16",
          "Gateway": "172.17.0.1"
        }
      ]
    },
    "Options": {
      "com.docker.network.bridge.default_bridge": "true",
      "com.docker.network.bridge.enable_icc": "true",
      "com.docker.network.bridge.enable_ip_masquerade": "true",
      "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0"
    }
  }
]
```

<Callout icon="lightbulb">
  The IPAM (IP Address Management) section shows how Docker assigns subnets and gateways.
</Callout>

## Running Containers on the Default Bridge

When you start a container without specifying a network, it’s attached to `bridge`:

```bash theme={null}
docker run -itd --name first centos:7
```

Inspect its network settings:

```bash theme={null}
docker inspect first --format '{{json .NetworkSettings}}' | jq
```

```json theme={null}
{
  "Gateway": "172.17.0.1",
  "IPAddress": "172.17.0.2",
  "IPPrefixLen": 16,
  "MacAddress": "02:42:ac:11:00:02",
  "Networks": {
    "bridge": {
      "IPAddress": "172.17.0.2",
      "Gateway": "172.17.0.1",
      "MacAddress": "02:42:ac:11:00:02"
    }
  }
}
```

Create a second container:

```bash theme={null}
docker run -itd --name second centos:7
```

On the default bridge, embedded DNS is **not** enabled. Attempting to ping by container name fails:

```bash theme={null}
docker exec first ping -c 2 second
