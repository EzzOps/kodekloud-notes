# Removing Resources with the removed Block

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Refactoring-Terraform-State/Removing-Resources-with-the-removed-Block/page

Explains Terraform removed block to safely remove resources from state without destroying infrastructure, providing workflow steps, examples, use cases, and differences from the moved block.

In this lesson we explain Terraform's `removed` block: what it does, when to use it, and the correct workflow to remove resources from Terraform state without destroying the underlying infrastructure.

Real-world scenario: production databases
You've been managing two production PostgreSQL instances with Terraform for months. The database team now needs full manual control of schema changes on one instance (for example, `production-db-02`) and asks that Terraform stop managing that instance so they can make manual changes safely.

<Frame>
  <img alt="The image depicts a &#x22;Real-World Scenario&#x22; with a purple background, featuring an abstract icon above two stacked database symbols labeled &#x22;production_db_01&#x22; and &#x22;production_db_02&#x22;." />
</Frame>

Original Terraform resource definitions
These were the original resource blocks in your configuration:

```hcl theme={null}
resource "google_sql_database_instance" "prd_db_1" {
  name             = "production-db-01"
  database_version = "POSTGRES_15"
  region           = "us-central1"
  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database_instance" "prd_db_2" {
  name             = "production-db-02"
  database_version = "POSTGRES_15"
  region           = "us-central1"
  settings {
    tier = "db-f1-micro"
  }
}
```

Why you can't just delete the resource block
Removing the `prd_db_2` resource block from code and running `terraform plan` will make Terraform interpret the resource as removed from configuration and propose to destroy the real infrastructure:

```plaintext theme={null}
