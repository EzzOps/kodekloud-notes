# Demo Configure Multiple Sites

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Intermediate-Config/Demo-Configure-Multiple-Sites/page

How to configure Nginx host based virtual hosting to serve multiple websites, create site configs, enable sites, and test using curl with custom Host headers

In this lesson you'll configure Nginx to host two different websites on the same server using host-based virtual hosting. Nginx inspects the HTTP `Host` header and routes requests to the matching `server` block (site). We'll create two site configs (example1 and example2), enable them, and test using `curl` with a custom `Host` header.

<Frame>
  <img alt="A presentation slide that reads &#x22;Configure Multiple Sites&#x22; on the left and shows a teal gradient shape on the right with the word &#x22;Demo.&#x22; The bottom-left corner includes &#x22;© Copyright KodeKloud.&#x22;" />
</Frame>

## Overview

* Client (browser or `curl`) sends an HTTP request to the server.
* Nginx reads the `Host` header and selects the `server` block with a matching `server_name`.
* If no match is found, Nginx serves the default server for that address/port (the first matching server block).

## Initial state — remove the default site

Remove the default site so it doesn't interfere with our example sites, then reload Nginx:

```bash theme={null}
