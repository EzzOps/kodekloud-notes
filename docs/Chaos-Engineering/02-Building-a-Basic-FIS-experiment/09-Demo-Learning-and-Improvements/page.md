# Demo Learning and Improvements

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Building-a-Basic-FIS-experiment/Demo-Learning-and-Improvements/page

This article discusses validating application availability using AWS Auto Scaling and Fault Injection Service by terminating an EC2 instance.

In this lesson, we validate our Fault Injection Service (FIS) experiment and confirm that terminating one EC2 instance does not impact application availability thanks to Auto Scaling.

## 1. Configure the Auto Scaling Group

We’ve updated our Auto Scaling group to maintain a **desired capacity** of 2 and a **minimum capacity** of 2.

| Setting          | Value                    |
| ---------------- | ------------------------ |
| Desired Capacity | 2                        |
| Minimum Capacity | 2                        |
| Launch Template  | `my-app-launch-template` |

![The image shows an AWS EC2 Auto Scaling group details page, displaying information such as group name, desired capacity, and launch template. The interface includes navigation options on the left for various AWS services.](https://kodekloud.com/kk-media/image/upload/v1752871784/notes-assets/images/Chaos-Engineering-Demo-Learning-and-Improvements/aws-ec2-auto-scaling-group-details.jpg)

> **lightbulb** Ensure your Auto Scaling group spans multiple Availability Zones for greater fault tolerance.

## 2. Verify Running Instances

1. Open the EC2 console.
2. Filter instances by the tag `Experiment=ready`.
3. Confirm that **two** EC2 instances are in the *running* state.

## 3. Rerun the FIS Experiment

Next, launch your Fault Injection Service experiment using the template you created:

```bash theme={null}
aws fis start-experiment --experiment-template-id my-fis-template
```

* Wait for the experiment to reach **Running** status.
* FIS will select a target instance (e.g., ending in **9456**) and terminate it.

![The image shows the AWS Resilience Hub interface, specifically the Fault Injection Service, displaying a completed action summary for terminating EC2 instances in the us-east-1 region.](https://kodekloud.com/kk-media/image/upload/v1752871785/notes-assets/images/Chaos-Engineering-Demo-Learning-and-Improvements/aws-resilience-hub-fault-injection-summary.jpg)

## 4. Validate Instance Termination

1. Return to the EC2 console.
2. Refresh the instance list.
3. Verify that the instance ending in **9456** is no longer *running*.
4. Clear the “running” filter to see that the instance is now in the **terminated** state.

## 5. Check Auto Scaling Activity

Navigate to your Auto Scaling group’s **Activity** tab. You should see entries indicating:

* The instance ending in **9456** was taken out of service.
* A new replacement instance was launched to restore the group back to **2**.

![The image shows an AWS management console screen with sections for activity notifications and activity history, detailing EC2 instance actions such as launching and terminating instances.](https://kodekloud.com/kk-media/image/upload/v1752871786/notes-assets/images/Chaos-Engineering-Demo-Learning-and-Improvements/aws-management-console-ec2-instance-actions.jpg)

## 6. Confirm Application Availability

Finally, verify on the EC2 dashboard that two **t3.micro** instances are running and have passed status checks (either *initializing* or *2/2 checks passed*). This confirms that our application remains available despite the induced failure.

![The image shows an AWS EC2 dashboard with two running instances, both of type t3.micro, with their status checks and availability zones displayed.](https://kodekloud.com/kk-media/image/upload/v1752871788/notes-assets/images/Chaos-Engineering-Demo-Learning-and-Improvements/aws-ec2-dashboard-t3micro-instances.jpg)

## Conclusion

Our FIS hypothesis has been validated: terminating one instance does not impact application uptime because the Auto Scaling group maintains the desired minimum capacity of 2.

***

## References

* [AWS Fault Injection Service (FIS)](https://docs.aws.amazon.com/fis/latest/userguide/what-is-fis.html)
* [Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
* [Chaos Engineering on AWS](https://aws.amazon.com/architecture/resiliency/)

- [Watch Video](https://learn.kodekloud.com/user/courses/chaos-engineering/module/d49a2b6d-60a1-4603-965d-7e8292688875/lesson/29d08a3c-5ef4-4346-b311-e2cdaf4ed846)
