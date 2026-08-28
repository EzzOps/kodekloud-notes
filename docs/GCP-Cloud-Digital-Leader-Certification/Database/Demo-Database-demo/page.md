# Demo Database demo

Source: https://notes.kodekloud.com/docs/GCP-Cloud-Digital-Leader-Certification/Database/Demo-Database-demo/page

This article covers launching and managing a cloud database using Google Cloud Platform, including setting up a Cloud SQL instance and connecting to it.

Hello and welcome back to this demo lesson on launching and managing a cloud database using Google Cloud Platform (GCP). In this session, we will set up a Cloud SQL instance, connect to it using Cloud Shell, and explore essential configuration options.

## Cloud Database Architecture

The architecture for this demo is straightforward: users access a URL on their smartphones or laptops, which routes through a cloud load balancer to an instance group. This group then connects to Cloud SQL for database services.

Below is a diagram illustrating the typical Google Cloud architecture:

<Frame>
  ![The image is a diagram of a Google Cloud architecture showing mobile devices connecting to a cloud load balancer, which distributes traffic to an instance group of virtual machines, with a connection to Cloud SQL.](https://kodekloud.com/kk-media/image/upload/v1752875219/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Database-demo/google-cloud-architecture-diagram.jpg)
</Frame>

## Creating a Cloud SQL Instance

In this section, you'll learn how to spin up a Cloud SQL instance and configure it for your needs.

<Callout icon="lightbulb">
  In production environments, always secure your database with a strong password.
</Callout>

Follow these steps:

1. **Access the GCP Console:** Start by logging into your GCP account and navigating to the Cloud SQL page.
2. **Create Instance:** Click on **Create Instance**.

<Frame>
  ![The image shows a Google Cloud interface for managing Cloud SQL instances, with options to create an instance or migrate data. It includes a brief description of Cloud SQL services.](https://kodekloud.com/kk-media/image/upload/v1752875220/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Database-demo/google-cloud-sql-management-interface.jpg)
</Frame>

3. **Select MySQL:** From the three options provided, choose **MySQL**. Name your instance "main-db". For this demo, the instance is set up without a password. (For production, always use password protection.)
4. **Configure Instance Settings:** Choose your desired MySQL version. Additional configurations include:
   * **Automated Backups:** GCP automatically backs up your database.
   * **High Availability:** The database is spread across multiple zones to minimize downtime.
   * **Point-in-Time Recovery:** Enables quick recovery from failures.
5. **Choose Environment:** Optionally, select whether the database is for development or production. Leave the region at its default value for this demo.
6. **Create Instance:** Once you have verified your settings, click on **Create Instance**. The process usually takes about 6 to 7 minutes.

<Frame>
  ![The image shows a Google Cloud interface for creating a MySQL instance, displaying configuration options and a summary of instance specifications like region, memory, and storage.](https://kodekloud.com/kk-media/image/upload/v1752875222/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Database-demo/google-cloud-mysql-instance-creation.jpg)
</Frame>

After the instance is created, click on it to open the dashboard, where you can monitor CPU utilization, active connections, and other key metrics.

<Frame>
  ![The image shows a Google Cloud SQL dashboard for a MySQL database instance named "main-db," displaying options for monitoring metrics like CPU utilization and active connections. It also includes configuration details such as vCPUs, memory, and SSD storage.](https://kodekloud.com/kk-media/image/upload/v1752875223/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Database-demo/google-cloud-sql-mysql-dashboard.jpg)
</Frame>

## Connecting to the Cloud SQL Instance

To interact with your MySQL database, use Cloud Shell available directly in the GCP console.

1. **Launch Cloud Shell:** Click on **Open Cloud Shell**.

2. **Connect to the Database:** Run the following command to initiate the connection:

   ```bash theme={null}
   gcloud sql connect main-db --user=root --quiet
   ```

3. **Enable Cloud SQL Admin API:** If the connection fails because the Cloud SQL Admin API isn’t enabled, a URL will be provided. Copy and open this URL in a new browser tab to enable the API. This process may take one to two minutes.

4. **Reconnect:** After enabling the API, execute the command again:

   ```bash theme={null}
   gcloud sql connect main-db --user=root --quiet
   ```

5. **MySQL Session:** No password was set during creation, so simply press Enter when prompted. Within the MySQL session, you can run commands like:

   ```mysql theme={null}
   SHOW DATABASES;
   ```

6. **Exit MySQL:** To exit the session, type:

   ```mysql theme={null}
   quit
   ```

<Callout icon="lightbulb">
  In production applications, credentials should be securely stored and used rather than connecting manually through Cloud Shell.
</Callout>

## Disabling Delete Protection and Deleting the Instance

When you're ready to clean up, you will disable delete protection before deleting the instance.

1. **Edit the Instance:** Click on the **Edit** button for your database.
2. **Disable Delete Protection:** Locate the delete protection option and disable it, then save your changes.

<Frame>
  ![The image shows a Google Cloud SQL configuration page for editing a database instance, with options for deletion protection, maintenance, and a summary of the instance's specifications.](https://kodekloud.com/kk-media/image/upload/v1752875224/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Database-demo/google-cloud-sql-instance-config.jpg)
</Frame>

3. **Review Maintenance Settings (Optional):** You may review and adjust maintenance windows by scrolling to the maintenance section. Configure a preferred maintenance window (e.g., Sunday) and set its duration.

<Frame>
  ![The image shows a Google Cloud SQL interface for editing a database instance, with maintenance settings on the left and a summary of instance details on the right.](https://kodekloud.com/kk-media/image/upload/v1752875225/notes-assets/images/GCP-Cloud-Digital-Leader-Certification-Demo-Database-demo/google-cloud-sql-database-interface.jpg)
</Frame>

4. **Delete the Instance:** Return to the main database page, click **Delete**, confirm the database name, and proceed. Deletion typically takes about two to three minutes.

## Summary

In this lesson, you learned how to:

* Spin up a Cloud SQL database on Google Cloud Platform.
* Connect to the database using Cloud Shell.
* Configure key features such as automated backups, high availability, and maintenance windows.
* Disable delete protection and safely delete the database instance.

Thank you for following along with this demo lesson on managing cloud databases with GCP. For further reading, check out the [Kubernetes Documentation](https://kubernetes.io/docs/) and [Docker Hub](https://hub.docker.com/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gcp-cloud-digital-leader-certification/module/8bcad91c-3036-4438-ae54-6ad95434bbeb/lesson/057c3706-726f-48c6-96bc-8247e42f5503" />
</CardGroup>
