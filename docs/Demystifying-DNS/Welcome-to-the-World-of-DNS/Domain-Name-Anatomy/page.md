# Domain Name Anatomy

Source: https://notes.kodekloud.com/docs/Demystifying-DNS/Welcome-to-the-World-of-DNS/Domain-Name-Anatomy/page

This article explains the structure and delegation of domain names using a land ownership analogy to simplify technical concepts.

Domain names are composed of words separated by dots to clearly delineate ownership and responsibility. In this article, we use a land ownership analogy to explain the structure of domain names, making these technical concepts easier to understand.

## Understanding the Domain Name Structure

Domain names are read from right to left, meaning the rightmost part (e.g., .com) is the least specific. For instance, when you see a domain name like KodeKloud.com, think of KodeKloud as a registered entity on a vast piece of land called "com." In this analogy, ".com" represents a large territory that can be subdivided, much like how organizations reserve portions of land to establish their own services.

The domain registration process mirrors this subdivision of land. When a company registers a domain like kodekloud.com, the domain registrar assigns a portion of the .com territory to that company. This process gives the company the authority to manage its own domain as long as it pays the required annual registration fees through an accredited registrar.

<Frame>
  ![The image illustrates the concept of domain name anatomy, depicting a registration process and subdivision, with explanations about domain responsibilities and authority.](https://kodekloud.com/kk-media/image/upload/v1752873270/notes-assets/images/Demystifying-DNS-Domain-Name-Anatomy/domain-name-anatomy-registration-diagram.jpg)
</Frame>

This delegation of authority allows KodeKloud to create and host services referenced using the kodekloud.com domain. It is important to note that not all domains use the .com suffix. For example, linuxfoundation.org follows a similar process within a different territory known as ".org."

<Frame>
  ![The image illustrates the anatomy of domain names, showing how "kodekloud.com" and "linuxfoundation.org" are subdivisions of their respective top-level domains, ".com" and ".org". It includes diagrams to represent the hierarchical structure of domain names.](https://kodekloud.com/kk-media/image/upload/v1752873271/notes-assets/images/Demystifying-DNS-Domain-Name-Anatomy/domain-names-anatomy-diagram.jpg)
</Frame>

## The DNS Hierarchy: An Inverted Tree

Imagine the DNS system as an inverted tree. At the apex lies the root zone, functioning like a central real estate agency that manages all major territories (top-level domains such as .com, .org, .net, .io, etc.). Directly beneath the top-level domains are the second-level domains, such as linuxfoundation.org and kodekloud.com.

<Frame>
  ![The image illustrates the structure of domain name anatomy, showing the hierarchy from the root zone to top-level domains (TLDs) and second-level domains, resembling an inverted tree.](https://kodekloud.com/kk-media/image/upload/v1752873272/notes-assets/images/Demystifying-DNS-Domain-Name-Anatomy/domain-name-anatomy-structure.jpg)
</Frame>

When KodeKloud registered the kodekloud.com domain via a registrar (like godaddy.com or Cloudflare), the registrar verified the domain’s availability and, recognizing the .com suffix, forwarded a delegation request to Verisign—the organization responsible for the .com domain. Verisign then created a specific zone for KodeKloud, delegating authority over that portion of the territory.

<Callout icon="lightbulb">
  Without this subdivision, all domains ending in .com would remain under Verisign's control, much like a large land parcel that was never subdivided.
</Callout>

<Frame>
  ![The image illustrates the anatomy of a domain name, showing the hierarchical structure of DNS with a focus on the top-level domain (TLD) and second-level domain. It also includes a diagram depicting DNS as an inverted tree.](https://kodekloud.com/kk-media/image/upload/v1752873274/notes-assets/images/Demystifying-DNS-Domain-Name-Anatomy/domain-name-anatomy-dns-diagram.jpg)
</Frame>

## Subdomains and Further Delegation

Delegation enables domain owners to create subdomains within their zones. For example, the subdomain engineer.kodekloud.com represents a specific service but remains under the authority of the kodekloud.com zone. KodeKloud can further add nested subdomains—such as example1.engineer.kodekloud.com or example2.engineer.kodekloud.com—without changing the managing zone.

<Frame>
  ![The image illustrates the anatomy of a domain name, showing the hierarchy from the root zone to the top-level domain (TLD) and second-level domain, using "example1.engineer.kodekloud.com" as an example.](https://kodekloud.com/kk-media/image/upload/v1752873275/notes-assets/images/Demystifying-DNS-Domain-Name-Anatomy/domain-name-anatomy-example1.jpg)
</Frame>

Similarly, linuxfoundation.org can host services under subdomains like training.linuxfoundation.org while still being managed within the same zone administered by the Public Interest Registry.

<Frame>
  ![The image illustrates the anatomy of domain names, showing the structure from the root zone to top-level domains (TLDs) like ".com" and ".org," with examples and associated organizations.](https://kodekloud.com/kk-media/image/upload/v1752873276/notes-assets/images/Demystifying-DNS-Domain-Name-Anatomy/domain-name-anatomy-structure-2.jpg)
</Frame>

Domain registration companies ensure that each subdivision is properly documented. When KodeKloud initiated the registration of kodekloud.com, the registrar started the delegation process with Verisign, which then granted operational control over the specific zone.

Imagine a scenario in which KodeKloud wants to sell the engineer.kodekloud.com service to another company while maintaining the same subdomain name. Initially, both coldcloud.com and engineer.coldcloud.com might be part of the same zone. This can be verified using the dig command:

```bash theme={null}
$ dig kodekloud.com
$ dig engineer.kodekloud.com
```

Both commands would typically return the same set of A records, signifying that they belong to the same zone. To transfer the subdomain engineer.kodekloud.com into a new zone for another company, a further delegation of authority would be required—similar to the process illustrated below.

<Frame>
  ![The image illustrates the anatomy of a domain name, showing the hierarchy from the root zone to the second-level domain, using "engineer.kodekloud.com" as an example. It explains the subdivision and delegation of authority in domain naming.](https://kodekloud.com/kk-media/image/upload/v1752873277/notes-assets/images/Demystifying-DNS-Domain-Name-Anatomy/domain-name-anatomy-hierarchy.jpg)
</Frame>

<Callout icon="lightbulb">
  We will explore the technical details behind the delegation of authority in a subsequent section. For now, think of it simply as transferring a subdomain into a new administrative zone.
</Callout>

## Comparing DNS Records

To further illustrate how delegation affects DNS zones, let’s compare the DNS records for linuxfoundation.org and its subdomain training.linuxfoundation.org using the dig command.

```bash theme={null}
$ dig linuxfoundation.org
; <<>> DiG 9.18.28-0ubuntu0.24.04.1-Ubuntu <<>> linuxfoundation.org
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 45172
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;linuxfoundation.org.            IN      A

;; ANSWER SECTION:
linuxfoundation.org.       600     IN      A       3.131.150.69

;; Query time: 99 msec
;; SERVER: 10.255.255.254#53(10.255.255.254) (UDP)
;; WHEN: Tue Nov 05 23:43:06 CST 2024
;; MSG SIZE  rcvd: 64
```

```bash theme={null}
$ dig training.linuxfoundation.org
; <<>> DiG 9.18.28-0ubuntu0.24.04.1-Ubuntu <<>> training.linuxfoundation.org
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 58716
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;training.linuxfoundation.org.    IN      A

;; ANSWER SECTION:
training.linuxfoundation.org.  600     IN      A       23.185.0.1

;; Query time: 129 msec
;; SERVER: 10.255.255.254#53(10.255.255.254) (UDP)
;; WHEN: Tue Nov 05 23:42:09 CST 2024
;; MSG SIZE  rcvd: 73
```

These examples demonstrate that even if DNS queries return different A records, they might still belong to the same zone. Later, a demonstration will provide insights on how to accurately determine whether nested subdomains are part of the same zone.

This detailed explanation of domain name anatomy and DNS delegation aims to simplify complex networking concepts by using familiar analogies. For further reading on DNS and domain registration processes, consider visiting [Kubernetes Documentation](https://kubernetes.io/docs/) or exploring more specialized articles on domain management.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/demystifying-dns/module/a983cc32-7f91-4feb-8946-eeb1cea67970/lesson/0fc410b3-dbd9-4546-821d-62c0af946834" />
</CardGroup>
