# HTTPS

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Security/HTTPS/page

Explains HTTPS/TLS, certificate authorities, obtaining and using certificates with Certbot or mkcert, and configuring Nginx to serve secure HTTPS for production and local development.

In this lesson you’ll learn what HTTPS is, why it matters, how TLS certificates work, and how to obtain and use them with a web server. The Nginx server block shown later demonstrates how to wire a certificate into a production-style configuration.

Why HTTPS matters

* Security: HTTPS (TLS) encrypts the entire communication channel between browser and website. On a shared network (e.g., public Wi‑Fi) an attacker cannot read intercepted traffic without access to the server’s private key. HTTPS protects usernames, passwords, payment data, and other sensitive information.
* SEO and trust: Modern search engines and browsers favor HTTPS. A secure site can rank better in search results and displays browser UI (padlock) that increases user trust.

<Frame>
  <img alt="An illustrated slide titled &#x22;Importance of HTTPS&#x22; showing people in a coffee shop using laptops and Wi‑Fi, with a padlock icon and dotted lines depicting a secure (HTTPS) connection." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Importance of HTTPS&#x22; showing an https:// lock icon labeled &#x22;SEO Benefits.&#x22; Below it are icons and captions indicating HTTPS protects customer data and boosts visibility in search engines." />
</Frame>

SSL vs TLS

* SSL (Secure Sockets Layer) is deprecated. TLS (Transport Layer Security) is the modern, secure protocol that replaced SSL.
* People still say “SSL certificate,” but the protocol in use is TLS. Use TLS 1.2 or TLS 1.3; TLS 1.0 and 1.1 (and all SSL versions) are insecure and should be disabled.

<Frame>
  <img alt="A simple diagram titled &#x22;SSL and TLS&#x22; showing a browser icon on the left and a web server stack on the right, connected under a shield with a checkmark. The caption says the protocols ensure privacy and integrity between browser and server." />
</Frame>

High-level TLS handshake (simplified)

1. The browser opens an HTTPS connection to the server.
2. The server sends its TLS certificate (an X.509 document signed by a Certificate Authority). The certificate includes the server’s public key and identifying information (domain name).
3. The browser validates the certificate (chain-of-trust, expiration, and domain name). If valid, the browser and server complete an authenticated key exchange (commonly ECDHE), which results in ephemeral symmetric session keys.
4. All subsequent traffic is encrypted using the negotiated symmetric keys for performance and confidentiality.

<Frame>
  <img alt="A simple diagram showing an SSL/TLS step where a store’s web server sends its SSL/TLS certificate to a user’s browser/payment form. It features a user icon on the left, a payment form in the center, and server racks with a certificate icon on the right." />
</Frame>

Certificate Authorities (CAs)

* CAs validate identity and digitally sign certificates so browsers can trust them.
* Examples include DigiCert, Sectigo, and other commercial CAs.
* Let’s Encrypt is a widely used free, automated CA trusted by modern browsers and suitable for production.

<Frame>
  <img alt="A presentation slide titled &#x22;Certificate Authority&#x22; that shows a company/person icon issuing a digital certificate. The certificate graphic is labeled with contents like user's name, company information, and website address, and the slide notes the CA governs and manages digital certificates." />
</Frame>

Certificates verify ownership

* A TLS certificate is effectively a website’s online ID card. It proves the certificate requester controls the domain and prevents impersonation.

<Frame>
  <img alt="A slide titled &#x22;Certificates&#x22; showing a stylized browser window with the URL https://www.onlinestore.com and an SSL certificate icon. The caption notes that a certificate verifies the domain belongs to the store, not an impostor." />
</Frame>

Public/private keys (asymmetric encryption)

* TLS uses asymmetric cryptography for authentication and key exchange: a public key (shared) and a private key (kept secret on the server).
* The public/private key pair authenticates the server and helps establish session keys; bulk encryption uses symmetric keys because symmetric algorithms are faster.

<Frame>
  <img alt="A diagram showing a web server sending a public key (depicted by an unlocked padlock) to a browser. The browser then uses that key to encrypt the data being sent." />
</Frame>

<Frame>
  <img alt="A slide titled &#x22;Private Key&#x22; showing a lock icon in a speech-bubble and a separate key icon labeled &#x22;Kept secret by the server.&#x22; It illustrates that the private key is stored confidentially on the server." />
</Frame>

Practical flow for a payment form

* After the TLS handshake, the browser encrypts sensitive form fields (e.g., credit card numbers) with the negotiated symmetric session keys.
* The server uses its private key and the session keys established during the handshake to decrypt and process the request.

<Frame>
  <img alt="A diagram illustrating how public-key encryption works in practice. It shows a browser encrypting a credit card number, sending the encrypted data to a server that decrypts it with a private key and processes the payment." />
</Frame>

Obtaining TLS certificates

* Let’s Encrypt + Certbot: Let’s Encrypt issues free, trusted certificates. Certbot is a popular, well-documented client to obtain and renew certificates automatically.
* Requirements: you must own (or control) the domain and have DNS pointing to the server where you run Certbot.

Example Certbot usage (adjust domains and plugin/flags for your environment):

```bash theme={null}
sudo apt update
sudo apt install certbot
