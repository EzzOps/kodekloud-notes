# Web Application Firewall Default Rules

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Implement-a-Web-Application-Firewall/Web-Application-Firewall-Default-Rules/page

Explains Azure Web Application Firewall default rule set, managed rule groups, and demo showing Front Door WAF blocking XSS attacks and tuning options

Azure Web Application Firewall (WAF) — Default Rule Set (DRS), rule groups, and rules.

Azure WAF includes a Microsoft-managed Default Rule Set (DRS) that’s built on the OWASP Core Rule Set and updated regularly. The DRS provides immediate, out-of-the-box protection for common web attacks so you don’t need to manually create protections for every threat pattern.

Key protections in the Default Rule Set include:

| Attack class                          | What it protects against                                           |
| ------------------------------------- | ------------------------------------------------------------------ |
| Cross‑Site Scripting (XSS)            | Reflective and stored XSS where user input is returned unsanitized |
| SQL Injection                         | Malicious SQL fragments injected into parameters                   |
| PHP injection                         | PHP code injection attempts                                        |
| Java-related attacks                  | Java-specific request payload exploits                             |
| Remote Command Execution (RCE)        | Payloads attempting to execute system commands                     |
| Local/Remote File Inclusion (LFI/RFI) | Attempts to include files from local or remote sources             |
| Session fixation                      | Attacks targeting session identifiers                              |
| Protocol attacks                      | HTTP request smuggling, response splitting, and similar anomalies  |

Each rule in the DRS matches a specific signature or pattern. When a request matches a rule, the WAF applies the configured action (for example, `Block` or `Log`). Administrators can enable/disable individual rules or entire rule groups to tune protection to application requirements.

<Frame>
  <img alt="The image displays a list of Web Application Firewall default rule sets with descriptions, actions, statuses, and rule groups. Various attack types like SQL Injection and HTTP Request Smuggling are set to be blocked on anomaly." />
</Frame>

Rules are organized into groups by attack category (for example: SQL injection, protocol attacks, RCE). This grouping makes it simple to enable or disable whole categories—useful when parts of the application stack (e.g., PHP) are not in use—while keeping baseline protections for other threats.

Think of the Default Rule Set as the first line of defense for most common attack patterns. You may still need custom rules for business-specific scenarios (for example, geofencing or rate limiting), but managed rules significantly reduce exposure with minimal configuration.

In this walkthrough we demonstrate how the managed Default Rule Set blocks a basic Cross‑Site Scripting (XSS) exploit by placing Azure Front Door (AFD) with a WAF policy in front of vulnerable App Service web apps.

I created two intentionally vulnerable App Service web apps that reflect user input back into the page without proper sanitization. Both instances exhibit a simple XSS vulnerability.

<Frame>
  <img alt="The image shows the Azure portal's App Services page, listing two running web apps with their locations, pricing tiers, and app service plans." />
</Frame>

Because of the vulnerability, injecting one of these payloads into a comment/name field triggers script execution in the browser:

```html theme={null}
<script>alert('XSS Attack!')</script>
<img src=x onerror=alert('XSS')>
```

Submitting such input to the vulnerable app causes the browser to execute the injected script and show an alert dialog.

<Frame>
  <img alt="The image shows a webpage with a pop-up alert from a site indicating &#x22;XSS&#x22; with an &#x22;OK&#x22; button." />
</Frame>

Here are several common XSS payload variants you can use for testing (consolidated):

```html theme={null}
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
<iframe src=javascript:alert('XSS')>
javascript:alert('XSS')
```

I also deployed a second identical web app in another region to simulate a global application behind Front Door; the same payloads work there as well.

<Frame>
  <img alt="The image shows a web application interface used for testing cross-site scripting (XSS) vulnerabilities, with fields for input and examples of common XSS test payloads." />
</Frame>

<Frame>
  <img alt="The image shows a web application interface designed to test XSS vulnerabilities, with fields to input a name and comment and a submit button. It includes a warning about the vulnerability and a list of common XSS test payloads." />
</Frame>

Next, place Azure Front Door in front of both App Services and attach a WAF policy to the Front Door endpoint.

You can deploy the vulnerable apps with an automation script (not shown here) that creates the App Services used in this lesson. After the apps exist, create an AFD profile and add a WAF policy. I used the Front Door Quick Create flow to speed the demo: I selected the Premium tier and set my primary App Service as the origin. During Front Door creation you can either attach an existing WAF policy or create a new standalone policy that can be reused across profiles.

<Frame>
  <img alt="The image depicts the Azure Portal interface for &#x22;Azure Front Door&#x22; with no front doors displayed in the list. There is an option to create a new front door." />
</Frame>

I created a new WAF policy called "WAF01" during Front Door creation.

<Frame>
  <img alt="This image shows a Microsoft Azure interface for creating a Front Door profile, with options for setting the tier and endpoint details, and a popup to create a new WAF policy." />
</Frame>

After the profile was created, I added the secondary App Service to the Front Door origin group so Front Door could route traffic to either instance based on proximity and health.

<Frame>
  <img alt="The image shows a Microsoft Azure portal dashboard for a resource named &#x22;afd-waf,&#x22; which is part of the Azure Front Door service, displaying various settings like resource group, subscription details, and security policies." />
</Frame>

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface where an origin is being added to a Front Door service, with settings such as origin type, host name, and ports specified." />
</Frame>

Updating an origin group can take a short time. After propagation, the secondary app becomes reachable via Front Door.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface for configuring an &#x22;Origin group&#x22; in Front Door, including setting origin host names, session affinity, and health probes." />
</Frame>

Open the standalone WAF policy resource to inspect managed rules, custom rules, diagnostic settings, and associations. A standalone WAF policy can be attached to multiple Front Door profiles, enabling centralized policy management.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying a list of security policies for a Front Door setup, with one policy named &#x22;waf01-a616d833&#x22; that has succeeded." />
</Frame>

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying the configuration details for a Front Door WAF policy named &#x22;waf01,&#x22; with options for policy settings, managed rules, custom rules, and associations." />
</Frame>

From the WAF policy blade you can:

* Toggle between Detection and Prevention modes
* Review and tune managed rules
* Add custom rules evaluated prior to managed rules
* Enable logging/diagnostics (stream to Azure Monitor or Event Hub)
* View and manage associations with Front Door profiles

<Frame>
  <img alt="The image shows a Microsoft Azure portal screen where a user is configuring a WAF (Web Application Firewall) policy and associating it with a Front Door profile. The user interface allows selection of domains for the specified Front Door WAF policy." />
</Frame>

Under Manage rules you can inspect the Default Rule Set provided by Microsoft. The rules are grouped into categories such as Bot detection, PHP, protocol protections, Java, LFI, XSS, SQL injection, and RCE—which makes coverage visible and tunable.

<Frame>
  <img alt="The image shows a Microsoft Azure portal displaying managed rules for a web application firewall (WAF) policy named &#x22;waf01,&#x22; listing various security rules for detecting potential threats." />
</Frame>

In this policy, Cross‑Site Scripting rules are enabled by default as part of the managed rule set. You can create custom rules on top of the managed rules to address business-specific scenarios (rate limiting, geofencing, IP restrictions, etc.). Custom rules are evaluated before managed rules, so use them to allow or block traffic that would otherwise be handled by the DRS.

Now test the Front Door endpoint by opening the Front Door URL in a browser. Note that Front Door will route requests to the nearest healthy origin; if you encounter HTTPS certificate validation errors when Front Door is configured with App Service origins, you can temporarily disable certificate validation for the origin to troubleshoot.

<Frame>
  <img alt="The image displays a webpage for a WAF Demo App focused on testing XSS vulnerabilities, with fields for input and examples of common XSS test payloads." />
</Frame>

By default the WAF policy was created in Detection mode (logging only). For the demo switch the policy to Prevention mode so matching requests are actively blocked. If you want visibility into matched detections, enable diagnostics to stream logs to Azure Monitor or Event Hub.

<Callout icon="lightbulb">
  Detection mode logs matching requests but does not block them. Switch to Prevention mode to actively block malicious requests; enable diagnostics for visibility into matches and blocks.
</Callout>

With the policy in Prevention mode, submit the same XSS payloads via the Front Door endpoint. The requests that trigger managed rules will be blocked and return a 403 Forbidden response. Use browser devtools or a network capture to inspect the request and the WAF response headers.

<Frame>
  <img alt="The image shows a network request log with details of a failed HTTP GET request that resulted in a 403 Forbidden error, along with request and response headers displayed." />
</Frame>

When you inspect the blocked event in the portal or logs, you can see which managed rule matched and triggered the block. In this example the rule detected script blocks and identified the request as an XSS attempt; the WAF prevented the request from reaching the backend.

This demonstrates how Microsoft’s managed Default Rule Set provides immediate protection against common attack patterns like XSS—reducing risk with minimal configuration.

Remember: while managed rules cover most general threats, you may still need custom rules for specific business requirements (for example, only allow traffic from particular countries or block specific IP ranges). Custom rules give you precise control and are evaluated before managed rules.

Creating and tuning custom rules (geofencing, rate limiting, IP restrictions, and exceptions) will be covered in a follow-up article.

References and further reading:

* OWASP Core Rule Set: [https://owasp.org/www-project-modsecurity-core-rule-set/](https://owasp.org/www-project-modsecurity-core-rule-set/)
* Azure Front Door WAF documentation: [https://learn.microsoft.com/azure/frontdoor/](https://learn.microsoft.com/azure/frontdoor/)
* Azure WAF managed rules overview: [https://learn.microsoft.com/azure/web-application-firewall/managed-rule-sets/overview](https://learn.microsoft.com/azure/web-application-firewall/managed-rule-sets/overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/4339a7c9-9465-4ca0-ba30-4ee56ed54bf1/lesson/fbd26e10-538e-48b6-afd7-9e5a9f9c68a9" />
</CardGroup>
