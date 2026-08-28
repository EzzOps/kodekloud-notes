# Licensing on RDS

Source: https://notes.kodekloud.com/docs/AWS-RDS/Different-Database-Engines-in-RDS/Licensing-on-RDS/page

Explains Amazon RDS licensing options for commercial and open source databases, comparing license included versus bring your own license, migration guidance and compliance considerations.

Welcome back. In this lesson we’ll explain how database licensing works when you run engines in Amazon RDS, what options AWS provides, and practical guidance for choosing between them during migration or ongoing operations.

## Open-source vs. vendor-licensed engines

Databases such as PostgreSQL and MariaDB are open source. You can install and run them on [Amazon Elastic Compute Cloud (EC2)](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) or on-premises without paying a vendor for a license. Running these engines on Amazon RDS (see [Introduction to AWS Databases](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases)) is the same in that AWS does not collect vendor licensing fees for open-source engines.

By contrast, commercial database engines—most notably Oracle Database and Microsoft SQL Server—use vendor licensing models. When you run these engines on Amazon RDS (see [Introduction to AWS Databases](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases)), you typically choose one of two licensing approaches:

## Licensing options in Amazon RDS

| Licensing option              | How it works                                                                                                                                                                          | Typical use cases                                                                                               |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| License-included              | AWS provides the required database license as part of the RDS instance billing. No separate vendor license procurement is required; AWS handles licensing and billing on your behalf. | Greenfield deployments or when you prefer AWS-managed licensing and simplified operations.                      |
| Bring Your Own License (BYOL) | You use an existing vendor license that you already own and remain responsible for meeting the vendor’s licensing terms (mobility, support contracts, compliance).                    | Migrations where you already have active on-premises licenses and want to avoid paying twice during transition. |

* License-included: simplifies procurement and ongoing license administration because the license cost is bundled into the RDS instance price.
* Bring Your Own License (BYOL): lets you reuse existing vendor licenses to avoid duplicate costs during migration, but you must ensure compliance with the vendor’s rules.

If you’re migrating a legacy application that already has an active vendor license, BYOL often prevents you from paying twice for the same license during the migration window. Many teams lift-and-shift databases to Amazon RDS using BYOL, then switch to the license-included model once their existing contracts expire to offload license management to AWS.

AWS supports switching between BYOL and license-included in many scenarios, but exact procedures and eligibility depend on the database engine and the vendor agreement. Confirm the required steps for your specific engine (for example, Oracle or SQL Server) and whether license mobility or special confirmations are necessary.

<Callout icon="lightbulb">
  Before choosing BYOL, always verify your vendor license terms: check license mobility, support contract implications, and any required vendor confirmations. Licensing rules vary by vendor, edition, and region.
</Callout>

## Choosing the right approach

Consider the following when deciding between license-included and BYOL:

* Existing contracts: If you have active licenses and maintenance, BYOL can reduce migration costs.
* Operational overhead: License-included reduces administrative burden and centralizes billing.
* Long-term costs: Compare the total cost of ownership (TCO) over the expected lifetime of the database.
* Compliance and auditability: Ensure you can meet vendor reporting and compliance requirements under BYOL.

Summary: License-included on Amazon RDS simplifies license management by bundling vendor licenses into instance pricing. BYOL helps you avoid duplicate licensing during migration but requires you to maintain compliance with vendor terms. Choose the model that aligns with your contracts, migration strategy, and operational preferences. For more detail, see [Introduction to AWS Databases](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases).

<Frame>
  <img alt="A slide comparing AWS licensing options for proprietary databases, with headings about BYOL vs license-included and a note that switching between them is allowed, illustrated by Oracle and SQL Server logos. The text explains that databases like Oracle and Microsoft SQL Server require licensing and you can either bring your own license or use AWS’s license-included option." />
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/0525aa45-ab52-4496-8a27-0ab6ec827d6f/lesson/8924c486-b010-4bec-8942-1b4a058f2da0" />
</CardGroup>
