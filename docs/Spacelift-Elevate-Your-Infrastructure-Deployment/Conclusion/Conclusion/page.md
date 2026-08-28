# Set the mission name
mission_name=lunar-mission

# Use the variable in subsequent commands
mkdir "$mission_name"
rocket-add "$mission_name"
rocket-start-power "$mission_name"
rocket-internal-power "$mission_name"
rocket-crew-ready "$mission_name"
rocket-start-sequence "$mission_name"
rocket-start-engine "$mission_name"
rocket-lift-off "$mission_name"
rocket-status "$mission_name"
```

To change the mission, update the variable assignment at the beginning:

```bash theme={null}
mission_name=mars-mission
```

This update automatically propagates to all commands, eliminating the need for repetitive manual changes.

<Callout icon="lightbulb">
  Variable names should use only lowercase letters and underscores (e.g., `mission_name`). Avoid using hyphens or other characters, as variable names must consist solely of alphanumeric characters or underscores.
</Callout>

## Capturing Command Output in Variables

Variables in shell scripts can also store the output of commands. For instance, if the command `rocket-status` outputs a value such as "launching", "success", or "failed", you can capture that output and then display it. The following example demonstrates how to do this:

```bash theme={null}
#!/bin/bash

# Set the mission name for a different mission
mission_name=mars-mission

# Execute the series of commands for the mission
mkdir "$mission_name"
rocket-add "$mission_name"
rocket-start-power "$mission_name"
rocket-internal-power "$mission_name"
rocket-crew-ready "$mission_name"
rocket-start-sequence "$mission_name"
rocket-start-engine "$mission_name"
rocket-lift-off "$mission_name"
rocket-status "$mission_name"

# Capture the rocket status output into a variable
rocket_status=$(rocket-status "$mission_name")

# Print the status of the launch
echo "Status of launch: $rocket_status"
```

Here, the output of `rocket-status` is stored in the variable `rocket_status` using the command substitution syntax `$(...)` and then printed using the `echo` command.

## Practice Makes Perfect

Applying these concepts will help you write more robust and maintainable scripts. Try refactoring your existing scripts by replacing hardcoded values with variables to see how much easier updates become.

I look forward to seeing you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2709b373-3a6f-4b31-9aff-fe8a553898fa/lesson/c5cf2034-a087-42da-ab32-1988042eda61" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2709b373-3a6f-4b31-9aff-fe8a553898fa/lesson/cf45ee2d-0c63-4e13-95e8-47bc4ece8174" />
</CardGroup>


# Conclusion

Source: https://notes.kodekloud.com/docs/Spacelift-Elevate-Your-Infrastructure-Deployment/Conclusion/Conclusion/page

This article provides an overview of Spacelift, highlighting its features and benefits for efficient infrastructure deployment.

Throughout this article, we provided an in-depth overview of [Spacelift](https://learn.kodekloud.com/user/courses/spacelift-elevate-your-infrastructure-deployment), outlining its key features and benefits for efficient infrastructure deployment. We trust that the insights shared here will help you optimize your infrastructure management and deployment strategies.

<Callout icon="lightbulb">
  For additional resources and further learning, consider exploring related articles and official documentation on Spacelift.
</Callout>

Thank you for reading, and we look forward to bringing you more valuable content in our upcoming articles.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/spacelift-elevate-your-infrastructure-deployment/module/da592756-23c5-405c-abf3-01547572ae74/lesson/01d6256d-5550-48af-b999-1482c2344f03" />
</CardGroup>
