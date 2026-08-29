# AWS Database Demo

Source: https://notes.kodekloud.com/docs/AWS-Cloud-Practitioner-CLF-C02/Technology-Part-Two/AWS-Database-Demo/page

This article provides a demo on creating and managing different types of databases using Amazon RDS, focusing on practical examples and configurations.

Welcome back, Cloud Practitioners! In this lesson, we'll walk through a comprehensive demo of the Amazon Relational Database Service (RDS). Our focus is on understanding the key use cases rather than the intricate backend details. By observing practical examples—such as launching a PostgreSQL database—you'll gain insights into how RDS simplifies database management.

## Overview

We will create three types of databases:

* A standard PostgreSQL database using the free tier.
* An Aurora PostgreSQL database that automatically provisions a cluster.
* An Aurora Serverless PostgreSQL database that scales dynamically.

## Launching a Standard PostgreSQL Database

Start at the RDS console (logged in and with the region set to Ohio). Click on **Create Database** and select the **Easy Create** option. Remember, RDS offers two sub-options: standard Aurora and Aurora Serverless. In this section, we are working with the primary RDS option for PostgreSQL.

<Frame>
  ![The image shows a configuration screen for selecting a database engine type on AWS, including options like PostgreSQL, MySQL, Oracle, and others.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862237/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_60.jpg)
</Frame>

When creating your first database:

* Select PostgreSQL.
* Choose the free tier to minimize configuration.
* Close the side panel and click **Auto-Generate a Password**.
* Leave default settings intact (e.g., encryption enabled and the default VPC is used).

<Frame>
  ![The image shows an AWS RDS database creation interface, with options for setting a master username, password, EC2 connection, and default settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862238/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_80.jpg)
</Frame>

After reviewing your settings:

<Frame>
  ![The image shows an AWS RDS configuration screen detailing database settings, including VPC, backups, security, and engine version, with various options enabled or disabled.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862240/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_90.jpg)
</Frame>

Click **Create Database**. The system begins provisioning your PostgreSQL database, and you'll see a progress notification at the bottom of the screen. This instance is created as a T3 micro PostgreSQL database. Even though options like restoring a database from S3 exist, in this demo, we are focusing on a basic configuration.

<Frame>
  ![The image shows an Amazon RDS dashboard with a PostgreSQL database named "database-1" being created, featuring options for database management and deployment suggestions.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862242/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_140.jpg)
</Frame>

## Creating an Aurora PostgreSQL Database

To create the Aurora PostgreSQL database, click **Create Database** again and choose **Easy Create**. This time, select Aurora PostgreSQL. Notice the interface differences in the upper right between standard PostgreSQL and Aurora. For this example, use the **DevTest** mode with default configurations to create "database two."

<Frame>
  ![The image shows an AWS RDS database creation interface, highlighting the selection of Aurora PostgreSQL-Compatible Edition with its features listed on the right.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862243/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_170.jpg)
</Frame>

On the Aurora configuration page, you'll configure:

* Instance size.
* DB cluster identifier.
* Master username.

After clicking **Create Database**, an Aurora cluster is provisioned. Unlike the standard PostgreSQL instance, Aurora instantly creates a database cluster. Initially, the cluster comprises one instance, but you have the flexibility to add more instances later. The dashboard will show the Aurora PostgreSQL instance along with a reader instance.

<Frame>
  ![The image shows an AWS RDS setup page for creating an Aurora PostgreSQL database, with options for instance size, DB cluster identifier, and master username.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862244/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_190.jpg)
</Frame>

## Deploying an Aurora Serverless PostgreSQL Database

For the third database, click **Create Database** and choose **Standard Create**. Select Aurora PostgreSQL-Compatible Edition, then pick a version that supports Serverless v2. Enter a database name (for example, "dev-test") and dismiss any pop-up triggers that appear.

During the serverless instance configuration:

* You have the option to auto-generate a password.
* Select between Aurora Standard and Aurora Optimized.
* Configure the compute capacity by choosing a range. Typically, this demo uses a minimum of 1 and a maximum of 4 Aurora Capacity Units (ACUs), with 1 ACU providing 2 GB of memory.
* This configuration ensures that your serverless database scales automatically based on demand.

<Frame>
  ![The image shows an AWS RDS configuration page for selecting Aurora DB cluster storage options, highlighting compatibility issues with the selected Aurora PostgreSQL version.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862246/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_290.jpg)
</Frame>

Additional instance settings include backup configurations, linking Aurora as a replica, and various networking options. In this demo, the default settings are sufficient. After confirming your settings by clicking **Create Database**, the serverless database is provisioned.

<Frame>
  ![The image shows an AWS RDS instance configuration page, detailing options for DB instance class, capacity range, and availability settings, including serverless and memory-optimized classes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862247/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_320.jpg)
</Frame>

An extra screenshot further details the serverless v2 settings, such as capacity ranges and supported DB engine versions.

<Frame>
  ![The image shows an AWS RDS instance configuration page, highlighting options for serverless v2, capacity range, and DB engine versions.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862248/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_350.jpg)
</Frame>

Another diagram illustrates additional networking and availability configurations, including connections to compute resources.

<Frame>
  ![The image shows an AWS RDS configuration page, detailing options for availability, connectivity, and network type, with a list of supported DB engine versions on the right.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862250/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_360.jpg)
</Frame>

## Viewing Your Databases

Once all three databases are created, your dashboard displays:

* A standard PostgreSQL database.
* An Aurora PostgreSQL database (with both instance and cluster details).
* A serverless Aurora PostgreSQL database (showing scaling details from 1 to 4 ACUs).

<Frame>
  ![The image shows an Amazon RDS dashboard displaying a list of databases with their identifiers, statuses, roles, engines, and regions.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862251/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_400.jpg)
</Frame>

By clicking on the database credentials link, you can connect remotely to any of these databases just as if they were running locally. One of the PostgreSQL instances might display an ongoing backup process on the RDS summary view.

<Frame>
  ![The image shows an Amazon RDS dashboard displaying database details, including summary, connectivity, security settings, and current status of a PostgreSQL instance.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862253/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Database-Demo/frame_440.jpg)
</Frame>

<Callout icon="lightbulb">
  In this demo, you learned how to launch three unique configurations on AWS RDS:

  * A standard PostgreSQL database.
  * An Aurora PostgreSQL database (with automatic cluster creation).
  * An Aurora Serverless PostgreSQL database with auto-scaling capabilities.
</Callout>

If you have any questions, please feel free to reach out in the forums. We look forward to seeing you in the next lesson!

## Further Reading

* [AWS RDS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
* [Amazon Aurora User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Welcome.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-practitioner-clf-c02/module/f47a1e6e-5593-4fac-bc8b-f24ef6e6f418/lesson/a1770e51-2e63-4545-b255-cdb179eb8d8b" />
</CardGroup>
