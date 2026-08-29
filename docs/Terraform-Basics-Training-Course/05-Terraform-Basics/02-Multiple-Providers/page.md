# Multiple Providers

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Basics/Multiple-Providers/page

Learn to leverage multiple providers in Terraform configurations to generate random resources alongside existing ones.

In this lesson, you’ll learn how to leverage multiple providers in a Terraform configuration. Until now, you have been using a single provider (local) to deploy a file to your system:

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

Terraform makes it easy to integrate additional providers. In this example, we introduce the random provider, which is capable of generating random resources, such as IDs, integers, or even pet names. Our goal is to generate a random pet name by adding a new resource block that uses the random provider.

By referring to the provider documentation, you can add the following resource block to your existing main.tf file. The resource block is divided into two parts: the provider (random) and the resource type (pet). We name this resource "my-pet" and specify three arguments:

* prefix: A string added to the beginning of the generated pet name.
* separator: A character that separates the prefix from the pet name.
* length: The number of words in the generated pet name.

The updated main.tf file now looks like this:

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}

resource "random_pet" "my-pet" {
  prefix    = "Mrs"
  separator = "."
  length    = 1
}
```

This configuration now contains resource definitions for both the local file and the random pet.

<Callout icon="lightbulb">
  Before proceeding with any changes or deployments, always run the Terraform initialization command to download and configure all required provider plugins.
</Callout>

## Initializing Providers

Before generating an execution plan and applying the configuration, you must initialize the providers by using the Terraform init command. This command downloads and sets up the necessary plugins for each provider being used. When you run the following command, Terraform will initialize both the local and random provider plugins:

```bash theme={null}
$ terraform init
Initializing the backend...

Initializing provider plugins...
- Using previously-installed hashicorp/local v2.0.0
- Finding latest version of hashicorp/random...
- Installing hashicorp/random v2.3.0...
- Installed hashicorp/random v2.3.0 (signed by HashiCorp)

The following providers do not have any version constraints in configuration,
so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking
changes, we recommend adding version constraints in a required_providers block
in your configuration, with the constraint strings suggested below.
* hashicorp/local: version = "~> 2.0.0"
* hashicorp/random: version = "~> 2.3.0"

Terraform has been successfully initialized!
```

As shown, Terraform reuses the already installed local provider and newly installs the random provider since it had not been used before.

## Reviewing the Execution Plan

After initialization, review the planned actions by running the Terraform plan command. In this plan, the local file resource remains unchanged, and a new resource (“my-pet”) is set to be created:

```plaintext theme={null}
$ terraform plan
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but
will not be persisted to local or remote state storage.

local_file.pet: Refreshing state...
[id=[AWS_SECRET_ACCESS_KEY]]
.
.
