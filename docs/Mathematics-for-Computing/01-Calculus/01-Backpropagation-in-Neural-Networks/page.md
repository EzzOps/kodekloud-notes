# Backpropagation in Neural Networks

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Calculus/Backpropagation-in-Neural-Networks/page

Explains backpropagation, the chain rule, and gradient descent using a numeric Netflix recommendation example to compute gradients and update neural network weights.

Welcome — Alan Chapman from KodeKloud.

In this lesson we unpack how neural networks learn from their mistakes using the chain rule and gradient descent. You’ll see a concrete, step-by-step example that connects calculus (derivatives) to the weight updates that improve predictions.

<Frame>
  <img alt="The image features a woman presenting with the text &#x22;Mathematics for Computing&#x22; and &#x22;Backpropagation and Chain Rule&#x22; on a purple background with a dotted pattern." />
</Frame>

Overview

* Backpropagation: the algorithm for computing gradients of the loss w\.r.t. each weight by propagating error backward through the network.
* Chain rule: the calculus tool that decomposes derivatives of composite functions into products of simpler derivatives.
* Gradient descent: the optimization step that uses gradients to update weights and reduce error.

Why this matters (real-world intuition): recommendations (e.g., Netflix) rely on models that continuously adjust internal weights as they observe user interactions — the same calculus principles power that adaptation.

<Frame>
  <img alt="The image features a list of three topics about neural networks and prediction, alongside a cartoon dog and a person wearing a &#x22;KodeKloud&#x22; shirt." />
</Frame>

Example: How Netflix learns your taste
When you first sign up, recommendations are noisy. As you interact (watch, rate, skip), the system computes prediction errors and adjusts its parameters so future suggestions better match your preferences.

<Frame>
  <img alt="The image shows a woman standing next to a screen displaying a Netflix interface with various TV shows and movies. The text &#x22;How does Netflix know?&#x22; is written on the top left." />
</Frame>

Neural network anatomy (simple)

* Input layer: receives features (e.g., encoded genre, setting).
* Hidden layer(s): transform inputs and extract patterns.
* Output layer: yields final prediction (e.g., probability of watching a suggested show).
* Weights: connections between nodes that determine importance of each input.

Table — Common components and purpose

| Component     | Purpose                            | Example                                |
| ------------- | ---------------------------------- | -------------------------------------- |
| Input layer   | Accepts feature values             | `genre`, `setting`                     |
| Hidden layer  | Learns intermediate features       | single neuron for illustration         |
| Output layer  | Produces probability or label      | probability of watching "Heartstopper" |
| Weights       | Parameters updated during training | `w1`, `w2`                             |
| Loss function | Measures prediction error          | `0.5*(y - t)^2`                        |

<Frame>
  <img alt="The image shows a diagram of a neural network with input, hidden, and output layers, illustrating the process from &#x22;Watched Show&#x22; to &#x22;Recommends Show.&#x22; A person is standing beside the diagram, explaining it." />
</Frame>

Roles typically involved in building recommendation systems

* Machine learning engineers: implement and train models.
* Data scientists: analyze and prepare feature data.
* AI researchers: design novel architectures and optimization techniques.
* Software engineers (AI-focused): integrate models into products.

Table — Roles and responsibilities

| Role                      | Typical responsibilities          |
| ------------------------- | --------------------------------- |
| Machine learning engineer | Train, validate, deploy models    |
| Data scientist            | Feature engineering, experiments  |
| AI researcher             | New algorithms, theoretical work  |
| Software engineer (AI)    | Product integration, latency/perf |

Simplifying to a tiny model
We’ll analyze a toy network with:

* Two inputs: x1 (genre), x2 (setting)
* One hidden neuron (for clarity) and a sigmoid activation at the output
* Output y = sigmoid(s), where s = x1*w1 + x2*w2

<Frame>
  <img alt="The image illustrates a neural network process for Netflix recommendations, showing stages from watched shows to recommendation and backpropagation. A person stands on the right, wearing a &#x22;KodeKloud&#x22; t-shirt." />
</Frame>

Notation and forward pass

* Inputs: x1, x2
* Weights: w1, w2
* Weighted sum: s = x1*w1 + x2*w2
* Activation (sigmoid): y = sigmoid(s) = 1 / (1 + exp(-s))

<Frame>
  <img alt="The image illustrates a neural network model for Netflix recommendations, showing inputs as genre and setting, a hidden layer, and outputs with TV show examples. A person is explaining the concept alongside a cartoon cat asking a question about hidden layers." />
</Frame>

Concrete numeric example (step-by-step)
Given:

* x1 = 4.0 (encoded genre)
* x2 = 2.0 (encoded setting)
* initial weights: w1 = 0.2, w2 = 0.6

Compute s and y:

```python theme={null}
