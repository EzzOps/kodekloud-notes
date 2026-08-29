# Configuring General Settings

Source: https://notes.kodekloud.com/docs/AZ-204-Developing-Solutions-for-Microsoft-Azure/Configuring-Web-App-Settings/Configuring-General-Settings/page

Guidance for configuring Azure App Service General Settings including runtime stack, platform behavior, debugging, and client certificate options to optimize compatibility, performance, and security

In this lesson we cover the General Settings for an Azure App Service (web app). These settings control the app's runtime stack, host platform behavior, debugging options, and client-certificate handling. Correct configuration improves compatibility, performance, and security for your application.

## Overview

General Settings are grouped into four main areas:

* Stack settings — choose language/framework and runtime version.
* Platform settings — host OS bitness, pipeline model (Windows), publishing methods, HTTP version, WebSockets, Always On, session affinity, TLS/HTTPS, and related proxies.
* Debugging — enable remote debugging for supported runtimes.
* Incoming client certificates — configure mutual TLS (mTLS) behavior.

Use the following quick reference table to decide which area to change for common needs:

| Setting area                 | Purpose                                                                                      | When to change                                                                      |
| ---------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Stack settings               | Select runtime (e.g., .NET, Node.js, Python) and version                                     | When app language/version differs from current host                                 |
| Platform settings            | Control host features (bitness, HTTP version, WebSockets, FTPS, Always On, session affinity) | When dependencies, performance, or security policies require specific host behavior |
| Debugging                    | Remote debugging configuration for supported runtimes                                        | Enable only for troubleshooting or development                                      |
| Incoming client certificates | Configure client-certificate modes for mTLS                                                  | When implementing certificate-based client authentication or compliance controls    |

## Stack settings

Stack settings determine the runtime environment your app will run on (for example: .NET, ASP.NET Core, Node.js, Python, PHP) and the specific version of that runtime. Select the stack and version that match what your application was developed and tested against to avoid runtime incompatibilities.

Common guidance:

* Always pin to a specific major/minor runtime you have tested (for example, Node 18.x, Python 3.10).
* For rolling security updates, evaluate using platform-managed upgrades only if your deployment and testing pipelines can tolerate changes.
* When switching stacks (e.g., from PHP to Node), verify extension and dependency compatibility, and update deployment scripts.

## Platform settings

Platform settings control how the App Service host behaves and how it handles inbound/outbound traffic. Below is a concise reference of common platform controls and recommended usage.

| Option                                 | Description                                                                     | Recommendation                                                                                  |
| -------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Bitness (32-bit / 64-bit)              | Host process architecture — affects memory availability and native dependencies | Use 64-bit for memory-heavy apps or native 64-bit libs; use 32-bit only for legacy dependencies |
| Managed pipeline version (Windows/IIS) | Integrated or Classic IIS pipeline model                                        | Use Integrated unless you have legacy dependencies on Classic pipeline                          |
| SCM / Kudu / FTP publishing            | Deployment endpoints (Local Git/Kudu console, FTP/FTPS)                         | Enable Kudu for advanced deployment hooks and diagnostics; prefer FTPS over FTP                 |
| FTPS Only                              | Enforce encrypted file transfers                                                | Enable FTPS-only to protect credentials and payloads                                            |

> **lightbulb** Use FTPS-only whenever possible to prevent credentials and payloads from being sent in clear text.

\| HTTP version | HTTP/1.1 or HTTP/2 for client-facing connections | Use HTTP/2 for modern clients to gain multiplexing and performance benefits when supported |
\| HTTP/2 proxy | Forward HTTP/2 traffic to the worker (useful for gRPC) | Enable when your app or framework supports HTTP/2 semantics (gRPC, server push) |
\| WebSockets | Persistent, bi-directional connections for real-time apps | Enable for chat, live updates, or other real-time features |
\| Always On | Prevents the app from unloading due to inactivity | Enable for APIs, background jobs, or apps that must respond immediately |
\| Session Affinity (ARR Affinity) | Sticky sessions via Azure cookie | Enable if your app stores in-memory session state; disable if your app is stateless and needs even load distribution |
\| HTTPS Only | Redirect all traffic to HTTPS | Enable to require encrypted transport for all requests |
\| Minimum TLS version | Enforce minimal TLS protocol (e.g., TLS 1.2) | Set to TLS 1.2 or higher to comply with modern security standards |

Practical notes:

* FTPS-only and HTTPS-only reduce exposure to plaintext protocols.
* Enabling Always On increases resource usage but reduces cold-start latency.
* Session affinity helps legacy stateful apps but can reduce effective load balancing.

## Debugging

Azure App Service supports remote debugging for several runtimes:

* ASP.NET / ASP.NET Core — remote debugging with Visual Studio; choose the matching Visual Studio version.
* Node.js — remote debugging support for specific Node versions and tooling (inspect protocol).

Security and performance notes:

* Remote debugging can expose sensitive information and may impact performance. Enable it only while actively debugging and disable it in production when not required.
* Use role-based access control to restrict who can enable remote debugging.

Recommended links:

* Visual Studio remote debugging: [https://learn.microsoft.com/visualstudio/debugger/remote-debugging](https://learn.microsoft.com/visualstudio/debugger/remote-debugging)
* App Service remote debugging: [https://learn.microsoft.com/azure/app-service/containers/app-service-linux-remote-debugging](https://learn.microsoft.com/azure/app-service/containers/app-service-linux-remote-debugging) (and the equivalent for Windows)

## Incoming client certificates

Incoming client certificates are used to enforce mutual TLS (mTLS): the client presents a certificate during the TLS handshake and the server validates it before allowing access.

Modes you will typically see:

* Ignore — App Service does not request or validate client certificates.
* Allow (optional) — App Service requests a client certificate but allows access without one; your app can read certificate details if provided.
* Require — The client must present a valid certificate to establish a connection.

When enabled, App Service forwards client certificate data to your application (commonly via the X-ARR-ClientCert header). Your application is responsible for validating the certificate chain and applying authorization logic.

> **warning** Requiring client certificates will block clients that do not present a valid certificate. Use this only when client certificates are part of your authentication model or compliance requirements.

Implementation tips:

* If using Allow or Require, implement server-side validation (certificate chain, revocation, subject/issuer checks).
* For APIs, document certificate pinning and rotation procedures for clients.
* Test clients across environments (dev/staging/prod) to ensure certificate trust is configured correctly.

## Putting it into practice — Azure Portal walkthrough

You configure these settings in the Azure portal under your App Service → Configuration → General settings. Here’s the typical order and what you’ll see:

1. Stack settings
   * Runtime stack dropdown (e.g., .NET, Node, PHP, Python) and version selector. Pick the exact runtime you tested against.

2. Platform settings
   * Platform architecture: 32-bit or 64-bit.
   * Managed pipeline version (Windows/IIS apps): Integrated or Classic.
   * SCM (Kudu) and FTP toggles: enable/disable publishing endpoints.
   * FTPS Only toggle: enable to enforce encrypted file transfer.
   * HTTP version: select HTTP/1.1 or HTTP/2.
   * HTTP/2 proxy: enable to forward HTTP/2 traffic to the worker (useful for gRPC).
   * WebSockets: enable for persistent client-server connections.
   * Always On: enable to avoid idle unloads (recommended for APIs/background jobs).
   * Session Affinity: enable ARR affinity if your app requires sticky sessions.
   * HTTPS Only: enforce HTTPS redirection.
   * Minimum TLS Version: select the minimum allowed TLS version for inbound connections.

3. Debugging
   * Remote debugging toggle(s) and Visual Studio / Node target version selection.

4. Incoming client certificates
   * Set client certificate mode to Ignore / Allow / Require and implement certificate validation in your app when using Allow/Require.

Quick checklist before applying changes:

* Confirm your app’s runtime and dependencies are compatible with the selected stack and bitness.
* Review the impact of Always On and session affinity on scaling and cost.
* Verify FTP/SCM decisions align with deployment and security policies (prefer Kudu and FTPS).
* Restrict remote debugging to trusted users and time windows.
* If enabling client certificates, ensure certificate trust chains and revocation checks are properly configured.

## Links and references

* App Service configuration (Azure): [https://learn.microsoft.com/azure/app-service/configure-common](https://learn.microsoft.com/azure/app-service/configure-common)
* App Service TLS/SSL settings: [https://learn.microsoft.com/azure/app-service/configure-ssl-bindings](https://learn.microsoft.com/azure/app-service/configure-ssl-bindings)
* Kudu (SCM) documentation: [https://github.com/projectkudu/kudu/wiki](https://github.com/projectkudu/kudu/wiki)
* gRPC on Azure App Service and HTTP/2: [https://learn.microsoft.com/azure/architecture/grpc](https://learn.microsoft.com/azure/architecture/grpc)
* Remote debugging Visual Studio: [https://learn.microsoft.com/visualstudio/debugger/remote-debugging](https://learn.microsoft.com/visualstudio/debugger/remote-debugging)

By understanding and correctly configuring these General Settings, you can tailor an Azure App Service host for optimal compatibility, performance, and security for your application.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-204-developing-solutions-for-microsoft-azure/module/874e2f85-3b70-421e-94c6-722d572e440f/lesson/b5714b75-e2a6-4c2a-9443-7e93e8f8f485)
