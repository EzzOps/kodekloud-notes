# Example CloudFormation snippet
Resources:
  MyFISExperiment:
    Type: AWS::FIS::ExperimentTemplate
    Properties:
      Description: "Terminate EC2 instance for resilience testing"
      Actions:
        - ActionId: aws:ec2:terminate-instances
          Parameters:
            instanceIds: ["i-0123456789abcdef0"]
      Targets:
        - ResourceType: "aws:ec2:instance"
          ResourceTags:
            chaos-test: "true"
      RoleArn: arn:aws:iam::123456789012:role/FISRole
      StopConditions:
        - Source: "aws:cloudwatch:alarm"
          Value: arn:aws:cloudwatch:us-west-2:123456789012:alarm:HighCPUUtilization
```

<Callout icon="triangle-alert">
  Always run experiments in a staging or non-production environment first. Fault injection can cause service interruptions!
</Callout>

## Security & Permissions

Leverage **AWS Identity and Access Management (IAM)** to grant granular permissions:

* `fis:CreateExperimentTemplate`
* `fis:StartExperiment`
* `fis:StopExperiment`
* `cloudwatch:DescribeAlarms`
* `ec2:TerminateInstances`

Use IAM policies and roles to restrict who can create, modify, or execute FIS experiments.

***

## Links and References

* [AWS Fault Injection Simulator Documentation](https://docs.aws.amazon.com/fis/)
* [Chaos Engineering Concepts](https://chaosengineering.org/)
* [Amazon CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
* [AWS X-Ray Overview](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/chaos-engineering/module/b45a00dd-3232-4d00-81b8-60e98b8e3f77/lesson/8991c8a2-8f46-46a3-be8c-e85aa23a44eb" />
</CardGroup>


# What is Chaos Engineering

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Chaos-Engineering-Fundamentals/What-is-Chaos-Engineering/page

Chaos engineering involves running controlled experiments to understand system behavior under failure conditions, uncovering weaknesses and improving resilience through intentional fault injection.

Chaos engineering is the discipline of running controlled experiments to understand how systems behave under failure conditions. By intentionally injecting faults, teams can uncover hidden weaknesses and improve resilience. This lesson walks through the five fundamental steps of chaos engineering, illustrated with diagrams and real-world examples.

## The Five Key Steps

1. **Collect Metrics**\
   Establish baseline measurements that represent your system’s normal (steady state) behavior.

<Frame>
  ![The image features a presentation slide titled "Chaos Engineering Experiments" with a focus on "Collect Metrics" and a person speaking on the right side.](https://kodekloud.com/kk-media/image/upload/v1752871800/notes-assets/images/Chaos-Engineering-What-is-Chaos-Engineering/chaos-engineering-experiments-collect-metrics.jpg)
</Frame>

2. **Form a Hypothesis**\
   Predict how the system will react when a specific fault is introduced, based on your steady state.

3. **Design the Experiment**\
   Define the smallest, most targeted test that can validate or refute your hypothesis.

4. **Inject Failure**\
   Execute the experiment by introducing the planned disruption.

<Callout icon="triangle-alert">
  Always run chaos experiments in a safe, isolated environment and ensure you have monitoring and rollback plans in place.
</Callout>

5. **Measure Impact**\
   Compare post-failure metrics against your baseline to determine whether the hypothesis holds. Use findings to enhance system robustness.

***

## Analogy: States of Water

To make these concepts concrete, consider how water changes state with temperature:

* **Given**: Water exists as vapor, liquid, or solid depending on temperature.
* **Hypothesis**: Placing liquid water in a freezer for 10 minutes will cause it to freeze.

<Frame>
  ![The image shows a presentation slide about a hypothesis/experiment on the states of water, with a diagram of a container and a glass, and a person speaking.](https://kodekloud.com/kk-media/image/upload/v1752871802/notes-assets/images/Chaos-Engineering-What-is-Chaos-Engineering/water-states-hypothesis-presentation-slide.jpg)
</Frame>

**Experiment**: We put a container of water in the freezer for 10 minutes.

<Frame>
  ![The image shows a hypothesis about water turning into ice if placed in a freezer for 10 minutes, alongside a person speaking.](https://kodekloud.com/kk-media/image/upload/v1752871803/notes-assets/images/Chaos-Engineering-What-is-Chaos-Engineering/water-ice-hypothesis-freezer-person.jpg)
</Frame>

**Result**: After 10 minutes, the water remains liquid because the freezer’s temperature was higher than expected.

<Frame>
  ![The image shows a slide about a hypothesis/experiment, noting that water didn't freeze in 10 minutes due to an unaccounted freezer temperature setting, alongside a person in a headscarf.](https://kodekloud.com/kk-media/image/upload/v1752871805/notes-assets/images/Chaos-Engineering-What-is-Chaos-Engineering/hypothesis-experiment-water-freezing-slide.jpg)
</Frame>

**Refinement**: We lower the freezer temperature and repeat the test. The water freezes within 10 minutes, validating our updated hypothesis.

<Frame>
  ![The image shows a woman in a headscarf next to a diagram of a freezer with a suggestion to change the freezer temperature setting as part of a hypothesis or experiment.](https://kodekloud.com/kk-media/image/upload/v1752871805/notes-assets/images/Chaos-Engineering-What-is-Chaos-Engineering/woman-headscarf-freezer-diagram-hypothesis.jpg)
</Frame>

<Callout icon="lightbulb">
  Refining your experiment parameters is key to isolating root causes and achieving reliable results.
</Callout>

***

## Technical Example: Auto Scaling Group

Next, let’s apply the five steps to a cloud infrastructure scenario:

* **Given**: An application runs on a single EC2 instance within an Auto Scaling group (ASG), which maintains a minimum of one instance.
* **Hypothesis**: Terminating the instance won’t affect availability because the ASG will launch a replacement immediately.

<Frame>
  ![The image shows a hypothesis about an application not being impacted due to an Auto Scaling Group ensuring instance availability, alongside a diagram illustrating the process. There is also a person speaking, possibly explaining the concept.](https://kodekloud.com/kk-media/image/upload/v1752871807/notes-assets/images/Chaos-Engineering-What-is-Chaos-Engineering/auto-scaling-group-hypothesis-diagram.jpg)
</Frame>

**Inject Failure**: We terminate the running instance.\
**Observation**: The ASG replaces the instance, but boot time takes 15 minutes—resulting in unexpected downtime.

<Frame>
  ![The image shows a presentation slide about a hypothesis/experiment related to server boot time, with a person speaking on the right.](https://kodekloud.com/kk-media/image/upload/v1752871808/notes-assets/images/Chaos-Engineering-What-is-Chaos-Engineering/server-boot-time-hypothesis-presentation.jpg)
</Frame>

**Refinement**: Increase the ASG’s desired capacity to two instances so one remains available during boot.

<Frame>
  ![The image shows a presentation slide about a hypothesis/experiment on improving auto-scaling groups by increasing instances to ensure availability. It includes a diagram of instances and a person speaking on the right.](https://kodekloud.com/kk-media/image/upload/v1752871809/notes-assets/images/Chaos-Engineering-What-is-Chaos-Engineering/auto-scaling-hypothesis-experiment-slide.jpg)
</Frame>

Rerunning the experiment confirms zero downtime, validating our updated hypothesis and architecture.

***

## Next Steps

You’ve now seen how chaos engineering uncovers hidden weaknesses and drives iterative improvements. In the upcoming sections, we will explore how to implement these experiments using [AWS Fault Injection Simulator (FIS)](https://docs.aws.amazon.com/fis/latest/userguide/what-is-fis.html) to automate fault injection and monitoring in your cloud environment.

***

## References

* [Chaos Engineering on AWS](https://aws.amazon.com/fis/)
* [AWS Fault Injection Simulator User Guide](https://docs.aws.amazon.com/fis/latest/userguide/)
* [Principles of Chaos Engineering](https://principlesofchaos.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/chaos-engineering/module/b45a00dd-3232-4d00-81b8-60e98b8e3f77/lesson/1d4b1676-75bf-4afb-a022-05f8f2d355ef" />
</CardGroup>
