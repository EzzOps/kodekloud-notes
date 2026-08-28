# Versioning Strategies Semantic Versioning Date Based Versioning

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-a-Package-Management-Strategy/Versioning-Strategies-Semantic-Versioning-Date-Based-Versioning/page

This guide compares Semantic Versioning and Date-Based Versioning in software development, highlighting their setup, advantages, and suitability for CI/CD pipelines.

In modern software development, a clear versioning strategy ensures consistency, compatibility, and traceability. This guide compares two popular approaches—[Semantic Versioning](https://semver.org/) (SemVer) and Date-Based Versioning—demonstrated with a simple .NET console application. You’ll learn how to set up each scheme, understand their advantages, and choose the best fit for your CI/CD pipeline in environments like Azure DevOps.

## Getting Started

Begin by creating a new .NET console app and setting an initial version:

```bash theme={null}
dotnet new console -n VersioningDemo
cd VersioningDemo
```

Open `Program.cs` and add a `version` field:

```csharp theme={null}
using System;

namespace VersioningDemo
{
    // Version number will be updated per strategy
    static class Program
    {
        static string version = "v0.0.0";

        static void Main(string[] args)
        {
            Console.WriteLine("Hello, Azure DevOps!");
            Console.WriteLine($"Version: {version}");
        }
    }
}
```

Run the app to verify:

```bash theme={null}
dotnet run
