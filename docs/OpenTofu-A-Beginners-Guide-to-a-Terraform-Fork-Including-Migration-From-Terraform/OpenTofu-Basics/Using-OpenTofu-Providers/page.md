# terraform.tfvars: type = "t3.micro"  # (2)
# vars.auto.tfvars: type = "t3.small"  # (3)
$ tofu apply -var "type=t2.medium"     # (5)
```

The final `instance_type` will be **t2.medium**, since `-var` overrides all others.

***

## Links and References

* [OpenTofu GitHub](https://github.com/opentofu/opentofu)
* [Terraform Input Variables](https://developer.hashicorp.com/terraform/language/values/variables)
* [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/e015a0a3-3e40-43f0-93a0-2ca32c47b5f8" />
</CardGroup>


# Using OpenTofu Providers

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Using-OpenTofu-Providers/page

This guide explains how to use OpenTofu providers for resource provisioning across various platforms.

OpenTofu relies on a plugin-based architecture to manage providers, enabling you to provision resources across AWS, GCP, Azure, and many more platforms. This guide covers how to initialize your working directory, understand provider types, and reference provider plugins in your configurations.

## 1. Initializing Your Directory

Run the following command in a directory containing your OpenTofu configuration files:

```bash theme={null}
tofu init
```

When executed against valid `.tf` files, `tofu init` will:

* Install all required provider plugins.
* Create a lock file (`.terraform.lock.hcl`) to pin provider versions.
* Ensure idempotent behavior: rerunning does not alter existing infrastructure.

```bash theme={null}
$ tofu init

Initializing the backend...

Initializing provider plugins...
- Finding the latest version of hashicorp/local...
- Installing hashicorp/local v2.4.1...
- Installed hashicorp/local v2.4.1 (signed, key ID 0C0AF313E5FD9F80)

Providers are signed by their developers.
If you'd like to know more about provider signing, see:
  https://opentofu.org/docs/cli/plugins/signing/

OpenTofu has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that OpenTofu can guarantee the same selections next time you run "tofu init".

OpenTofu has been successfully initialized!
```

<Callout icon="lightbulb">
  Always commit the `.terraform.lock.hcl` file to your VCS. This ensures consistent provider versions across environments.
</Callout>

Plugins are stored under the hidden directory
`.terraform/providers` in your working directory.

## 2. Provider Types

Providers are distributed via [Terraform Registry] and [OpenTofu Registry], and fall into three categories:

| Provider Type | Maintainer                          | Registry Badge  |
| ------------- | ----------------------------------- | --------------- |
| Official      | HashiCorp                           | Official badge  |
| Verified      | Third-party (reviewed by HashiCorp) | Checkmark badge |
| Community     | Individual contributors             | No badge        |

<Frame>
  ![The image is a diagram showing HashiCorp's providers, including AWS, Google Cloud, Azure, and others, leading to the Terraform and OpenTofu registries.](https://kodekloud.com/kk-media/image/upload/v1752882833/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Using-OpenTofu-Providers/hashicorp-providers-terraform-diagram.jpg)
</Frame>

## 3. Plugin Naming Conventions

Each provider is referenced by a source address with this structure:

```text theme={null}
<hostname>/<namespace>/<type>
```

* **hostname** (optional): Defaults to `registry.opentofu.org` if omitted.
* **namespace**: Organization or author (e.g., `hashicorp`).
* **type**: Provider name (e.g., `aws`, `local`).

### Examples

Using the **default registry**:

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"  # Implicitly registry.opentofu.org
      version = "~> 2.4.0"
    }
  }
}
```

Using the **fully qualified** address:

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "registry.opentofu.org/hashicorp/local"
      version = "~> 2.4.0"
    }
  }
}
```

## 4. References

* [Terraform Registry]: https://registry.terraform.io/
* [OpenTofu Registry]: https://registry.opentofu.org/
* [Provider Signing Docs]: https://opentofu.org/docs/cli/plugins/signing/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/21846b0b-7e9c-4bea-84fa-c249512886c5" />
</CardGroup>
