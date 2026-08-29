# Domain Registration Process

Source: https://notes.kodekloud.com/docs/Demystifying-DNS/Domain-Name-Lifecycle/Domain-Registration-Process/page

This article explains the domain registration process, detailing the roles of registrars, registrants, and registries in securing unique domain names.

In this lesson, we dive deep into the domain registration process by using an analogy involving three key actors: the registrar, the registrant, and the registry. This in-depth explanation builds on previous discussions about domain registration and DNS functionality to help you understand the underlying mechanisms that keep the digital world connected.

## Key Actors in Domain Registration

* **Registrar**: Think of the registrar as an Internet real estate agent. Companies like GoDaddy, Namecheap, and Google Domains offer domain registration services and facilitate the interaction between the registrant and the registry.
* **Registrant**: This is the individual or organization looking to secure a unique domain name—the digital equivalent of owning real estate.
* **Registry**: Registries maintain authoritative records for specific top-level domains (TLDs). For instance, VeriSign manages millions of transactions daily for the .com TLD, while the Public Interest Registry oversees .org domains.

Imagine a registrant growing tired of generic subdomains provided by platforms like WordPress.com, Medium.com, or GitHub.io. The desire for an independent identity on the Internet sparks a quest for a personal and unique domain name. This exploration leads to the discovery of registrars (the real estate agents) and the roaming power of registries (the custodians of the TLD territories).

## Understanding TLD Territories

For example, VeriSign is responsible for managing .com domains, ensuring that each registration is correctly recorded. Meanwhile, the .org TLD is managed by the Public Interest Registry, dedicated to serving non-profits and organizations.

<Frame>
  ![The image illustrates the domain registration process, featuring a registrant and a browser window highlighting Verisign's role in controlling the .com domain territory, processing transactions, maintaining information, and enforcing strict control.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873219/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-verisign-process.jpg)
</Frame>

Similarly, within the .io territory, the Internet Computer Bureau has emerged as a prominent registry. This TLD has become popular with tech startups seeking modern and trendy digital addresses.

<Frame>
  ![The image illustrates the domain registration process, showing a registrant and a browser window with the Internet Computer Bureau logo, indicating it runs the .io territory.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873220/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-process-io-logo.jpg)
</Frame>

## Domain Drop Catching

During his exploration, the registrant also learns about an underground facet of the industry called domain drop catching. Some registrars specialize in capturing domains the moment they expire. Automated systems deployed by companies such as [DropCatch.com](https://www.dropcatch.com) and [SnapNames](https://www.snapnames.com) monitor for domain expirations and register valuable domains as soon as they become available.

<Frame>
  ![The image illustrates the domain registration process, highlighting services like DropCatch and SnapNames that use automation to catch expiring domains.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873222/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-process-automation.jpg)
</Frame>

## Expiration and Renewal Protocols

To prevent mass chaos from expired domains, registries have established a redemption system:

* **30-Day Grace Period** for regular renewal
* **30-Day Redemption Period** with higher fees
* **5-Day Waiting Period** before a domain becomes generally available

<Callout icon="lightbulb">
  These periods ensure that domain owners have sufficient time to renew their domains while also providing a controlled process for third parties interested in expired domains.
</Callout>

<Frame>
  ![The image illustrates the domain registration process, highlighting a 30-day grace period for normal renewal and a 30-day redemption period where renewal is possible but expensive.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873223/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-grace-redemption.jpg)
</Frame>

## Pricing Insights

Traditional registrars like GoDaddy and Namecheap act similarly to real estate agencies by providing registration services. They work with registries that interact only with authorized registrars. During the process, the registrant discovers that pricing varies between registrars. Each registry charges its own protection fee. For example:

* **.com domains**: VeriSign charged between $8 to $20 yearly.
* **.io domains**: Typically around \$60 yearly.

Registrars then add their markup to these base fees, influencing the final retail price.

<Frame>
  ![The image illustrates the domain registration process, highlighting that registries charge registrars varying protection fees by territory, with Verisign charging more for .com domains and the Internet Computer Bureau raising prices.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873225/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-process-fees-illustration.jpg)
</Frame>

## A Practical Domain Registration Scenario

Eager to secure a domain, the registrant initially attempts to register bestcode.com. However, after consulting with a reputable registrar, he learns that the domain is already taken. He then checks bestcode.io and finds it available—with a caveat that trendy TLDs like .io are snapped up quickly.

<Frame>
  ![The image illustrates the domain registration process, showing a registrant and a registrar with a domain name "bestcode.io" linked to the registrar. A note states that only authorized registrars can communicate directly.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873226/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-process-bestcode.jpg)
</Frame>

## The EPP Protocol in Action

At this stage, the registrar communicates with the registry (Internet Computer Bureau) using the Extensible Provisioning Protocol (EPP). The dialogue unfolds as follows:

```text theme={null}
Registrar: I have a potential registrant interested in your territory.
Registry: Confirming a customer is interested in establishing within our namespace.
Registrar: They wish to register bestcode.io. All necessary information and payment have been collected.
Registry: Checking records... bestcode.io is available. As you are an authorized registrar, please proceed by sending over the technical details.
```

<Frame>
  ![The image illustrates the domain registration process, showing the interaction between a registrar and a registry using the EPP protocol to check and create domains, with responses given through specific status codes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873227/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-epp-protocol-diagram.jpg)
</Frame>

Once verified, the registry adds bestcode.io to the .io zone file along with its designated name servers. It is important to note that while the registry updates the zone file, it does not alter the root servers. The root servers continue to delegate all .io domains to the registry's name servers.

## Configuring Name Servers

Next, the registrar collaborates with the registrant to configure the name servers. Think of name servers as building permits—they determine where your domain’s services are hosted. The registrant is given the option to use the registrar’s default name servers or provide custom names, such as those offered by their preferred hosting company.

In this example, the registrant opts for popular hosting company name servers, such as "ns1.hostcompany.com" and "ns2.hostcompany.com." After entering these details, the registrar notifies the registry accordingly.

<Frame>
  ![The image illustrates a domain registration process, showing a registrant and a web interface where nameserver details are entered and submitted.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873228/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-nameserver-process.jpg)
</Frame>

The registry’s zone file is then updated with these name server details. When a user enters bestcode.io in their browser, the updated zone file directs the DNS system to the authoritative name servers hosting the site.

<Frame>
  ![The image illustrates the domain registration process, showing how the "zone file" at the registry level updates a directory that informs the internet about authoritative nameservers for each domain.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873229/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-zone-file-diagram.jpg)
</Frame>

## Finalizing the Registration

With the successful update of the zone file and the delegation of name servers, the registrant now owns a fully operational domain. Although the registrar handles the formal registration process and associated paperwork, the registrant retains complete freedom to decide where and how to use the domain. This separation between domain registration and hosting is fundamental—it means you can register your domain with one provider (e.g., GoDaddy) while hosting your website with another service (e.g., AWS or Cloudflare).

<Frame>
  ![The image illustrates the domain registration process, showing the separation between domain registration (with GoDaddy) and domain hosting (with AWS and Cloudflare). It emphasizes that this separation is a key principle of the internet.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873230/notes-assets/images/Demystifying-DNS-Domain-Registration-Process/domain-registration-process-godaddy-aws-cloudflare.jpg)
</Frame>

Finally, once the name server details are entered and confirmed, the registry updates its master database—the ultimate source of truth for domains under its TLD. With the process complete, the registrant stands proudly with bestcode.io, ready to embark on a new digital journey.

<Callout icon="lightbulb">
  Remember: The separation between domain registration and hosting allows for flexibility in managing your online presence. You can register your domain with one provider and host your website with another, giving you the freedom to choose the best services for your needs.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/demystifying-dns/module/fada8728-c242-452d-a6e1-7dc8aa2511f3/lesson/9d66fbef-7f58-4a0f-bfaa-53fe6c9f8bf0" />
</CardGroup>
