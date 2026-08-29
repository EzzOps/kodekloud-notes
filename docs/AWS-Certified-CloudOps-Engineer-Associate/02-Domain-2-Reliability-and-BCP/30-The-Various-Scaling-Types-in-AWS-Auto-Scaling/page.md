# The Various Scaling Types in AWS Auto Scaling

Source: https://notes.kodekloud.com/docs/AWS-Certified-CloudOps-Engineer-Associate/Domain-2-Reliability-and-BCP/The-Various-Scaling-Types-in-AWS-Auto-Scaling/page

This article explores the three main scaling methods in AWS EC2 Auto Scaling dynamic scaling, scheduled scaling, and predictive scaling.

Welcome back. In this article, we explore the three main scaling methods used in AWS EC2 Auto Scaling: dynamic scaling, scheduled scaling, and predictive scaling. Auto Scaling leverages three core components:

* **Launch Templates:** Define the configuration for launching new EC2 instances.
* **Auto Scaling Groups (ASGs):** Set parameters such as minimum, maximum, and desired instance counts.
* **Scaling Policies:** Specify when and how to modify the number of instances.

This guide focuses on scaling policies, which include dynamic scaling (with multiple modes), scheduled scaling, and predictive scaling.

<Frame>
  <img alt="The image is a diagram showing types of AWS Auto Scaling, including Dynamic Scaling, Predictive Scaling, and Scheduled Scaling. Dynamic Scaling is further divided into Target Tracking Scaling, Step Scaling, and Simple Scaling." />
</Frame>

## Dynamic Scaling

Dynamic scaling adjusts the number of instances based on real-time metrics. It is available in three modes:

1. **Target Tracking Scaling:**\
   Specify a target metric value (e.g., maintaining average CPU utilization at 80%). The scaling policy automatically adds or removes instances to keep the metric close to your target.

2. **Step Scaling:**\
   Define multiple thresholds along with distinct scaling actions. For instance, if CPU utilization ranges between 70% and 80%, the policy might add one instance; if it rises from 80% to 90%, it might add two instances. This approach provides a graduated response to varying loads.

3. **Simple Scaling:**\
   This method triggers a fixed scaling action when a single metric surpasses a preset threshold (such as CPU utilization rising above 80%). Though effective, it is considered a legacy method compared to the other dynamic options.

### Example: Dynamic Scaling Modes in Action

Imagine you set a target tracking policy to maintain CPU utilization at 50%. Whether the usage is marginally above or below 50%, the scaling mechanism makes periodic adjustments to align with the target.

<Frame>
  <img alt="The image illustrates a concept of target tracking scaling with five microchip icons, showing varying levels of usage, and a central icon indicating scaling adjustments." />
</Frame>

In step scaling, you might configure thresholds such as:

* Below 70%: No scaling action.
* Between 70% and 85%: Increase capacity by adding a specific number of instances.
* Above 85%: Add even more instances to handle the elevated load quickly.

<Frame>
  <img alt="The image illustrates a dynamic scaling policy for auto-scaling, showing three types of scaling: target tracking, step scaling, and simple scaling, with metrics like CPU utilization and network bytes." />
</Frame>

Simple scaling, by contrast, relies solely on set thresholds for scaling up or down, lacking the nuanced responses that step scaling provides.

<Frame>
  <img alt="The image illustrates a step scaling process for EC2 CPU utilization, showing a series of CPU icons and a bar graph indicating different utilization levels." />
</Frame>

## Scheduled Scaling

Scheduled scaling is based on predetermined time intervals rather than real-time metrics. This approach works best when your application's workload follows predictable patterns. For example, if a website experiences peak traffic from 8 AM to 10 AM, you can schedule an increase in instance capacity just before 8 AM and a decrease after 10 AM.

<Frame>
  <img alt="The image illustrates how scheduled auto-scaling works for a website, showing different scaling configurations for specific time periods." />
</Frame>

<Callout icon="lightbulb">
  Scheduled scaling is ideal for workloads with known traffic patterns but might be less effective if the traffic pattern deviates from the expected schedule.
</Callout>

## Predictive Scaling

Predictive scaling, sometimes referred to as historical scaling, uses historical data and machine learning models to forecast demand. This method is particularly valuable for applications with cyclical or seasonal traffic trends. The system analyzes past data to predict future resource needs and scales accordingly.

<Frame>
  <img alt="The image illustrates a process of predictive scaling using a machine learning model, involving steps like loading metrics, performing regression analysis, scheduling scaling actions, and repeating daily." />
</Frame>

<Callout icon="triangle-alert">
  Predictive scaling requires sufficient historical data. Without enough past metrics, the accuracy of predictions may be compromised, making it less suitable for new applications.
</Callout>

## Conclusion

AWS Auto Scaling provides three distinct approaches to handling varying workloads:

* **Dynamic Scaling:** Easily adapts in real time with options such as target tracking, step scaling, and simple scaling.
* **Scheduled Scaling:** Adjusts instance counts based on predetermined schedules, perfect for predictable traffic patterns.
* **Predictive Scaling:** Uses historical data to forecast and react to future demands dynamically.

Each scaling strategy can be tailored to meet the unique needs of your application depending on its traffic trends and operational requirements. We hope this detailed guide enhances your understanding of AWS Auto Scaling methods.

See you in the next article!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-sysops-administrator-associate/module/1b592900-bdef-468a-9a2b-de667b7e9cae/lesson/1c773ba9-aa8f-4361-a53c-ef1e4342bc26" />
</CardGroup>
