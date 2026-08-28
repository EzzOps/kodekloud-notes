# Signing in and seeing the visuals

Source: https://notes.kodekloud.com/docs/Jenkins/Exploring-the-Jenkins-UI/Signing-in-and-seeing-the-visuals/page

This article provides an overview of the Jenkins dashboard and its key components for managing CI/CD processes.

In this article, we take an in-depth look at the Jenkins dashboard and explore its key components. This guide will help you navigate through the various options available, making it easier to manage your continuous integration and continuous delivery (CI/CD) processes.

Let's start by examining the top section of the dashboard.

<Frame>
  ![The image shows the Jenkins dashboard, featuring options like "New Item," "Build History," and "Manage Jenkins," with sections for creating jobs and setting up distributed builds.](https://kodekloud.com/kk-media/image/upload/v1752880036/notes-assets/images/Jenkins-Signing-in-and-seeing-the-visuals/frame_20.jpg)
</Frame>

At the top-left corner, the Jenkins logo is prominently displayed. When clicked, the logo directs you to the login page if you're not yet authenticated; otherwise, it returns you to the homepage. For instance, navigating to "Manage Jenkins" and then clicking the logo will always bring you back to the main screen.

Beneath the logo lies the search bar. If you enter "manage" in this field, Jenkins promptly displays the "Manage Jenkins" option. On the other hand, a search for terms such as "people" may not return any results immediately. Although there might be a slight delay in displaying search results, the feature still efficiently guides you toward the relevant options.

<Frame>
  ![The image shows the Jenkins dashboard interface, highlighting options like "Manage Jenkins," "Configure System," and "Manage Plugins," with a security warning about using the built-in node.](https://kodekloud.com/kk-media/image/upload/v1752880038/notes-assets/images/Jenkins-Signing-in-and-seeing-the-visuals/frame_50.jpg)
</Frame>

Clicking the home icon once again confirms the navigation back to the main screen. When you click on your username, your account details are revealed. Under the "Dashboard" section in your account page, you can view information about your builds, views, credentials, and configurations associated with your account. Additionally, a logout option is provided, which returns you to the welcome page when used. You can sign back in anytime to continue your session.

<Frame>
  ![The image shows a Jenkins dashboard displaying user information, including a user named "mike" with no recent commit activity.](https://kodekloud.com/kk-media/image/upload/v1752880039/notes-assets/images/Jenkins-Signing-in-and-seeing-the-visuals/frame_80.jpg)
</Frame>

## Navigating the Left Sidebar

The left sidebar is a central hub for Jenkins navigation. Below is a breakdown of its primary options:

1. **New Item:**\
   This menu option is the starting point of your CI/CD process. By selecting "New Item," you can create various types of jobs for your projects.

<Frame>
  ![The image shows a Jenkins interface for creating a new item, offering options like Freestyle project, Pipeline, Multi-configuration project, Folder, and Multibranch Pipeline.](https://kodekloud.com/kk-media/image/upload/v1752880040/notes-assets/images/Jenkins-Signing-in-and-seeing-the-visuals/frame_120.jpg)
</Frame>

2. **People:**\
   Manage users and perform actions like creating new user accounts.

3. **Build History:**\
   This section keeps a record of your build history, which is particularly useful when working with Jenkins pipelines.

<Frame>
  ![The image shows a Jenkins dashboard with a "Build History" section, navigation menu, and build queue status indicating no builds in progress.](https://kodekloud.com/kk-media/image/upload/v1752880041/notes-assets/images/Jenkins-Signing-in-and-seeing-the-visuals/frame_140.jpg)
</Frame>

4. **Manage Jenkins:**\
   Access system configurations, security settings, plugin management, and troubleshooting tools from here.

<Frame>
  ![The image shows the "Manage Jenkins" dashboard, featuring options for system configuration, security, and plugin management, with a sidebar for navigation.](https://kodekloud.com/kk-media/image/upload/v1752880043/notes-assets/images/Jenkins-Signing-in-and-seeing-the-visuals/frame_150.jpg)
</Frame>

This section also displays status information and offers a selection of tools to help trace and resolve configuration issues.

<Frame>
  ![The image shows a Jenkins dashboard with options for troubleshooting and tools, including managing old data, reloading configurations, and using the Jenkins CLI.](https://kodekloud.com/kk-media/image/upload/v1752880044/notes-assets/images/Jenkins-Signing-in-and-seeing-the-visuals/frame_160.jpg)
</Frame>

5. **Views:**\
   Customize how your jobs are displayed. Whether you prefer a simple list format or an automatic display of all your accessible jobs, Jenkins gives you the flexibility to create and manage various views.

<Frame>
  ![The image shows a Jenkins dashboard interface with options to create a new view, including "List View" and "My View," and a sidebar menu.](https://kodekloud.com/kk-media/image/upload/v1752880045/notes-assets/images/Jenkins-Signing-in-and-seeing-the-visuals/frame_190.jpg)
</Frame>

## Additional Dashboard Elements

Scrolling down further, you'll observe the following dashboard components:

* **Build Queue:**\
  This area shows the queue of jobs waiting to be executed.

* **Build Executor Status:**\
  Monitor the status of active jobs and see which executors are currently running builds.

* **Footer Information:**\
  At the bottom of the dashboard, you'll find the Jenkins version along with a link to the REST API. The API provides comprehensive information about Jenkins' configuration and system details.

This comprehensive overview of the Jenkins dashboard highlights its key components and navigation features. In future sections, we will delve deeper into each area for a more detailed exploration.

<Callout icon="lightbulb">
  For enhanced clarity, consider adding a description to your Jenkins projects. A brief description can help you and your team quickly understand the purpose and configuration of each project.
</Callout>

That wraps up this session. We look forward to exploring more Jenkins functionalities in the next article.

For more useful guides and tips on Jenkins, visit [Jenkins Documentation](https://www.jenkins.io/doc/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins/module/a04dd614-ac4a-452f-b42a-c7f7086c5897/lesson/83c00654-e27e-4fd5-a931-a37554148e58" />
</CardGroup>
