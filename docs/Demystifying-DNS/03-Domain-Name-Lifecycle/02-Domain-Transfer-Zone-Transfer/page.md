# Domain Transfer Zone Transfer

Source: https://notes.kodekloud.com/docs/Demystifying-DNS/Domain-Name-Lifecycle/Domain-Transfer-Zone-Transfer/page

This article explains domain transfers, including changing registrars, transferring ownership, and defending against domain hijacking.

In a previous lecture, we explained that a Zone Transfer is the process by which nameservers synchronize data. In DNS, the leader-follower architecture means that the primary nameserver receives updated records in a hosted zone file and secondary nameservers replicate this data using various mechanisms.

<Frame>
  ![The image illustrates a "Leader Follower" concept with a sequence of nameservers and documents connected in a linear flow.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873231/notes-assets/images/Demystifying-DNS-Domain-Transfer-Zone-Transfer/leader-follower-nameservers-diagram.jpg)
</Frame>

In this article, we focus on domain transfers. A domain transfer can refer to:

* Changing the registrar that manages your domain
* Transferring the domain ownership (registrant)
* Or, performing both actions simultaneously

For instance, consider KodeKloud.com, which is managed using Cloudflare nameservers. If Mumshad Mannambeth decides to retain ownership but move KodeKloud.com from Cloudflare to AWS Route 53, this is considered a registrar transfer. Conversely, if the ownership of the domain is being transferred to someone else, it would be described as a registrant transfer.

<Frame>
  ![The image explains "Domain Transfer" with two points: changing registrars and giving a domain to someone else.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873232/notes-assets/images/Demystifying-DNS-Domain-Transfer-Zone-Transfer/domain-transfer-registrars-giving.jpg)
</Frame>

It is also possible to transfer both ownership and registrar simultaneously. However, be aware that domain transfers can sometimes occur through malicious activities. Domain hijacking is a type of DNS attack where an attacker attempts to take control of your domain by impersonating you—for example, by sending fake emails on your behalf.

<Frame>
  ![The image illustrates a "Domain Transfer: DNS Attack" with icons representing email and a hacker, connected by a line labeled "Domain hijacking: DNS attack."](../../../../images/kodekloud.com/kk-media/image/upload/v1752873233/notes-assets/images/Demystifying-DNS-Domain-Transfer-Zone-Transfer/domain-transfer-dns-attack-diagram.jpg)
</Frame>

<Callout icon="triangle-alert">
  Domain hijacking is particularly dangerous because ICANN considers email an acceptable method for assessing the legitimacy of a domain transfer.
</Callout>

To defend against domain hijacking, consider implementing these measures:

* Always keep your domain locked. Domain locking is a feature provided by most registrars (often enabled by default) that prevents unauthorized transfers.
* Keep your SOA (Start of Authority) records updated.
* Enable auto-renewal on your domain to prevent accidental expiration.
* Use strong authentication methods wherever possible.

<Frame>
  ![The image provides four tips to defend against domain hijacking: keep your domain locked, update SOA records, enable auto-renewal, and use strong authentication methods.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873234/notes-assets/images/Demystifying-DNS-Domain-Transfer-Zone-Transfer/domain-hijacking-defense-tips.jpg)
</Frame>

<Callout icon="lightbulb">
  Legitimate domain transfers are a standard part of domain management. However, if you suspect that your domain has been transferred without authorization, you can file a dispute with [ICANN](https://www.icann.org/) to investigate the issue and potentially reverse the transfer.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/demystifying-dns/module/fada8728-c242-452d-a6e1-7dc8aa2511f3/lesson/bb4d0881-ccc6-40f6-9cfc-012a3155d288" />
</CardGroup>
