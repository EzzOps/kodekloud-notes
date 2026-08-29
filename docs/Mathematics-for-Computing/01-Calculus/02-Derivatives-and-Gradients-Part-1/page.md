# python
import math

x1, x2 = 4.0, 2.0
w1, w2 = 0.2, 0.6

s = x1*w1 + x2*w2  # 2.0
y = 1 / (1 + math.exp(-s))  # sigmoid(s)

s, y
```

Result: s = 2.0, y ≈ 0.8808 (an 88% predicted probability of watching "Heartstopper").

<Frame>
  <img alt="The image illustrates a neural network for Netflix recommendations, showing how genre and setting are weighted to recommend shows, with examples of &#x22;Top Boy&#x22; and &#x22;Heartstopper.&#x22; A person stands to the right explaining the concept." />
</Frame>

Backpropagation: computing gradients with the chain rule
Suppose the observed target is t = 0.65. The model overpredicted, so we compute how to change weights to reduce the error.

We want dy/dw1. Since y depends on s and s depends on w1, use the chain rule:

* dy/dw1 = (dy/ds) \* (ds/dw1)

For the sigmoid:

* dy/ds = y \* (1 - y)

From s = x1*w1 + x2*w2:

* ds/dw1 = x1

Therefore:

* dy/dw1 = x1 \* y \* (1 - y)

Calculate numerically:

```python theme={null}
# python
x1 = 4.0
s = 2.0
y = 1 / (1 + math.exp(-s))  # ≈ 0.8807970779778823

dy_ds = y * (1 - y)  # ≈ 0.1050
ds_dw1 = x1  # 4.0

dy_dw1 = dy_ds * ds_dw1  # ≈ 0.420
dy_dw1
```

So dy/dw1 ≈ 0.420: this is the sensitivity of the output to changes in w1.

Loss function and gradient for weight update
Use squared-error loss: L = 0.5 \* (y - t)^2. Then:

* dL/dy = (y - t)
* dL/dw1 = dL/dy \* dy/dw1 = (y - t) \* dy/dw1

Numerically:

* error = y - t ≈ 0.8808 - 0.65 = 0.2308
* dL/dw1 ≈ 0.2308 \* 0.420 ≈ 0.0969

Gradient descent update with learning rate alpha:

```python theme={null}
# python
alpha = 0.1
error = y - 0.65
dL_dw1 = error * dy_dw1
w1_new = w1 - alpha * dL_dw1
w1_new
```

This slightly reduces w1 because the model was overpredicting. The same approach computes dL/dw2 using ds/dw2 = x2 and updates w2 accordingly.

<Frame>
  <img alt="The image illustrates a neural network process for Netflix recommendations, showing weights and activation functions, alongside a person explaining the concept." />
</Frame>

Callout: key intuition

> **lightbulb** Backpropagation combines local derivatives: compute how a small change to a weight affects the node output, then multiply by how that output affects the loss. In practice this scales to many layers by repeatedly applying the chain rule from output back to inputs.

Practical note about training

> **warning** Choose the learning rate (`alpha`) carefully. Too large -> divergence/overshooting; too small -> very slow learning. Also, scale and normalize inputs for stable training.

Generalization to deep networks
At scale, the same pattern holds: for each weight you compute the partial derivative of the loss with respect to that weight by multiplying derivatives layer-by-layer (the chain rule). Optimizers (e.g., SGD, Adam) use these gradients to update all weights across layers.

Mathematical refresh: chain rule for composite functions
If y = 3x^2 + 1 and z = y^3 + 3, then z is a composite of x via y. By the chain rule:

* dz/dx = (dz/dy) \* (dy/dx)
* dy/dx = 6x
* dz/dy = 3y^2
* dz/dx = 3y^2 \* 6x = 18 x y^2

Replace y with (3x^2 + 1) to express dz/dx entirely in terms of x.

<Frame>
  <img alt="The image features a person presenting on the topic of composite functions, with mathematical notations for derivatives and a purple cube representing the concept visually." />
</Frame>

Bakery analogy (another chain rule example)
Let:

* y = x^3 - 2
* z = 2 - y^2

Then:

* dy/dx = 3x^2
* dz/dy = -2y
* dz/dx = dz/dy \* dy/dx = (-2y) \* (3x^2) = -6 x^2 y

Evaluate at x = 1:

* y = 1^3 - 2 = -1
* dz/dx = -6 \* 1^2 \* (-1) = 6

This means at x = 1 a small increase in x improves z (positive derivative). The same multiplication-of-derivatives logic is exactly what backpropagation uses.

<Frame>
  <img alt="The image shows a presentation slide discussing &#x22;Neural Network for Netflix Recommendation&#x22; with mathematical equations and a speaker standing on the right." />
</Frame>

Recap applied to the numeric network

* Inner function: s = x1*w1 + x2*w2
* Outer function: y = sigmoid(s)
* Chain rule: dy/dw = (dy/ds) \* (ds/dw)
* The sign and magnitude of dL/dw determine whether to increase or decrease each weight.

<Frame>
  <img alt="The image features text explaining a neural network for Netflix recommendations, with equations and a 3D purple cube in the background and a person speaking in the foreground." />
</Frame>

Summary

* Backpropagation = chain rule applied through network layers to compute gradients.
* Gradients show how each weight affects the loss; optimizers use them to update weights and reduce error.
* Repeating forward passes and backpropagation over many examples and epochs is how networks learn complex patterns.

<Frame>
  <img alt="The image features a woman standing beside a presentation slide titled &#x22;Conclusion,&#x22; which summarizes concepts such as composite functions, chain rule, and backpropagation." />
</Frame>

Further reading and references

* Chain rule (calculus): [https://en.wikipedia.org/wiki/Chain\_rule](https://en.wikipedia.org/wiki/Chain_rule)
* Backpropagation algorithm: [https://en.wikipedia.org/wiki/Backpropagation](https://en.wikipedia.org/wiki/Backpropagation)
* Introduction to neural networks and training: [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/) (Goodfellow, Bengio, Courville)

This lesson connected the chain rule to neural network training with a concrete example: small network, explicit derivatives, and a gradient descent update — the core mechanics behind large-scale recommendation systems.

- [Watch Video](https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/582ff79b-c012-496e-8612-3ed7a8df5800/lesson/ceb39c46-0b4f-4a1a-83fd-ec3bdff660a7)


# Derivatives and Gradients Part 1

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Calculus/Derivatives-and-Gradients-Part-1/page

Introductory lesson on derivatives explaining rate of change, tangents, instantaneous speed, practical applications in self driving and machine learning, and an introduction to the power rule.

Welcome — I'm Alan Chapman from KodeKloud.

In this lesson we introduce derivatives: the mathematical tool that measures change. You’ll learn an intuitive, visual interpretation of derivatives using distance–time graphs, see how derivatives quantify instantaneous rates (like speed), and discover how these ideas apply to real-world systems such as self-driving cars and image-recognition models. We also preview the power rule so you can compute derivatives algebraically.

<Frame>
  <img alt="The image features a person in a dark shirt standing next to text detailing three objectives related to derivatives, with an animated cat character on the left." />
</Frame>

Why focus on derivatives? Because analyzing how things change lets models make better decisions — from avoiding collisions in autonomous vehicles to improving image recognition. Derivatives provide the quantitative measure of that change.

<Frame>
  <img alt="The image shows a person speaking next to a graphic with three cars on lanes and the text &#x22;Derivative Means 'Rate of Change'.&#x22;" />
</Frame>

Derivatives measure rate of change. In physics, speed is the rate of change of distance with respect to time. In machine learning, derivatives (and gradients) measure how model outputs change with respect to parameters — information that optimization algorithms use to improve performance.

<Frame>
  <img alt="The image shows a presentation slide titled &#x22;Derivative in IT Jobs,&#x22; with illustrations of a &#x22;Machine Learning Engineer&#x22; and a &#x22;Data Scientist,&#x22; alongside a person giving the presentation." />
</Frame>

Self-driving cars give a concrete example. They rely on sensors and math (no instincts). To travel safely they must monitor distances, adjust speed smoothly, and stop or change lanes when necessary. Those decisions all depend on knowing how speed or distance are changing over time — exactly what derivatives tell us.

Consider this roadworks scenario: cones, a narrow lane, and a car approaching at speed. The vehicle must evaluate whether to brake, hold speed, or change lanes. To choose correctly it needs the rate at which its speed or distance to obstacles is changing — this is derivative information.

<Frame>
  <img alt="The image shows a woman speaking in front of a presentation slide about &#x22;Making Decisions&#x22; related to driving, which includes illustrations of cars, traffic cones, and questions about speed and obstacles." />
</Frame>

A simple, concrete example helps build intuition. Meet Julia.

* She travels toward the library and hits traffic.
* For the first period she moves steadily: 30 metres every 15 seconds.
* After 45 seconds she has covered 90 metres — that’s 2 metres per second.

On a distance–time graph, steady motion shows up as a straight line. The slope of that line (rise over run) equals her speed; in this case the slope is 2 m/s.

After 45 seconds Julia stops for 15 seconds, then turns back home. The distance–time graph therefore has three phases: rising (moving away), flat (stopped), and falling (returning). Each phase corresponds to a different derivative value:

* Rising straight line → positive slope → moving away.
* Horizontal line → zero slope → stopped.
* Falling line → negative slope → getting closer (negative rate).

<Frame>
  <img alt="The image shows a graph of distance versus time with a line that rises, levels, and then falls, and a person explaining the graph. There's also an animated character in a car with a speech bubble questioning the line's downward trend, suggesting reversal." />
</Frame>

Key intuition at a glance:

| Slope (tangent) | Meaning                                          |
| --------------: | ------------------------------------------------ |
|    Steep upward | Large positive rate — fast increase (high speed) |
|   Gentle upward | Small positive rate — slow increase              |
|      Horizontal | Zero rate — no change (stopped)                  |
|        Downward | Negative rate — decrease (moving toward start)   |

In the real world, motion is usually smooth rather than piecewise-linear. Julia doesn’t stop or start instantly — she accelerates and decelerates smoothly, producing a curved distance–time plot. To find her instantaneous speed at any moment on that smooth curve, we draw a tangent at the point and compute its slope. That slope is the derivative at that instant.

A tangent line gives local, instantaneous information:

* A steep tangent → high instantaneous speed.
* A flatter tangent → slower instantaneous speed.
* A horizontal tangent → zero instantaneous speed.
* A negative tangent → distance decreasing (moving back).

Self-driving systems use the same concept to estimate instantaneous velocities and make split-second decisions: should the car brake now, or is it safe to change lanes?

To understand passing an obstacle: imagine the car approaching a roadworks site. If the distance from the car to the works is plotted versus time, the graph will dip as the car approaches (negative slope) and then rise after passing (positive slope). The moment when the driver (or autopilot) begins braking is a point on that curve — the instantaneous speed there equals the tangent slope.

<Frame>
  <img alt="The image shows a graph of distance versus time with a curved line and marked &#x22;accelerate,&#x22; alongside a person smiling and a cartoon animal character. A speech bubble asks if computers draw tangents every time." />
</Frame>

> **lightbulb** Computers don’t literally draw geometric tangents each time. Instead they use algebraic formulas from calculus (and numerical methods) to compute derivatives quickly. These computations let systems evaluate rates of change in real time for control and optimization tasks.

Next step: basic algebraic differentiation. The power rule is the simplest and most commonly used formula for derivatives. It states:

```text theme={null}
If f(x) = x^n, then f'(x) = n * x^(n-1)
```

Example:

```text theme={null}
f(x) = x^3
f'(x) = 3x^2
```

Using formulas like the power rule, a program can compute instantaneous rates without geometric construction. Those computed derivatives are the building blocks for gradients, which guide optimization algorithms in machine learning.

Further reading and references:

* [Derivative — Wikipedia](https://en.wikipedia.org/wiki/Derivative)
* [Calculus basics — Khan Academy](https://www.khanacademy.org/math/calculus-1)
* [Gradient descent and optimization (overview)](https://en.wikipedia.org/wiki/Gradient_descent)

In the next lesson we'll apply the power rule and begin computing derivatives for functions that commonly appear in machine learning models.

- [Watch Video](https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/582ff79b-c012-496e-8612-3ed7a8df5800/lesson/eb618e3c-aa00-4b68-b122-87713c7d3fb3)
