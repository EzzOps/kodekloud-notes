# WAF

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Services-Security/WAF/page

AWS Web Application Firewall (WAF) protects web applications from common attacks and advanced threats by inspecting HTTP requests and applying custom-defined rules.

AWS Web Application Firewall (WAF) is a robust security tool designed to protect your web applications from a variety of common attacks such as SQL injection, cross-site scripting, and other advanced threats at the application layer (Layer 7).

When your web application is positioned behind resources like an Elastic Load Balancer or an API Gateway, AWS WAF acts as the first line of defense. It inspects incoming HTTP requests and determines, based on custom-defined rules, whether to allow, block, or count each request. Because AWS WAF operates at Layer 7, it can interpret the HTTP protocol and allow more sophisticated actions like issuing CAPTCHA challenges or redirecting users.

<Frame>
  ![The image illustrates the concept of a Web Application Firewall (WAF), showing how it monitors HTTP requests from clients (legitimate users or hackers) before they reach web applications.](https://kodekloud.com/kk-media/image/upload/v1752865931/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-WAF/web-application-firewall-http-monitoring.jpg)
</Frame>

## How AWS WAF Works

AWS WAF uses a series of rules organized within what is called a Web Access Control List (Web ACL). A Web ACL is essentially a collection of rules that evaluate incoming requests based on various conditions. These conditions can include properties like:

* IP addresses
* HTTP headers
* Request bodies
* URI strings
* Packet sizes
* Specific geographic locations
* Rate-based conditions to mitigate DDoS attacks

<Frame>
  ![The image is a diagram illustrating a WebACL setup, showing the flow from a firewall icon through various rules and conditions, to a set of network-related icons.](https://kodekloud.com/kk-media/image/upload/v1752865932/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-WAF/webacl-setup-diagram-firewall-rules.jpg)
</Frame>

<Callout icon="lightbulb">
  AWS WAF processes each web request as follows:

  1. The request is made to a resource (e.g., a CloudFront distribution or an Elastic Load Balancer).
  2. AWS WAF inspects the request and evaluates it against the defined rules in the Web ACL in order of priority.
  3. If a request matches a rule, AWS WAF takes the specified action—allow, block, or count the request.
  4. If no rule is matched, the default action specified in the Web ACL is applied, typically allowing the request to reach the protected resource.
</Callout>

This consistent process applies whether AWS WAF is protecting an EC2 instance behind an Application Load Balancer, an API Gateway, or even Lambda functions.

## Key Use Cases for AWS WAF

AWS WAF seamlessly integrates with other AWS services—such as Firewall Manager and CloudWatch—providing a comprehensive security and compliance management strategy. It is particularly useful for:

* **Protecting Against Common Web Attacks:** Safeguard your web applications from SQL injection, cross-site scripting, and cross-site request forgery.
* **API Security:** Secure internet-facing APIs from unauthorized access and potential data exfiltration risks.
* **Enforcing Access Rules:** Implement authentication and authorization rules to ensure that only legitimate users and applications gain access.
* **Securing Serverless Applications:** Integrate easily with API Gateway to protect serverless applications.
* **Layer 7 Traffic Filtering:** Filter HTTP traffic based on methods, headers, URI strings, and body content.

<Frame>
  ![The image lists five use cases for a Web Application Firewall (WAF): protection against common web attacks, API security, protection for serverless applications, application layer firewall, and integration with other AWS services.](https://kodekloud.com/kk-media/image/upload/v1752865934/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-WAF/waf-use-cases-web-security.jpg)
</Frame>

<Callout icon="triangle-alert">
  Always review and update your Web ACL rules regularly to ensure they encompass the latest security threats and vulnerabilities. Regular monitoring and adjustments can help maintain the integrity of your application's defenses.
</Callout>

By leveraging AWS WAF's advanced capabilities, organizations can not only defend against sophisticated web threats but also maintain a seamless user experience through intelligent, rule-based traffic handling.

For more detailed information on AWS WAF and its integration with other services, consider browsing the [AWS Documentation](https://aws.amazon.com/waf/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/6b2d9e18-1714-499c-83d4-4d1f7ff29e66/lesson/161c2997-8661-4247-a66a-b2b9cf63a6b6" />
</CardGroup>
