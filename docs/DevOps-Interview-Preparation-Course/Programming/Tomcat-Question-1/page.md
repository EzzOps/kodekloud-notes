# CPU times
print(psutil.cpu_times())

# Average CPU load
print(psutil.getloadavg())

# Virtual memory
print(psutil.virtual_memory())

# Swap memory
print(psutil.swap_memory())

# Disk usage of the root directory
print(psutil.disk_usage('/'))

# Disk I/O counters (overall, not per disk)
print(psutil.disk_io_counters(perdisk=False))

# Temperature sensors (if available)
print(psutil.sensors_temperatures())
```

When executed on your Linux server, this script outputs detailed monitoring data that can be analyzed further or sent to a centralized system for continuous tracking and alerting.

## Interview Strategy

During an interview, if asked how you would monitor an on-premises Linux server, you might respond with the following explanation:

"I would implement a Python-based monitoring solution, leveraging the psutil module to extract essential system metrics. This script provides critical insights into CPU performance, memory usage, disk activity, and temperature sensors. It serves as a blueprint that can be enhanced to forward data to a centralized monitoring dashboard for extensive analysis and alerting."

<Callout icon="lightbulb">
  Detailing your approach clearly not only demonstrates your technical expertise but also your practical problem-solving skills.
</Callout>

Thank you for reading this article. I hope you find this guide on using Python for server monitoring insightful. Stay tuned for more DevOps strategies and tips in our upcoming articles.

For more information on server monitoring and DevOps practices, explore our additional resources and documentation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-preparation-course/module/5e7996c8-ac3e-49b6-bfce-717b5a2ff2d3/lesson/6b048bf8-3b48-4bcd-a87c-c38866a1dd1e" />
</CardGroup>


# Tomcat Question 1

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Preparation-Course/Programming/Tomcat-Question-1/page

This article discusses a common Tomcat interview question and provides insights based on real-world DevOps experience.

In this article, we discuss a frequently encountered interview question in the Tomcat domain and provide a thoughtful answer based on real-world DevOps experience.

The interview question is: "Are you supporting any applications, and if so, which application server are you using?" As a DevOps engineer, automation is at the core of your daily tasks. However, it's equally important to consider the audience for your automation efforts—whether they are developers, application teams, or another group. This question aims to gauge your hands-on familiarity with various application servers.

Application servers play a crucial role, ensuring that once code is deployed, the application runs as expected. The diagram below illustrates the role of a DevOps engineer in managing multiple application servers for Java, Node.js, and Python:

<Frame>
  ![The image contains text about the role of a DevOps engineer in supporting applications, listing various application servers for Java, NodeJS, and Python, such as Tomcat, JBoss, and Django.](https://kodekloud.com/kk-media/image/upload/v1752873401/notes-assets/images/DevOps-Interview-Preparation-Course-Tomcat-Question-1/devops-engineer-application-servers.jpg)
</Frame>

Before addressing the answer, let's clarify what an application server entails. For a Java project, you might use Tomcat—an open-source server known for its ease of use and broad adoption. On the other hand, projects may sometimes require JBoss or WebLogic, which are typically license-based. For Node.js environments, IIS might be utilized, while Python projects often rely on Django.

Given the diversity of application servers, interview responses may vary based on your technical expertise and the specific technology stack you work with. Here, we focus on Tomcat due to its popularity and accessibility.

Now, let’s review a sample answer that you can use during an interview:

<Frame>
  ![The image is a note about DevOps engineers supporting various applications, listing Java, NodeJS, and Python with associated servers like Tomcat, JBoss, Weblogic, and Django, with some items circled and checked.](https://kodekloud.com/kk-media/image/upload/v1752873402/notes-assets/images/DevOps-Interview-Preparation-Course-Tomcat-Question-1/devops-engineers-applications-note.jpg)
</Frame>

<Callout icon="lightbulb">
  "I currently support a team that is developing a Java application, and we are using Tomcat as our application server. This server effectively manages our web-based endpoints. Additionally, I have experience with other application servers in diverse technology stacks, such as Python's Django and Node.js environments, and I am proficient in debugging and maintaining these services when needed."
</Callout>

This answer not only emphasizes your expertise with Tomcat but also demonstrates your versatility with multiple application servers across various programming languages.

That concludes this article. Continue exploring more DevOps interview questions in our upcoming posts to further enhance your career in DevOps.

Thank you.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-preparation-course/module/5e7996c8-ac3e-49b6-bfce-717b5a2ff2d3/lesson/4fcb4187-70e8-4ec6-bc47-d742cc6f7e19" />
</CardGroup>
