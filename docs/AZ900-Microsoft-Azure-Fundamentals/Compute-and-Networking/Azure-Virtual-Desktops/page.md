# Write to the Azure Functions log stream.
Write-Host "PowerShell HTTP trigger function processed a request."

# Interact with query parameters or the body of the request.
$name = $Request.Query.Name
if (-not $name) {
    $name = $Request.Body.Name
}

$body = "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."

if ($name) {
    $body = "Hello, $name. This HTTP triggered function executed successfully."
}

# Associate values to output bindings by calling 'Push-OutputBinding'.
Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
    StatusCode = [HttpStatusCode]::OK
    Body = $body
})
```

5. **Test Your Function:**\
   Click on "Get Function URL" to copy the URL, then paste it into your browser with `?Name=Sam` appended to see the message "Hello, Sam. This HTTP triggered function executed successfully." If no name is provided, the function will prompt you to pass a name.

These event-driven functions demonstrate the serverless computing model by executing code in response to specific triggers.

## Conclusion

This guide covered the fundamentals of Azure Functions, including its architecture, significant benefits, and common use cases. Additionally, you learned how to create a Function App and implement an HTTP-triggered function using the Azure Portal. Future comparisons with other Azure compute services will further enhance your understanding of how to select the best service for your application needs.

Thank you for reading!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az900-microsoft-azure-fundamentals/module/8eca3741-67ac-4ee2-8439-aa23c16d33dd/lesson/4413b2d1-c5aa-466d-8b52-dff525e8b378" />
</CardGroup>


# Azure Virtual Desktops

Source: https://notes.kodekloud.com/docs/AZ900-Microsoft-Azure-Fundamentals/Compute-and-Networking/Azure-Virtual-Desktops/page

Azure Virtual Desktop provides complete desktop environments and applications in the cloud, enabling secure remote access from various devices while adhering to corporate policies.

Azure Virtual Desktop (AVD) is a comprehensive platform that goes beyond traditional Azure Virtual Machines by delivering complete desktop environments and applications in the cloud. It provides a fully functional personal Windows PC experience that you can access from anywhere, regardless of your device.

For instance, if you need to run Power BI Desktop but are using a Mac, you can seamlessly connect to a Windows 10 desktop hosted on AVD via your company’s network. Similarly, when traveling or on vacation, you can use your tablet or any other device to remotely access your Windows 10 environment—all while adhering to corporate policies and joining the corporate domain.

## Key Features of Azure Virtual Desktop

AVD stands out with its robust capabilities:

* **Remote Access:**\
  Enjoy a full desktop experience from any location. Unlike standard Azure VMs that support only a single user at a time (forcing sign-outs for concurrent sessions), AVD enables multiple users to simultaneously access a single Windows 10 virtual machine, thus maximizing resource utilization.

* **Security and Compliance:**\
  Built upon the Azure Security Foundation, AVD offers continuously updated, integrated security measures that safeguard your data and help meet regulatory standards.

* **Flexibility, Cost-Effectiveness, and Scalability:**
  * **Flexibility:** Connect using various devices including laptops, tablets, or smartphones, empowering a mobile workforce.
  * **Cost-Effective:** Optimize expenses by leveraging existing licenses while paying solely for the resources you use.
  * **Scalability:** Scale resources dynamically to match your organization’s requirements.

<Frame>
  ![The image lists key features of Azure Virtual Desktops: Remote Access, Multi-Session Windows 10, and Security and Compliance.](https://kodekloud.com/kk-media/image/upload/v1752868288/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Virtual-Desktops/azure-virtual-desktops-features.jpg)
</Frame>

## Common Use Cases

Azure Virtual Desktop is particularly effective in scenarios like remote work and BYOD (Bring Your Own Device) policies. It enables employees to securely access corporate desktops from their personal devices while ensuring adherence to company policies and robust data security.

<Frame>
  ![The image highlights the benefits of Azure Virtual Desktops, featuring three key points: flexibility, cost-effectiveness, and scalability.](https://kodekloud.com/kk-media/image/upload/v1752868289/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Virtual-Desktops/azure-virtual-desktops-benefits.jpg)
</Frame>

AVD enforces organizational policies by granting regulated access to company data and ensuring desktops are joined to the corporate domain, making it the ideal solution for businesses aiming to support a flexible and secure workforce.

<Frame>
  ![The image illustrates common use cases for Azure Virtual Desktops, including remote work, BYOD (Bring Your Own Device), and regulated access to company data, with a diagram showing virtual machines (VM01, VM02, VM03).](https://kodekloud.com/kk-media/image/upload/v1752868290/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Virtual-Desktops/azure-virtual-desktops-use-cases.jpg)
</Frame>

## A Glimpse into the AVD Setup Process

Setting up an Azure Virtual Desktop environment involves several key components, including host pools, workspaces, and application groups. Consider the following demo scenario to understand the process:

1. **Creating a Host Pool:**\
   Begin by logging into the Azure portal to create a host pool. A host pool is a collection of virtual machines that form the backbone of AVD, delivering flexible and enhanced virtual desktops.

<Frame>
  ![The image shows the Azure Virtual Desktop interface, specifically the "Host pools" section, displaying a list of host pools with details like name, resource group, location, and subscription.](https://kodekloud.com/kk-media/image/upload/v1752868292/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Virtual-Desktops/azure-virtual-desktop-host-pools.jpg)
</Frame>

2. **Navigating the Virtual Machines Section:**\
   In the Virtual Machines section, you will notice many machines prefixed with AVD. Although these are virtual machines under the hood, they are optimized to provide a superior desktop experience.

3. **Connecting via the Remote Desktop Web Client:**\
   Users can connect to these virtual desktops using the Remote Desktop Web Client, available both as a browser-based interface and as downloadable client applications for various devices (including tablets and smartphones).

<Callout icon="lightbulb">
  When connecting through a browser, a session prompt will request permission to access local resources such as clipboard, printers, and file transfers to ensure a smooth remote experience.
</Callout>

<Frame>
  ![The image shows a browser window with the Azure Virtual Desktop interface, displaying a prompt to allow access to local resources such as clipboard, printer, and file transfer.](https://kodekloud.com/kk-media/image/upload/v1752868293/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Virtual-Desktops/azure-virtual-desktop-browser-window.jpg)
</Frame>

4. **Experiencing the Full Desktop Session:**\
   Once connected, the Windows 10 desktop session loads completely, offering familiar features such as a full-screen mode and access to essential applications like Office, OneDrive, and SharePoint.

<Frame>
  ![The image shows a Windows 10 desktop with the Start menu open, displaying various applications and a blue background with the Windows logo.](https://kodekloud.com/kk-media/image/upload/v1752868293/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Virtual-Desktops/windows-10-desktop-start-menu.jpg)
</Frame>

## Conclusion

Azure Virtual Desktop leverages the advanced capabilities and security of Azure to deliver a scalable and cost-effective cloud-based desktop solution. Its ability to provide secure remote access, optimize resource utilization, and support a flexible, mobile workforce makes it an essential tool for modern businesses.

Next, we will explore another essential Azure service: App Service.

<Frame>
  ![The image shows a Windows 10 desktop with a network discovery prompt on the right side, asking if the PC should be discoverable on the network.](https://kodekloud.com/kk-media/image/upload/v1752868294/notes-assets/images/AZ900-Microsoft-Azure-Fundamentals-Azure-Virtual-Desktops/windows-10-network-discovery-prompt.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az900-microsoft-azure-fundamentals/module/8eca3741-67ac-4ee2-8439-aa23c16d33dd/lesson/ede63003-ec63-438a-8e26-a3bf1f5a9814" />
</CardGroup>
