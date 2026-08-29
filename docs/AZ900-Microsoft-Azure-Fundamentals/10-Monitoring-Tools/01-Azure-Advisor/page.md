# Azure Advisor

Source: https://notes.kodekloud.com/docs/AZ900-Microsoft-Azure-Fundamentals/Monitoring-Tools/Azure-Advisor/page

Azure Advisor helps optimize Azure resources with personalized recommendations across high availability, security, performance, cost optimization, and operational excellence.

Azure Advisor is a powerful tool designed to help the Vela Innovation IT team follow best practices when deploying Azure resources. Instead of providing generic recommendations from Microsoft documentation, Azure Advisor offers personalized insights tailored to your deployed environment, effectively acting as your personalized cloud consultant within the Azure ecosystem.

Azure Advisor analyzes your resource configurations and usage patterns, providing recommendations across five key areas as part of Microsoft's well-architected framework: high availability, security, performance, cost optimization, and operational excellence.

<Frame>
  ![The image shows five circular icons representing different aspects of Azure Advisor: High Availability, Security, Performance, Cost, and Operational Excellence. Each icon has a unique color and symbol related to its category.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868456/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Advisor/azure-advisor-icons-high-availability-security-performance-cost-operational-excellence.jpg)
</Frame>

These recommendations align with best practices, ensuring your Azure resources are optimized, secure, and cost-effective.

## Key Features of Azure Advisor

### Personalized Recommendations

Azure Advisor delivers customized guidance based on your specific usage patterns and resource configurations. It provides actionable insights along with direct links to implement recommended changes, enabling you to rapidly enhance your cloud environment.

### Integrated Experience

Accessible directly from the Azure Portal, Azure Advisor integrates seamlessly into your existing workflow and is available at no additional cost.

<Frame>
  ![The image outlines the key features of Azure Advisor, highlighting personalized recommendations, actionable guidance, and an integrated experience.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868457/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Advisor/azure-advisor-key-features-outline.jpg)
</Frame>

<Callout icon="lightbulb">
  Azure Advisor leverages Microsoft's well-architected framework, ensuring that every recommendation aligns with industry standards for high availability, security, performance, cost, and operational excellence.
</Callout>

## Benefits of Using Azure Advisor

1. **Cost Optimization:**\
   Identify underutilized resources and receive actionable suggestions to reduce costs without compromising functionality.

2. **Performance Improvement:**\
   Enhance the efficiency and responsiveness of your applications with recommendations aimed at boosting overall performance.

3. **Enhanced Security:**\
   Receive guidance to strengthen the security posture of your resources and protect against potential vulnerabilities. Security recommendations are integrated from [Microsoft Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/).

4. **High Availability:**\
   Ensure the continuity of critical business applications with recommendations designed to minimize downtime and service interruptions.

## Use Cases and Live Demonstration

Azure Advisor is ideal for continuously assessing your Azure environment. Whether you are refining deployments or implementing industry best practices, it offers a clear path to achieving operational excellence.

To explore Azure Advisor, simply search for "Advisor" in the Azure Portal's top search bar. Once opened, the tool displays scores for each recommendation category. Please note that in a demo subscription, certain recommendations—such as those related to cost optimization, operational excellence, or performance—might not appear. For instance, the reliability section may show only a few suggestions.

<Frame>
  ![The image shows the Microsoft Azure Advisor Overview dashboard, displaying scores and recommendations for cost, security, reliability, operational excellence, and performance. It includes sections for tips and getting started with Advisor.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868459/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Advisor/azure-advisor-overview-dashboard.jpg)
</Frame>

Click on any recommendation to access detailed information, including the impact, description, potential benefits, and the latest update timestamp.

<Frame>
  ![The image shows the Microsoft Azure Advisor dashboard, specifically the "Reliability" section, displaying recommendations for improving system reliability with details on impact, potential benefits, and impacted resources.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868460/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Advisor/azure-advisor-reliability-dashboard.jpg)
</Frame>

For security, recommendations stem from [Microsoft Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/), ensuring you receive comprehensive and up-to-date guidance.

<Frame>
  ![The image shows a Microsoft Azure Advisor Security dashboard with recommendations for improving security, including one medium and one low impact issue affecting virtual machines.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868462/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Advisor/azure-advisor-security-dashboard-recommendations.jpg)
</Frame>

<Callout icon="triangle-alert">
  In demo subscriptions, not all recommendation categories may be fully represented. Ensure you test Azure Advisor in a production-like environment to see the complete set of recommendations.
</Callout>

This concludes our overview of Azure Advisor. Leverage these insights to optimize your cloud resources, enhance security, improve performance, and manage costs effectively.

For more details on Azure best practices and resource optimization, explore the [Azure Documentation](https://docs.microsoft.com/en-us/azure/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az900-microsoft-azure-fundamentals/module/fe17e76e-2be4-4e04-bbfe-a7e8f72b1f6f/lesson/72e2dddf-258b-47c7-80cc-039858d8045f" />
</CardGroup>
