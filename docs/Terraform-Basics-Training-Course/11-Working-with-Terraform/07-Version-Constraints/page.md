# local_file.pet:
resource "local_file" "pet" {
  content              = "We love pets!"
  directory_permission = "0777"
  file_permission      = "0777"
  filename             = "/root/pets.txt"
  id                   = "cba595b7d9f94ba1107a46f3f731912d95fb3d2c"
}
```

To view this state in JSON format, use the `-json` flag:

```plaintext theme={null}
$ terraform show -json
{"format_version":"0.1","terraform_version":"0.13.0","values":{"root_module":{"resources":[{"address":"local_file.pet","mode":"managed","type":"local_file","name":"pet","provider_name":"registry.terraform.io/hashicorp/local","schema_version":0,"values":{"content":"We love pets!","content_base64":null,"directory_permission":"0777","file_permission":"0777","filename":"/root/pets.txt","id":"cba595b7d9f94ba1107a46f3f731912d95fb3d2c","sensitive_content":null}}]}}}
```

***

## Terraform Providers

The `terraform providers` command lists all providers required by your configuration along with those used in your state. It also supports mirroring provider plugins to a specified directory.

For example:

```bash theme={null}
$ terraform providers
Providers required by configuration:
    └── provider[registry.terraform.io/hashicorp/local]

Providers required by state:
    provider[registry.terraform.io/hashicorp/local]

$ terraform providers mirror /root/terraform/new_local_file
- Mirroring hashicorp/local...
- Selected v1.4.0 with no constraints
- Downloading package for windows_amd64...
- Package authenticated: signed by HashiCorp
```

<Callout icon="lightbulb">
  Mirroring providers can accelerate deployments in environments with restricted internet access, ensuring that all necessary plugins are available locally.
</Callout>

***

## Terraform Output Variables

Terraform output variables allow you to extract and display configuration values once your infrastructure has been applied. This is particularly useful for showing key results or passing values between modules.

Consider the following configuration:

```hcl theme={null}
resource "local_file" "pet" {
  filename       = "/root/pets.txt"
  content        = "We love pets!"
  file_permission = "0777"
}

resource "random_pet" "cat" {
  length    = "2"
  separator = "-"
}

output "content" {
  value       = local_file.pet.content
  sensitive   = false
  description = "Print the content of the file"
}

output "pet-name" {
  value       = random_pet.cat.id
  sensitive   = false
  description = "Print the name of the pet"
}
```

After applying the configuration, run:

```bash theme={null}
$ terraform output
content = We love pets!
pet-name = huge-owl
```

***

## Terraform Refresh

The `terraform refresh` command synchronizes your Terraform state with the actual state of your infrastructure. This is particularly useful when external changes have occurred outside of Terraform.

Consider the following configuration:

```hcl theme={null}
resource "local_file" "pet" {
  filename       = "/root/pets.txt"
  content        = "We love pets!"
  file_permission = "0777"
}

resource "random_pet" "cat" {
  length    = "2"
  separator = "_"
}
```

When you run a plan, Terraform refreshes the state in-memory:

```bash theme={null}
$ terraform plan
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be persisted to local or remote state storage.

random_pet.cat: Refreshing state... [id=huge-owl]
local_file.pet: Refreshing state... [id=cba595b7d9f94ba1107a46f3f731912d95fb3d2c]
--------------------------------------------------------------------
No changes. Infrastructure is up-to-date.
```

You can also update the state file without changing any infrastructure by using the `-refresh-only` flag with `terraform apply`:

```bash theme={null}
$ terraform apply -refresh-only
random_pet.cat: Refreshing state... [id=huge-owl]
local_file.pet: Refreshing state... [id=cba595b7d9f94ba1107a46f3f731912d95fb3d2c]
```

To prevent automatic refreshing during plan or apply, use the `-refresh=false` option.

***

## Terraform Graph

The `terraform graph` command creates a DOT format representation of resource dependencies in your configuration. The graph visually outlines how resources are connected.

For example, in this configuration with dependency references:

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "My favorite pet is ${random_pet.my-pet.id}"
}

resource "random_pet" "my-pet" {
  prefix    = "Mr"
  separator = "."
  length    = "1"
}
```

Running the command produces:

```bash theme={null}
$ terraform graph
digraph {
  compound = "true"
  newrank = "true"
  subgraph "root" {
    "[root] local_file.pet (expand)" [label = "local_file.pet", shape = "box"]
    "[root]" 
    provider["registry.terraform.io/hashicorp/local"] [label = "provider[\"registry.terraform.io/hashicorp/local\"]", shape = "diamond"]
    "[root]"
    provider["registry.terraform.io/hashicorp/random"] [label = "provider[\"registry.terraform.io/hashicorp/random\"]", shape = "diamond"]
    "[root] random_pet.my-pet (expand)" [label = "random_pet.my-pet", shape = "box"]
    "[root] local_file.pet (expand)" -> "[root] local_file.pet (expand)" [label = "provider[\"registry.terraform.io/hashicorp/local\"]"]
    "[root] local_file.pet (expand)" -> "[root] random_pet.my-pet (expand)"
    "[root] meta.count-boundary (EachMode fixup)" -> "[root] local_file.pet (expand)"
  }
}
```

<Callout icon="lightbulb">
  The DOT format may be challenging to interpret directly. Use a visualization tool like Graphviz to render a graphical version of the dependency graph.
</Callout>

***

## Visualizing the Graph with Graphviz

Graphviz is a widely-used tool for converting DOT files into visual images. On Ubuntu, you can install Graphviz as follows:

```bash theme={null}
$ apt update
$ apt install graphviz -y
```

After installation, pipe the output of the `terraform graph` command into Graphviz's `dot` command to create an SVG:

```bash theme={null}
$ terraform graph | dot -Tsvg > graph.svg
```

Open the resulting `graph.svg` file in your browser to see a visual representation of your resource dependencies. This helps in understanding how resources like the local file and random pet interact through dependency expressions.

***

That concludes our comprehensive look at essential Terraform commands. Use these tools to validate, format, and manage your infrastructure configurations effectively. Now, proceed to the hands-on labs to further explore and practice Terraform’s capabilities.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/98de9b33-985e-4ec4-9903-b39856d309e8/lesson/a1fb64aa-097f-46c1-92e8-0902161b2b0f" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/98de9b33-985e-4ec4-9903-b39856d309e8/lesson/870d2152-4979-422c-9dff-766e0ec630f5" />
</CardGroup>


# Version Constraints

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Working-with-Terraform/Version-Constraints/page

This article explains how to specify provider versions in Terraform using version constraints to maintain configuration stability.

In this article, we explain how to specify provider versions in Terraform to ensure your configuration consistently uses the intended plugin version. By default, running the `terraform init` command downloads the latest provider plugins from the public Terraform Registry. This behavior, however, might lead to unexpected issues if newer provider versions introduce breaking changes. To prevent this, you can restrict provider versions using version constraints in your Terraform configuration.

Consider the basic Terraform configuration below that creates a local file:

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pet.txt"
  content  = "We love pets!"
}
```

When you run:

```bash theme={null}
$ terraform init
```

you might see output similar to the following:

```bash theme={null}
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/local...
- Installing hashicorp/local v1.4.0...
- Installed hashicorp/local v1.4.0 (signed by HashiCorp)

The following providers do not have any version constraints in configuration, so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking changes, we recommend adding version constraints in a required_providers block in your configuration, with the constraint strings suggested below.

* hashicorp/local: version = "~> 1.4.0"

Terraform has been successfully initialized!
```

<Callout icon="lightbulb">
  Always specify provider versions to ensure your Terraform configurations remain stable, especially if newer provider releases might introduce breaking changes.
</Callout>

Because provider functionalities can change drastically between versions, it is critical to use a specific version that you have thoroughly tested. Detailed instructions for each provider's versioning are available on the provider’s Terraform Registry page. For instance, if the default and latest version of the local provider is 2.0.0 but your configuration requires an older version such as 1.4.0, update your configuration accordingly.

## Specifying a Specific Provider Version

To enforce a particular version of the local provider (for example, version 1.4.0), include a `terraform` block with a `required_providers` sub-block. This block explicitly instructs Terraform which version to install. Consider the following configuration:

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "1.4.0"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pet.txt"
  content  = "We love pets!"
}
```

When you run `terraform init`, Terraform reads the configuration and installs version 1.4.0 of the local provider.

## Using Comparison Operators for Version Constraints

Terraform supports several comparison operators to manage provider version constraints. For example, if you want to exclude a specific version, you can use the not-equal operator. In the configuration below, Terraform is directed to avoid version 2.0.0:

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "!= 2.0.0"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pet.txt"
  content  = "We love pets!"
}
```

You can also combine comparison operators to define a version range. The following configuration tells Terraform to use any version greater than 1.2.0 but less than 2.0.0, explicitly excluding version 1.4.0:

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "> 1.2.0, < 2.0.0, != 1.4.0"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pet.txt"
  content  = "We love pets!"
}
```

In this setup, Terraform may choose version 1.3.0 if it is the highest acceptable version according to the defined constraints.

## The Pessimistic Constraint Operator

Terraform offers the pessimistic constraint operator (`~>`) to allow patch-level flexibility while preventing major version upgrades. For example, using the following configuration:

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 1.2"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pet.txt"
  content  = "We love pets!"
}
```

Terraform can use version 1.2 and any incremental versions such as 1.3 or 1.4, up to but not including 2.0. If the maximum available version in the registry is 1.4.0, that version will be installed.

If you want to tightly constrain the version (for example, only accepting versions from 1.2.0 up to 1.2.9), consider the following configuration:

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 1.2.0"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pet.txt"
  content  = "We love pets!"
}
```

In this configuration, Terraform will install version 1.2.2 if that is the highest version available within the defined range.

After updating your configuration, running:

```bash theme={null}
$ terraform init
```

will produce output similar to this:

```bash theme={null}
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/local versions matching "~> 1.2.0"...
- Installing hashicorp/local v1.2.2...
- Installed hashicorp/local v1.2.2 (signed by HashiCorp)

Terraform has been successfully initialized!
```

This output confirms that Terraform installed the specified version of the local provider.

<Callout icon="lightbulb">
  For more best practices on managing Terraform configurations and version constraints, explore additional resources and updated documentation on the [Terraform Registry](https://registry.terraform.io/) and [Terraform Documentation](https://www.terraform.io/docs).
</Callout>

That concludes our article on Terraform version constraints. To further reinforce your understanding, experiment with these versioning techniques in your Terraform practice environment to ensure your configurations remain stable over time.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/98de9b33-985e-4ec4-9903-b39856d309e8/lesson/5f532378-f63e-4302-863e-f021f3f6b35b" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/98de9b33-985e-4ec4-9903-b39856d309e8/lesson/0b6ae539-3d1d-437f-9dac-ee6c0907fd7d" />
</CardGroup>
