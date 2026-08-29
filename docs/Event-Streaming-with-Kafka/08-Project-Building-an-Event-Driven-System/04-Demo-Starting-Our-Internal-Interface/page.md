# app.py
from flask import Flask, render_template, request, redirect, url_for
from confluent_kafka import Producer
import json
import logging
import socket

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka producer configuration
# NOTE: replace the IP below with your EC2 instance's public IP and port 9092.
conf = {
    'bootstrap.servers': '54.226.13.161:9092',
    'client.id': socket.gethostname()
}

# Initialize producer instance
producer = Producer(conf)

# Delivery callback for produced messages
def delivery_callback(err, msg):
    if err:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
        logger.info(f"Message timestamp: {msg.timestamp()}")

# Sample product data shown on the UI
products = [
    {"id": 1, "name": "Toy 1", "price": 10.99, "image": "toy1.jpg"},
    {"id": 2, "name": "Toy 2", "price": 15.99, "image": "toy2.jpg"},
    {"id": 3, "name": "Toy 3", "price": 25.99, "image": "toy3.jpg"},
    {"id": 4, "name": "Toy 4", "price": 29.99, "image": "toy4.jpg"},
    {"id": 5, "name": "Toy 5", "price": 35.99, "image": "toy5.jpg"},
    {"id": 6, "name": "Toy 6", "price": 45.99, "image": "toy6.jpg"}
]

# Simple in-memory cart (for demo purposes)
cart = []

@app.route('/')
def index():
    return render_template('index.html', products=products, cart=cart)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('product_id'))
    for p in products:
        if p['id'] == product_id:
            cart.append(p.copy())
            break
    return redirect(url_for('index'))

@app.route('/view_cart')
def view_cart():
    return render_template('cart.html', cart=cart)

@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        name = request.form.get('name')
        address = request.form.get('address')

        # Prepare the order event payload
        order_event = {
            "customer_name": name,
            "delivery_address": address,
            "products": cart,
            "total_amount": sum(item["price"] for item in cart)
        }

        # Convert event to JSON string and produce to Kafka
        event_string = json.dumps(order_event)
        logger.info(f"Sending order event to Kafka: {event_string}")

        producer.produce(
            topic='cartevent',
            value=event_string.encode('utf-8'),
            callback=delivery_callback
        )

        # Ensure all messages are delivered before proceeding
        producer.flush()

        # Clear cart after successful placement
        cart.clear()

        return render_template('order.html', name=name)
    except Exception as e:
        logger.error(f"Failed to process order: {e}")
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
```

> **lightbulb** Be sure to replace `54.226.13.161:9092` in the `bootstrap.servers` configuration with the public IP of your Kafka [Amazon Elastic Compute Cloud (EC2)](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) instance and the correct port. If broker is not reachable, the producer will fail to connect.

## Updating the bootstrap server

If your frontend cannot connect to Kafka, confirm the `bootstrap.servers` setting in `app.py` uses the EC2 instance's public IPv4 address and the Kafka listener port (default 9092). You can copy the public IP from the EC2 console and update the configuration accordingly.

<Frame>
  <img alt="The image shows the AWS EC2 management console with an instance named &#x22;kafka_demo&#x22; that is currently running. The instance details include its instance ID, type, public IPv4 address, and other network information." />
</Frame>

## Running the frontend and placing an order

Start the Flask app:

```bash theme={null}
python3 app.py
```

Open the Toy Shop in a browser ([http://localhost:5000](http://localhost:5000) if running locally). The UI shows a list of products. Add a couple of toys to the cart, view the cart, fill in name and address, and click Place Order. The app prepares an order object, serializes it to JSON, and produces it to the `cartevent` topic.

<Frame>
  <img alt="The image shows a webpage for &#x22;KodeKloud Toy Shop&#x22; displaying six toys with their prices and an option to add them to the cart." />
</Frame>

After placing the order you should see a confirmation page:

<Frame>
  <img alt="The image shows an order confirmation page thanking a user named Raghu, with a link to return to the shop." />
</Frame>

## Checking the application logs

The Flask app logs HTTP requests as well as producer activity. If message delivery succeeds, the delivery callback logs the metadata (topic, partition, offset, timestamp). Example local logs:

```plaintext theme={null}
INFO:werkzeug:127.0.0.1 - - [03/May/2025 10:08:31] "GET / HTTP/1.1" 200 --
INFO:werkzeug:127.0.0.1 - - [03/May/2025 10:09:26] "POST /place_order HTTP/1.1" 200 --
INFO:root:Sending order event to Kafka: {"customer_name": "Raghu", "delivery_address": "Delhi", "products": [...], "total_amount": 26.98}
INFO:root:Message delivered to cartevent [0] at offset 12
```

## Consuming messages on the Kafka broker

On the Kafka EC2 instance you can create the `cartevent` topic (if not already created) and consume messages to verify they were produced by the frontend.

```sh theme={null}
# Create topic (run on the Kafka server)
bin/kafka-topics.sh --create --topic cartevent --bootstrap-server 54.226.13.161:9092 --partitions 3 --replication-factor 1

# Consume messages from the beginning
bin/kafka-console-consumer.sh --bootstrap-server 54.226.13.161:9092 --topic cartevent --from-beginning
```

Example consumer output showing two orders placed from the frontend:

```plaintext theme={null}
{"customer_name": "Raghu", "delivery_address": "Delhi", "products":[{"id": 1, "name": "Toy 1", "price": 10.99, "image": "toy1.jpg"}, {"id": 2, "name": "Toy 2", "price": 15.99, "image": "toy2.jpg"}], "total_amount": 26.98}
{"customer_name": "Bob", "delivery_address": "Paris", "products": [{"id": 6, "name": "Toy 6", "price": 35.99, "image": "toy6.jpg"}], "total_amount": 35.99}
```

## Next steps

With the Toy Shop producing order events to the `cartevent` topic, a logical next step is to implement the Warehouse UI (an internal consumer dashboard). That dashboard can consume `cartevent` messages and present orders to warehouse staff for picking, packing, and shipping.

## Links and references

* [Kafka Documentation](https://kafka.apache.org/documentation/)
* [Confluent Python Client (confluent-kafka)](https://github.com/confluentinc/confluent-kafka-python)
* [Amazon EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/95f49caf-8e0b-4ed9-b7dd-9f43ff31ed9a/lesson/4eeb78bb-a67b-4178-8964-28da52079754)


# Demo Starting Our Internal Interface

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Project-Building-an-Event-Driven-System/Demo-Starting-Our-Internal-Interface/page

Setting up a warehouse backend UI that consumes front-end order events from Kafka, configures a consumer, and demonstrates running and testing the packer dashboard.

Welcome back. In this lesson we start the warehouse backend UI (the internal web interface) and connect it to the Kafka topic that receives cart/order events. The backend consumes events produced by the front-end and renders them for warehouse packers.

Below we walk through the key producer behavior from the frontend, how the warehouse app consumes those events, sample logs, the consumer implementation used by the UI, and how to run and test the dashboard end-to-end.

## Producer: front-end order event (context)

When an order is placed in the front-end, the app produces an order event to Kafka. The producer code looks like this:

```python theme={null}
