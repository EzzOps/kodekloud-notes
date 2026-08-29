# What is a Webhook

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Networking/What-is-a-Webhook/page

Explains webhooks versus polling, how webhooks work, security, retries, and implementation best practices for real time event notifications between applications.

How can one application learn about events that happen inside another application as soon as they occur?

A common scenario is handling a payment: you pay via a payment provider (for example Stripe) and your application needs to know the moment that payment is confirmed. There are two main approaches to solve this: polling and webhooks.

<Frame>
  <img alt="The image illustrates a concept of communication between two applications: &#x22;Your App&#x22; and a &#x22;Payment Co.&#x22; app, questioning how one app finds out about actions in the other." />
</Frame>

## Polling: the obvious but inefficient approach

With polling, your app repeatedly asks the other service, “Has the payment completed yet?” at a fixed interval (every few seconds or minutes).

This works, but it wastes bandwidth and server resources and introduces latency between the actual event and when your app learns about it.

<Frame>
  <img alt="The image illustrates a polling process between &#x22;Your App&#x22; and a &#x22;Payment Co.&#x22; system, questioning whether a payment is completed." />
</Frame>

## Webhooks: flip the direction of communication

A webhook reverses the flow: instead of your app asking, the other service calls your application when the event happens. You give the external service a publicly reachable callback URL on your server (for example `https://xyz.com/payment-done`). When the payment settles, the payment provider sends an HTTP request to that URL.

<Frame>
  <img alt="The image illustrates a webhook connection between &#x22;Your App&#x22; and &#x22;Payment Co,&#x22; with the text, &#x22;They call you the moment it happens.&#x22;" />
</Frame>

A webhook is a standard HTTP request. Typical payload example:

```http theme={null}
POST /payment-done HTTP/1.1
Host: xyz.com
Content-Type: application/json

{
  "event": "payment_succeeded",
  "order": 1234,
  "amount": 40
}
```

Your endpoint should acknowledge the delivery quickly by returning an HTTP 200 OK (or another success status depending on the provider):

```http theme={null}
HTTP/1.1 200 OK
Content-Type: text/plain

OK
```

Most webhook providers implement retry policies: if your server is down or returns an error, they will retry delivery a number of times. Retry specifics vary by provider, so review the provider documentation.

> **lightbulb** Your webhook endpoint must be reachable from the public internet. During development you can expose a local server using a tunneling tool (for example, [`ngrok`](https://ngrok.com)) so the provider can reach your callback URL.

## Securing webhooks

Because the endpoint is public, anyone can try to send forged requests. Providers mitigate this by signing webhook requests using a shared secret. Your server should verify the signature before processing the payload.

A common pattern is an HMAC signature included in a header (for example `X-Webhook-Signature`), computed over the raw request body using a shared secret and a secure hash function (such as SHA-256). Example verification in Python:

```python theme={null}
import hmac
import hashlib

payload = b'{"event":"payment_succeeded","order":1234,"amount":40}'
secret = b'my_signing_secret'
sig_header = "sha256=..."  # value from the X-Webhook-Signature header

expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
