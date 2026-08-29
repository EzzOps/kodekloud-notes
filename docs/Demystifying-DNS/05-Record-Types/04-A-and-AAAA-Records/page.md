# Clear DNS cache
$ ipconfig /flushdns

# Display DNS cache
$ ipconfig /displaydns

# Release and renew IP (includes DNS refresh)
$ ipconfig /release
$ ipconfig /renew
```

### Linux

Modern Linux distributions typically use systemd-resolved for DNS caching. If you are operating your own DNS server using BIND, the following commands help manage the service:

```bash theme={null}
$ sudo systemctl start named
$ sudo systemctl stop named
$ sudo systemctl restart named
$ sudo systemctl status named
```

For managing BIND9 without restarting the service, use the rndc tool:

```bash theme={null}
$ sudo rndc flush
```

### macOS

Commands to clear the DNS cache on macOS vary depending on the version:

```bash theme={null}
# For modern macOS (Ventura and higher):
$ sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# For older macOS versions (Monterey, Big Sur, or Catalina):
$ sudo killall -HUP mDNSResponder; sudo dscacheutil -flushcache

# For very old macOS versions (pre-Catalina):
$ sudo discoveryutil mdnsflushcache
```

## Application-Level Troubleshooting

Modern web browsers provide specific URLs or internal settings to clear DNS and host caches. For instance, in Opera you can navigate to:

![The image shows instructions for clearing the host cache in the Opera browser, with a search bar containing the URL "opera://net-internals/#dns" and a highlighted option to "Clear host cache."](https://kodekloud.com/kk-media/image/upload/v1752873249/notes-assets/images/Demystifying-DNS-Troubleshooting-DNS/opera-clear-host-cache-instructions.jpg)

For locally running or desktop applications, simply restarting the application might be sufficient to clear its DNS cache.

## Debugging Incorrect DNS Responses

If you suspect that DNS responses are incorrect or inconsistent due to caching issues or unsynchronized authoritative nameservers, query the nameservers directly to compare their responses. Use the following commands with dig or nslookup:

```bash theme={null}
# Query specific nameservers using dig
$ dig @ns1.example.com domain.com
$ dig @ns2.example.com domain.com

# Alternatively, using nslookup
$ nslookup domain.com ns1.example.com
$ nslookup domain.com ns2.example.com
```

If the responses differ, it might indicate a zone transfer or synchronization issue. To further diagnose such discrepancies, check the SOA serial numbers from the authoritative nameservers:

```bash theme={null}
$ dig @ns1.example.com domain.com SOA
...
;; ANSWER SECTION:
domain.com. 3600 IN SOA ns1.example.com. hostmaster.example.com. 2023010101
                3600 1800 1209600 86400
...

$ dig @ns2.example.com domain.com SOA
...
;; ANSWER SECTION:
domain.com. 3600 IN SOA ns2.example.com. hostmaster.example.com. 2023010102
                3600 1800 1209600 86400
...
```

A mismatch in SOA serial numbers confirms a synchronization issue between the nameservers.

By following these structured troubleshooting steps—from network connectivity assessments to operating system and application-level checks—you can systematically identify and resolve many common DNS issues. This approach not only helps in isolating the problem but also ensures that corrective actions are efficiently implemented.

- [Watch Video](https://learn.kodekloud.com/user/courses/demystifying-dns/module/eb686425-78d9-4e58-9903-c2ee56b25f3c/lesson/8290149e-6a5e-4e26-8abb-20070e1cc67b)


# A and AAAA Records

Source: https://notes.kodekloud.com/docs/Demystifying-DNS/Record-Types/A-and-AAAA-Records/page

This article explains how to configure A and AAAA records in DNS, including steps for adding records and testing DNS resolution.

In this lesson, we will explore how to configure A and AAAA records in DNS. While the demo will focus on A records, configuring AAAA records follows an identical process—the only difference is that AAAA records map domain names to IPv6 addresses instead of IPv4.

An A record maps a domain name to an IPv4 address by using a 4-byte address field in DNS packets, whereas a AAAA record maps a domain name to an IPv6 address with a 16-byte address field. Additionally, DNS packet headers include flags to identify the type of each record.

## Obtaining the IP Address from node02

Before updating the DNS zone file, determine the IP address for node02. Since the IP address may change in each playground session, run the following command to capture its current IPv4 address:

```bash theme={null}
bob@node01 ~ > ping node02
PING node02 (192.5.180.8) 56(84) bytes of data.
64 bytes from sandbox-ubuntu-multi-node-tyqrvp25f4w255rv_vm02.1.lej1m5c8m0xsx1upftq3psgz.sandbox-ubuntu-multi-node-tyqrvp25f4w255rv_k: icmp_seq=1 ttl=64 time=0.070 ms
64 bytes from sandbox-ubuntu-multi-node-tyqrvp25f4w255rv_vm02.1.lej1m5c8m0xsx1upftq3psgz.sandbox-ubuntu-multi-node-tyqrvp25f4w255rv_k: icmp_seq=2 ttl=64 time=0.077 ms
```

## Adding the A Record to the Zone File

With the IP address in hand, open your DNS zone file and add an A record to map node02 to its current IPv4 address:

```dns theme={null}
$TTL  300
@  IN  SOA  ns1.my.kodekloudlab.com. admin.my.kodekloudlab.com. (
                  2         ; Serial
              604800         ; Refresh
               86400         ; Retry
              2419200       ; Expire
               604800 )     ; Negative Cache TTL

@  IN  NS  ns1.my.kodekloudlab.com.
ns1    IN  A   127.0.0.1
node02 IN  A   192.5.180.8
```

After saving your changes, restart BIND9 to update the configuration.

## Testing DNS Resolution for a Subdomain

Initially, node02 is treated as a subdomain. Use the commands below to verify DNS resolution:

```bash theme={null}
bob@node01 ~ ➜ sudo vi /etc/bind/db.my.kodekloudlab.com
bob@node01 ~ ➜ sudo systemctl reload named
bob@node01 ~ ➜ dig @localhost node02.my.kodekloudlab.com

; <<>> DiG 9.18.30-Ubuntu <<>> @localhost node02.my.kodekloudlab.com
;; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 35077
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: d465d946485bd720100000067934232e87eb022df3a8ff94 (good)
;; QUESTION SECTION:
;node02.my.kodekloudlab.com. IN A

;; ANSWER SECTION:
node02.my.kodekloudlab.com. 300 IN 192.5.180.8

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(localhost) (UDP)
;; WHEN: Fri Jan 24 02:33:18 EST 2025
;; MSG SIZE  rcvd: 99
bob@node01 ~ ➜
```

## Configuring the Apex Domain

For many web deployments, you may want the apex domain (e.g., my.kodekloudlab.com) to resolve directly to your server’s IP address. This is especially useful when hosting a web server. To do so, update your zone file so that the apex domain uses the at symbol (@) instead of an explicit subdomain:

1. Open the zone file:

   ```bash theme={null}
   bob@node01 ~ ➜ sudo vi /etc/bind/db.my.kodeloudlab.com
   ```

2. Reload the DNS configuration:

   ```bash theme={null}
   bob@node01 ~ ➜ sudo systemctl reload named
   ```

3. Verify the DNS resolution for your domain:

   ```bash theme={null}
   bob@node01 ~ ➜ dig @localhost node02.my.kodeloudlab.com

   ;; <<>> DiG 9.18.30-Ubuntu <<>> @localhost node02.my.kodeloudlab.com
   ;; (2 servers found)
   ;; global options: +cmd
   ;; Got answer:
   ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 35077
   ;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

   ;; OPT PSEUDOSECTION:
   ; EDNS: version: 0, flags:; udp: 1232
   ; COOKIE: d465d94d6485bd720100000067934228e87eb022df3a8ff94 (good)
   ;; QUESTION SECTION:
   ;node02.my.kodeloudlab.com.  IN A

   ;; ANSWER SECTION:
   node02.my.kodeloudlab.com. 300 IN 192.5.180.8

   ;; Query time: 0 msec
   ;; SERVER: 127.0.0.1#53(localhost) (UDP)
   ;; WHEN: Fri Jan 24 02:33:18 EST 2025
   ;; MSG SIZE  rcvd: 99
   ```

Next, update the zone configuration to set the apex domain as follows:

```dns theme={null}
$TTL 300
@ IN SOA ns1.my.kodekouldab.com. admin.my.kodekouldab.com. (
    2          ; Serial
    604800     ; Refresh
    86400      ; Retry
    2419200    ; Expire
    604800     ; Negative Cache TTL
)
@ IN NS ns1.my.kodekouldab.com.
ns1 IN A 127.0.0.1
@ IN A 192.5.180.8
```

Restart BIND9 once again and confirm that the apex domain resolves correctly:

```bash theme={null}
bob@node01 ~ ➜ sudo vi /etc/bind/db.my.kodekloudlab.com
bob@node01 ~ ➜ sudo systemctl reload named
bob@node01 ~ ➜ dig @localhost my.kodekloudlab.com

;; <<>> DiG 9.18.30-Ubuntu <<>> @localhost my.kodekloudlab.com
;; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 39219
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 0a28c953013cb81010000006793426ba2a0f365488a04bf (good)
;; QUESTION SECTION:
;my.kodekloudlab.com.        IN      A

;; ANSWER SECTION:
my.kodekloudlab.com. 300 IN A 192.5.180.8

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(localhost) (UDP)
;; WHEN: Fri Jan 24 02:34:03 EST 2025
;; MSG SIZE  rcvd: 92
```

With this configuration, accessing the apex domain (my.kodekloudlab.com) will directly reach the web server on node02.

> **lightbulb** If you plan to configure a AAAA record, use the same process as for the A record. The only difference is that you will be mapping the domain to an IPv6 address.

## Next Steps: Configuring a CNAME Record

After successfully configuring the A record (and potentially a AAAA record), the next step is to configure a CNAME record. This record type allows you to alias one domain name to another. Detailed steps for configuring a CNAME record will be covered in the following lesson.

For additional DNS configuration best practices and further reading, check out the [DNS Concepts](https://en.wikipedia.org/wiki/Domain_Name_System) documentation.

Happy DNS configuring!

- [Watch Video](https://learn.kodekloud.com/user/courses/demystifying-dns/module/57433009-69d5-4b38-8c58-dde5c3354c62/lesson/b3cf28a3-3295-4d3f-b670-7322201db05f)
