# Exploring GitHub Packages

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-a-Package-Management-Strategy/Exploring-GitHub-Packages/page

This guide covers publishing a .NET class library to GitHub Packages and using it in a Blazor WebAssembly app.

GitHub Packages enables you to host and manage code dependencies alongside your repositories. In this guide, we’ll walk through publishing a .NET class library to GitHub Packages and consuming it in a Blazor WebAssembly app.

In this tutorial, you will:

1. Scaffold a .NET class library (`KodeKonvert`).
2. Configure NuGet package metadata in Visual Studio.
3. Build and pack the library.
4. Generate a GitHub Personal Access Token (PAT).
5. Register GitHub Packages as a NuGet source.
6. Push your `.nupkg` to GitHub Packages.
7. Consume the package in a new Blazor WASM project.

***

## 1. Scaffold the .NET Class Library

1. Open Visual Studio.
2. Create a new **Class Library** project.
3. Rename the project to **KodeKonvert**.
4. Target .NET 8.0 and confirm a successful build:

```bash theme={null}
dotnet build
