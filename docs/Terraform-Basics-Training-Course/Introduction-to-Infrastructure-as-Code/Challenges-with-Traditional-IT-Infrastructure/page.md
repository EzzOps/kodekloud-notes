# local_file.pet must be replaced.
-/+ resource "local_file" "pet" {
      content             = "We love pets!"
      directory_permission = "0777"
  ~ file_permission      = "0777" -> "0700" # forces replacement
      filename            = "/root/pets.txt"
  ~ id                   = "5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf" -> (known after apply)
}

Plan: 1 to add, 0 to change, 1 to destroy.

Note: You didn't specify an "-out" parameter to save this plan, so Terraform can't guarantee that exactly these actions will be performed if "terraform apply" is subsequently run.
```

<Callout icon="lightbulb">
  Even though the configuration change is minor, Terraform treats the resource as immutable. This means the old resource is destroyed and a new one is created with the updated settings.
</Callout>

To proceed with applying these changes, run the Terraform apply command. Confirm the action by typing "yes" when prompted:

```bash theme={null}
$ terraform apply
# local_file.pet must be replaced
-/+ resource "local_file" "pet" {
    content              = "We love pets!"
    directory_permission = "0777"
    ~ file_permission    = "0777" -> "0700" # forces replacement
    filename             = "/root/pets.txt"
    ~ id                 = "5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf" -> (known after apply)
}
Plan: 1 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
Terraform will perform the actions described above.
Only 'yes' will be accepted to approve.

Enter a value: yes
local_file.pet: Destroying... [id=5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf]
local_file.pet: Destruction complete after 0s
local_file.pet: Creating...
local_file.pet: Creation complete after 0s
Applied! Resources: 1 added, 0 changed, 1 destroyed.
```

## Destroying the Resource

When you need to completely delete the infrastructure, use the Terraform destroy command. Running this command will generate an execution plan that shows every attribute of the resource marked for deletion. The minus symbol (-) indicates that each attribute will be removed.

Below is an example output from the Terraform destroy command:

```bash theme={null}
$ terraform destroy
local_file.pet: Refreshing state... [id=5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

# local_file.pet will be destroyed
- resource "local_file" "pet" {
    content             = "We love pets!" -> null
    directory_permission = "0777" -> null
    file_permission     = "0700" -> null
    filename            = "/root/pets.txt" -> null
    id                  = "5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf" -> null
}

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
Terraform will destroy all your managed infrastructure, as shown above.
There is no undo. Only 'yes' will be accepted to confirm.

Enter a value: yes

local_file.pet: Destroying... [id=5f8fb950ac60f7f23ef968097cda0a1fd3c11bdf]
local_file.pet: Destruction complete after 0s

Destroy complete! Resources: 1 destroyed.
```

<Callout icon="triangle-alert">
  Double-check your plan before running the destroy command, as this action will permanently delete all managed resources in the current configuration.
</Callout>

## Conclusion

You have now learned how to update and destroy infrastructure using Terraform. Updating a resource triggers a replacement, while the destroy command allows for the complete removal of the resource. Practice these steps to reinforce your Terraform skills and better manage your infrastructure lifecycle.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/385de3de-cd58-4925-9a24-207ebd7844b3/lesson/885285d5-9916-42c5-9558-f75a0f6503af" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/385de3de-cd58-4925-9a24-207ebd7844b3/lesson/e3732897-89a4-42ce-b045-4cda7f012907" />
</CardGroup>


# Challenges with Traditional IT Infrastructure

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Introduction-to-Infrastructure-as-Code/Challenges-with-Traditional-IT-Infrastructure/page

This article discusses the challenges of traditional IT infrastructure and the transition to cloud computing and Infrastructure as Code for improved application delivery.

In this lesson, we explore the evolution of application delivery—from the traditional IT approach to modern cloud computing and Infrastructure as Code (IaC). This discussion begins with an overview of how infrastructure provisioning has historically been handled and the challenges associated with traditional methods.

## Traditional Infrastructure Provisioning

Imagine an organization planning to launch a new application. The process kicks off with the business defining the application's requirements. A business analyst gathers these needs, analyzes them, and translates them into high-level technical specifications. These requirements are then handed over to a solution architect who designs the deployment architecture. This design includes infrastructure considerations such as the type, specifications, and quantity of servers required for various roles: front-end web servers, back-end servers, databases, load balancers, etc.

Under the traditional IT model, these servers are hosted in the organization's on-premises data center. If extra hardware is needed, the procurement team orders the equipment from vendors—a process that can take days, weeks, or even months.

Once the hardware arrives, field engineers perform the racking and stacking of equipment. Then, system administrators configure the systems, network administrators manage connectivity, storage teams allocate necessary storage, and backup administrators set up data protection mechanisms. Only after these steps is the infrastructure ready for the application teams to deploy their services.

**Key challenges of the traditional deployment model include:**

* Long turnaround times: The period from hardware procurement to application deployment can span several weeks or months.
* Limited scalability: Dynamically scaling the infrastructure up or down is challenging.
* High overall costs: Both deployment and ongoing maintenance incur significant expenses.
* Manual processes: Many provisioning tasks—like cabling and equipment configuration—are manual, raising the risk of human error and inconsistencies.
* Underutilization of resources: To handle peak loads, infrastructure is often over-provisioned, leading to resource wastage during off-peak periods.

<Frame>
  ![The image illustrates a business process flow, highlighting slow deployment, expense, limited automation, human error, and wasted resources, involving various teams and cloud/data center technologies.](https://kodekloud.com/kk-media/image/upload/v1752884180/notes-assets/images/Terraform-Basics-Training-Course-Challenges-with-Traditional-IT-Infrastructure/frame_200.jpg)
</Frame>

## The Shift to Cloud Computing

Over the past decade, many organizations have transitioned to virtualization and cloud platforms provided by industry leaders such as Amazon AWS, Microsoft Azure, and Google Cloud Platform. Migrating to the cloud significantly reduces the time required to spin up infrastructure and deploy applications.

In a cloud environment, you no longer need to manage physical hardware. Instead, cloud providers handle the underlying data center infrastructure and services. This transformation means that a virtual machine can be provisioned in minutes rather than the several months required by traditional methods. Cloud platforms not only lower costs by reducing the need for on-premises management and labor but also offer robust API support to streamline automation.

Built-in auto-scaling and elasticity in cloud infrastructures further minimize resource wastage. However, even with these benefits, manual provisioning through cloud management consoles can still be inefficient in highly elastic and scalable environments. Multiple teams and processes can introduce delays and inconsistencies, primarily when human intervention is required.

<Callout icon="lightbulb">
  To maximize cloud efficiency, automation is crucial. Relying solely on manual processes in a cloud environment can negate many benefits of elasticity and rapid scaling.
</Callout>

## The Emergence of Infrastructure as Code

In response to these challenges, organizations began developing scripts and tools to automate infrastructure provisioning. Early solutions included shell scripts and programs written in Python, Ruby, Perl, or PowerShell to interact with cloud APIs, enabling faster and more consistent deployments.

Over time, these practices evolved into what is now known as Infrastructure as Code (IaC) — a modern approach that treats infrastructure provision and management as software. IaC not only accelerates the deployment process but also enhances consistency, reduces the likelihood of human error, and simplifies infrastructure scaling.

<Frame>
  ![The image displays logos of various "Infrastructure as Code" tools, including Docker, Ansible, Terraform, CloudFormation, Vagrant, Packer, SaltStack, and Puppet.](https://kodekloud.com/kk-media/image/upload/v1752884181/notes-assets/images/Terraform-Basics-Training-Course-Challenges-with-Traditional-IT-Infrastructure/frame_340.jpg)
</Frame>

## Conclusion

The traditional IT model, characterized by manual processes and long lead times, poses several challenges for modern application delivery. The shift to cloud computing has mitigated many of these issues, but manual interventions still remain a bottleneck. Infrastructure as Code offers a robust solution, enabling organizations to automate and streamline infrastructure management in a scalable and efficient manner.

In the next lesson, we will delve deeper into Infrastructure as Code, examining its key components and the benefits it brings to modern infrastructure management.

<Callout icon="lightbulb">
  For more insights on cloud technologies and Infrastructure as Code, consider exploring [Kubernetes Documentation](https://kubernetes.io/docs/) and [Terraform Registry](https://registry.terraform.io/).
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e860c2fb-d55e-48f2-87cc-9149460b600a/lesson/a9418c73-1a78-4755-b551-bd341d1b6fa9" />
</CardGroup>
