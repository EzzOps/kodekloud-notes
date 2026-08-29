# Cloud VPC Private Service Connect

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Networking/Cloud-VPC-Private-Service-Connect/page

Explains Google Cloud Private Service Connect enabling private internal IP access to Google and third party services, using service attachments, restricted endpoints and static routes to avoid public internet

Welcome back. This lesson explains Private Service Connect (PSC) in Google Cloud VPC with a practical, exam-focused view. Think of PSC as creating a private lane on Google’s network so your workloads talk to services (Google APIs, partner services, or internal APIs) without traversing the public internet.

## At a glance

* Feature: Private Service Connect (PSC)
* Purpose: Private, internal-IP access to Google-managed or third-party services
* Key benefits: Improved security, predictable routing, and often better performance

## Core concepts

### Service perimeter and authorized VPC

* A [service perimeter](https://cloud.google.com/vpc-service-controls) acts as a security boundary around an authorized project. It restricts which services and external networks resources inside the perimeter can access.
* Inside that perimeter you typically run a Compute Engine VM or other workloads in an authorized VPC that need to call Google APIs (for example, [Cloud Storage](https://cloud.google.com/storage) or [BigQuery](https://cloud.google.com/bigquery)) without using public IPs.

### Private connectivity to Google APIs

* Rather than calling public endpoints like `public.googleapis.com`, use the restricted endpoint `restricted.googleapis.com` to keep traffic on Google’s private network.
* A static route — commonly the block `199.36.153.4/30` — directs traffic for the restricted endpoint to the private gateway so it never leaves Google’s backbone.

### How PSC maps to the consumer–producer model

* PSC follows a consumer–producer model:
  * Consumer: your project or VPC that needs to reach a service.
  * Producer: the project (Google, partner, or another team) exposing the service.
* The consumer creates a Private Service Connect endpoint and attaches it to the producer’s service (a service attachment). This exposes the producer’s service as an internal IP in the consumer’s VPC.
* PSC supports cross-project and cross-organization use cases, enabling teams to share internal APIs privately.

## Security and performance benefits

* Traffic stays on Google’s backbone and avoids the public internet, reducing exposure and attack surface.
* You can enforce access controls and keep traffic inside the service perimeter or an organization’s private network topology.
* Often yields lower latency and more predictable performance compared with public internet routing.

## Typical uses and certification focus

* Common scenarios:
  * Securely consuming managed Google services without public IPs.
  * Exposing internal APIs across teams or projects.
  * Migrating on-premises workloads while keeping traffic private.
* For exams, remember this pattern:
  * Authorized VPC / VM → `restricted.googleapis.com` → static route (`199.36.153.4/30`) → private gateway / PSC → service attachment to the producer

## Example: static route for the restricted endpoint

```text theme={null}
