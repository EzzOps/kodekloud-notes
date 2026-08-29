# Troubleshooting DNS

Source: https://notes.kodekloud.com/docs/Demystifying-DNS/Miscellaneous/Troubleshooting-DNS/page

This article provides a comprehensive guide for troubleshooting DNS issues, covering common problems and systematic diagnostic steps.

Troubleshooting DNS can be challenging because it involves multiple systems interacting—from your local machine to the authoritative nameserver—and handling the response on its way back. Understanding the complete flow is essential for diagnosing and resolving issues.

![The image illustrates the process of connecting a device to a nameserver using DNS, showing the flow from a home network through various resolvers to authoritative DNS servers on the internet.](https://kodekloud.com/kk-media/image/upload/v1752873241/notes-assets/images/Demystifying-DNS-Troubleshooting-DNS/dns-connection-process-diagram.jpg)

Different applications and platforms may implement distinct caching lifecycles. For example, you might execute a DNS command that correctly resolves a domain name:

![The image illustrates the concept of caching with icons of a trash bin, gears, and a web interface, highlighting that caching has different lifecycles per application or platform.](https://kodekloud.com/kk-media/image/upload/v1752873242/notes-assets/images/Demystifying-DNS-Troubleshooting-DNS/caching-concept-lifecycles-icons.jpg)

Yet, if your browser does not show the expected result, it could be because the operating system caches DNS records for a specified period while the browser uses a separate caching duration.

Below is an example using the dig command to query DNS records:

```python theme={null}
$ dig example.com
; <<>> DiG 9.18.28-0ubuntu0.24.04.1-Ubuntu <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 39669
;; flags: qr rd ra; QUERY: 1, ANSWER: 6, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;example.com.            IN      A

;; ANSWER SECTION:
example.com.            103     IN      A       96.7.128.175
example.com.            103     IN      A       96.7.128.198
example.com.            103     IN      A       23.192.228.80
example.com.            103     IN      A       23.192.228.84
example.com.            103     IN      A       23.215.0.136
example.com.            103     IN      A       23.215.0.138

;; Query time: 30 msec
;; SERVER: 10.255.255.254#53(10.255.255.254) (UDP)
;; WHEN: Wed Jan 15 20:10:51 CST 2025
;; MSG SIZE  rcvd: 136
```

The difference in caching durations between the operating system and the browser can lead to inconsistencies. Below is a quick overview of common DNS issues and initial troubleshooting guidelines:

1. Communication Issues: Systems may be unable to communicate due to network problems.
2. Slow DNS: Overloaded resolvers or nameservers can result in slow response times.
3. Incorrect DNS Responses: Outdated cache records or unsynchronized authoritative nameservers can return wrong responses.

![The image lists three basic DNS issues: networking aspects, slow DNS, and wrong DNS responses.](https://kodekloud.com/kk-media/image/upload/v1752873243/notes-assets/images/Demystifying-DNS-Troubleshooting-DNS/dns-issues-networking-slow-responses.jpg)

Let's break down each category and review the appropriate troubleshooting steps.

## Networking-Related DNS Issues

When encountering networking-related DNS problems, begin by checking basic connectivity. Verify that your network interface is configured correctly and determine whether the problem stems from DNS specific issues or overall internet connectivity.

First, test connectivity by pinging a reliable public DNS server:

```bash theme={null}
$ ping 8.8.8.8
Pinging 8.8.8.8 [8.8.8.8] with 32 bytes of data:
Reply from 8.8.8.8: bytes=32 time=42ms TTL=116
Reply from 8.8.8.8: bytes=32 time=43ms TTL=116
Reply from 8.8.8.8: bytes=32 time=40ms TTL=116
Reply from 8.8.8.8: bytes=32 time=41ms TTL=116

Ping statistics for 8.8.8.8:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 40ms, Maximum = 43ms, Average = 41ms
```

Next, inspect if firewall rules or restrictions are blocking port 53 (UDP or TCP). Use Telnet to verify connectivity:

```bash theme={null}
$ telnet dns-server 53
Trying 24.77.125.34...
Connected to 24.77.125.34.
Escape character is '^]'.
^]
```

> **lightbulb** VPN configurations can lead to DNS issues by introducing conflicts in network routing. Disconnect from the VPN to test if it affects DNS behavior.

![The image illustrates a person unplugging a cable from a device, with text suggesting that VPN conflicts can cause DNS leaks or routing issues and advising to check if disconnecting the VPN resolves the issue.](https://kodekloud.com/kk-media/image/upload/v1752873245/notes-assets/images/Demystifying-DNS-Troubleshooting-DNS/vpn-conflicts-dns-leaks-diagram.jpg)

## Slow DNS Resolution

Slow DNS responses generally indicate that a server in the resolution chain is overloaded or responding slowly. This may be noticeable when new websites take longer than usual to load. To diagnose slow DNS responses, use the dig command with the +trace option. This command steps through the entire DNS resolution process, exposing the time taken at each phase:

```bash theme={null}
$ dig +trace example.com
```

You can also combine the time command with dig to benchmark the resolver's speed directly. The following example queries Google’s DNS server:

```bash theme={null}
$ time dig @8.8.8.8 example.com
; <<>> DiG 9.10.6 <<>> @8.8.8.8 example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 17093
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 6, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDSECTION:
; EDNS: version: 0, flags: udp: 512
;; QUESTION SECTION:
;example.com.            IN      A

;; ANSWER SECTION:
example.com.            231     IN      A       23.192.228.84
example.com.            231     IN      A       23.215.0.136
example.com.            231     IN      A       96.7.128.175
example.com.            231     IN      A       96.7.128.198
example.com.            231     IN      A       23.192.228.80
example.com.            231     IN      A       23.215.0.138

;; Query time: 35 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Fri Jan 31 15:27:45 CST 2025
;; MSG SIZE  rcvd: 136

dig @8.8.8.8 example.com 0.00s user 0.01s system 22% cpu 0.052 total
```

Numerous online tools are available that can benchmark the performance of various DNS resolvers.

## Incorrect DNS Responses

Incorrect or inconsistent DNS responses often stem from caching complications or unsynchronized authoritative nameservers. This is a common and challenging DNS issue to diagnose.

![The image illustrates two types of DNS issues: caching problems and unsynchronized authoritative nameservers.](https://kodekloud.com/kk-media/image/upload/v1752873246/notes-assets/images/Demystifying-DNS-Troubleshooting-DNS/dns-issues-caching-nameservers.jpg)

Ruijan Paul, an engineer highly regarded for his DNS learning resources, suggests an outward-in approach when diagnosing caching issues. Start from external components, such as public resolvers, and work inward. Even if you clear your local operating system's cache, stale records may persist if upstream caches continue to provide outdated data.

Many public resolvers offer web tools for clearing the DNS cache. For example, major content delivery network providers like Akamai provide mechanisms to invalidate or remove cached entries.

![The image is a slide titled "Exploring Cache Tools – Akamai," showing a screenshot of Akamai's tech documentation on purge cache methods, specifically focusing on invalidate and delete methods.](https://kodekloud.com/kk-media/image/upload/v1752873247/notes-assets/images/Demystifying-DNS-Troubleshooting-DNS/exploring-cache-tools-akamai.jpg)

> **lightbulb** If your system uses an ISP's resolver, clearing caches on public resolvers like Cloudflare or Google may not produce any changes. In these cases, rebooting or resetting your router might help clear some cached records.

![The image illustrates the process of resetting a router when using an ISP resolver, highlighting resolver resets for Windows OS, Linux OS, DNS servers like BIND, and MacOS.](https://kodekloud.com/kk-media/image/upload/v1752873248/notes-assets/images/Demystifying-DNS-Troubleshooting-DNS/router-reset-isp-resolver-guide.jpg)

## Operating System-Level DNS Troubleshooting

### Windows

For Windows users, you can clear and view the DNS cache as well as release and renew your IP configuration using the following commands:

```bash theme={null}
