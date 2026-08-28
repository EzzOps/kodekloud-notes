# Compression

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Performance/Compression/page

Explains using gzip and Brotli in NGINX to compress text assets, compare algorithms, configure settings, and avoid compressing already compressed media.

Think of packing a suitcase for a week in Hawaii. If you stuff clothes without folding them, they take more space and are harder to close. Fold them neatly and you fit more. Compression does the same for data: it reduces the size of files sent over the network so they consume less bandwidth and arrive faster.

When an HTTP server compresses a response, it sends a smaller encoded version to the browser. The browser then decompresses and renders the original content. Without compression, the server sends full HTML, JavaScript, CSS, and other assets — increasing load times and data usage for end users, especially on mobile or metered connections.

<Frame>
  <img alt="An illustration labeled &#x22;Compression&#x22; showing a sanitation worker wheeling a recycling bin and carrying a trash bag. To the right, a conveyor belt feeds recyclables into a large compactor/machine marked with a recycling symbol." />
</Frame>

The end result of proper compression: less data transferred, faster page loads, and a better user experience.

<Frame>
  <img alt="An infographic titled &#x22;Fast Response&#x22; showing a server on the left sending only useful data (icons and an arrow) to a browser displayed on a laptop on the right. The components are labeled &#x22;Server&#x22; and &#x22;Browser.&#x22;" />
</Frame>

## What resources should you compress?

Text-based resources usually compress well and should be enabled for compression:

* HTML, CSS, JavaScript
* JSON, XML
* RSS, SVG, text files
* Font files (e.g., `font/woff`, `font/woff2`) — can be included selectively

Binary media and many archive formats are already compressed; recompressing them yields little benefit and wastes CPU:

* JPEG, PNG (use modern formats like WebP or AVIF instead for better compression)
* MP4, MP3, AVI, ZIP, TAR

<Frame>
  <img alt="A slide titled &#x22;Supported Compression&#x22; showing a rounded-square graphic of six file icons labeled CSS, HTML, XML, JSON, JS and JPEG, with a green checkmark indicating support." />
</Frame>

<Frame>
  <img alt="A slide titled &#x22;Unsupported Compression&#x22; showing four file icons (AVI, MP4, MP3, ZIP) inside a rounded box. A red X next to the box indicates those formats are not supported." />
</Frame>

Table — quick guidance

| Should compress                                                                          | Should generally not compress                                   |
| ---------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `text/html`, `text/css`, `application/javascript`, `application/json`, `application/xml` | `video/mp4`, `audio/mpeg`, `application/zip`                    |
| `text/plain`, `application/rss+xml`, `image/svg+xml`                                     | Already compressed images (JPEG/PNG) — prefer WebP/AVIF instead |

## Supported algorithms in NGINX

NGINX supports two widely used compression algorithms: gzip and Brotli.

### gzip

* Widely supported across browsers and servers (legacy compatibility).
* Compression levels 1–9 (1 = fastest, 9 = best compression, default commonly 6).
* Available as a built-in NGINX feature on most distributions.

<Frame>
  <img alt="A slide about Gzip showing an icon and brief facts (released in the 90s, .gz file format, available on Linux/Unix, use the gzip CLI). It also shows a compression-level scale from 1 to 9 with 6 marked as the default." />
</Frame>

Example: compress a file using the gzip CLI

```bash theme={null}
$ gzip ubuntu-jammy-jellyfish.iso
$ ls -l
-rw-r--r-- 1 user user  10G Jun 20 12:00 ubuntu-jammy-jellyfish.iso.gz
```

Recommended minimal nginx.conf gzip configuration (place inside the `http { ... }` block, often in `/etc/nginx/nginx.conf`):

```nginx theme={null}
http {
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types
        text/plain
        text/css
        text/html
        text/xml
        text/javascript
        application/json
        application/javascript
        application/rss+xml;
}
```

Notes:

* `gzip on;` — enable gzip compression.
* `gzip_comp_level` — set CPU vs. compression trade-off (1–9). Level 6 is a sensible default.
* `gzip_types` — list MIME types to compress (add `font/woff` and `font/woff2` if desired).
* `gzip_proxied any;` — allows compression for proxied requests.

### Brotli

* Better compression ratios in many cases (levels 0–11).
* Modern browsers advertise Brotli via `br` in `Accept-Encoding`.
* Not always built into stock NGINX; often provided via the third-party ngx\_brotli module or available in vendor packages.

<Frame>
  <img alt="A presentation slide titled &#x22;Brotli - Nginx Plus&#x22; showing the Brotli logo with the words &#x22;brotli&#x22; and &#x22;Debian/Ubuntu&#x22; beside it. The slide also has a small &#x22;© Copyright KodeKloud&#x22; note in the corner." />
</Frame>

Brotli is commonly added to open-source NGINX via the ngx\_brotli module. See the module repository for installation options and instructions:

* ngx\_brotli: [https://github.com/google/ngx\_brotli](https://github.com/google/ngx_brotli)

Comparison (gzip vs Brotli)

| Feature               | gzip      | Brotli                          |
| --------------------- | --------- | ------------------------------- |
| Browser support       | Universal | Modern browsers (`br`)          |
| Compression levels    | 1–9       | 0–11                            |
| Typical ratio         | Good      | Often better than gzip          |
| CPU cost              | Moderate  | Can be higher at top levels     |
| Availability in NGINX | Built-in  | Requires module or vendor build |

If you decide to build NGINX from source to include third-party modules (e.g., Brotli), the typical sequence is:

```bash theme={null}
