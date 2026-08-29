# Partial Derivatives and Gradient Descent Part 1

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Calculus/Partial-Derivatives-and-Gradient-Descent-Part-1/page

Explains partial derivatives, gradients, and introductory gradient descent for optimizing multivariable problems such as routing and travel time.

Welcome — it's Justyna from KodeKloud.

In this lesson we uncover how gradient descent helps machines make smarter decisions. We will define what a gradient is, show how partial derivatives compute it, and see how these tools guide models (like routing apps) to better solutions step by step.

<Callout icon="lightbulb">
  This article explains gradients, partial derivatives, and the first steps toward gradient descent — practical math used in routing, machine learning, and optimization.
</Callout>

Why does this matter? Consider Susie, an Uber Eats driver: faster deliveries mean more orders and higher earnings. To optimize each delivery, her app must evaluate routes and update them as conditions change. Gradient-based methods help the app decide when and how to change the route.

<Frame>
  <img alt="The image shows a presentation slide with three topics related to gradients and optimization, alongside a person standing and talking. There's also a cartoon character of a gray cat wearing a bandana next to the slide." />
</Frame>

Have you ever wondered how your phone's map app finds the fastest route and then updates it as traffic changes?

<Frame>
  <img alt="The image shows a person standing next to a graphic of a map, with the text &#x22;Calculating the Fastest Route&#x22; above. The person is wearing a shirt with the &#x22;KodeKloud&#x22; logo." />
</Frame>

AI-powered routing doesn't just compute a single shortest path — it continuously improves route choices using gradient information.

<Frame>
  <img alt="The image shows a woman wearing a KodeKloud T-shirt standing next to graphics of a gradient chart and a smartphone displaying a map, with the text &#x22;AI and Gradient&#x22; above." />
</Frame>

Meet Susie again: she accepts an order, and her app quickly calculates the fastest route based on distance, speed, traffic, and more. The app evaluates many factors, and gradients help it decide which direction to change its route to reduce travel time.

<Frame>
  <img alt="The image displays a delivery person on a scooter with an Uber Eats box and a smartphone showing a map. A person wearing a KodeKloud shirt stands nearby, suggesting an app-related theme." />
</Frame>

Interested in solving real-world problems with math and AI? Careers that work on routing, autonomous driving, and logistics include:

| Role                      | Focus                                         | Why it matters                              |
| ------------------------- | --------------------------------------------- | ------------------------------------------- |
| Machine Learning Engineer | Train models that predict and optimize routes | Turns data into adaptive routing strategies |
| Data Scientist            | Analyze traffic, weather, and demand patterns | Finds signals to improve model performance  |
| Software Engineer         | Build the apps and systems users rely on      | Integrates models into real-time products   |
| Logistics Analyst         | Plan efficient delivery networks              | Reduces cost and improves service           |

These fields are growing rapidly and need problem-solvers who can blend math, data, and systems.

<Frame>
  <img alt="The image features a presentation slide titled &#x22;Tech Jobs Powering Self-Driving Cars&#x22; with illustrations of a &#x22;Software Engineer&#x22; and a &#x22;Logistics Analyst,&#x22; alongside a person speaking." />
</Frame>

Now, back to the math.

Derivatives describe the rate of change of a function. We often write the derivative of `f` with respect to `x` as `df/dx` (or `f'(x)`); both express how a small change in `x` affects `f(x)`.

<Frame>
  <img alt="The image shows a presentation about &#x22;Derivative as Rate of Change&#x22; with a mathematical function and its derivative formulas, along with a person gesturing in front of a dark purple background." />
</Frame>

Example — a simple difficulty function that scores a route from 0 to 10. Let `x` be the distance (miles). One illustrative function is:

```plaintext theme={null}
f(x) = x^4 - 3x^2 + 2.5
```

On the graph, a downward slope means difficulty is decreasing; an upward slope means difficulty is increasing. The best moment to consider changing routes is where the slope is zero (a local minimum/maximum or saddle point).

<Frame>
  <img alt="The image shows a map and a graph titled &#x22;Derivative,&#x22; illustrating a journey's difficulty level against distance, with a person explaining in the foreground." />
</Frame>

Take the derivative (using power rules; constants go to zero):

```plaintext theme={null}
df/dx = 4x^3 - 6x
```

This derivative guides decisions: if `df/dx` is negative, the difficulty decreases with a small increase in `x` (good); if positive, difficulty increases (bad). For specific values:

| x | df/dx calculation | df/dx |
| - | ----------------: | ----: |
| 1 |   `4(1)^3 - 6(1)` |    -2 |
| 2 |   `4(2)^3 - 6(2)` |    20 |

<Frame>
  <img alt="The image shows a presentation slide about derivatives, featuring mathematical formulas and a graph, alongside a person explaining the content." />
</Frame>

A negative derivative at `x = 1` means difficulty is decreasing there; a large positive derivative at `x = 2` means difficulty rises quickly — the model should avoid staying in that region. In real-world systems we often have many variables, so we turn to multivariable functions.

<Frame>
  <img alt="The image shows a diagram illustrating a multivariable function with individual functions ( f(x) = 2x^2 ), ( f(y) = y^3 ), and ( f(z) = 3z ), combining into a main function ( f(x, y, z) = 2x^2 + y^3 + 3z ). A person is gesturing on the right side wearing a &#x22;KodeKloud&#x22; T-shirt." />
</Frame>

Our earlier function used only `x`. To model travel time we add `y` (speed limit). A simple travel-time function might look like:

```plaintext theme={null}
f(x) = x^4 + 3x^2 + 2.5

T(x, y) = x^4 + 3x^2 + 2.5 + y^3 - 5xy
```

Note the interaction term `-5xy`: it links distance (`x`) and speed (`y`) to show they jointly affect travel time.

This function exists in 3D: `x` (distance) on one axis, `y` (speed limit) on another, and `t = T(x,y)` vertical. In practice we consider only positive `x` and `y` (distance and speed are non-negative). The `y` axis could represent coarse speed categories (1 = 10 mph, 2 = 20 mph, etc.), while `t` is travel time.

<Frame>
  <img alt="The image features a presentation on a multivariable function, showing a 3D graph with axes labeled &#x22;Travel Time,&#x22; &#x22;Speed Limit,&#x22; and &#x22;Starting Distance,&#x22; along with a person explaining the concept." />
</Frame>

Our goal is to minimize travel time, and with multiple variables we use partial derivatives to measure change with respect to each variable separately. Partial derivatives replace `d` with `∂` and, together, form the gradient — a vector pointing in the direction of greatest increase. For minimization we move opposite the gradient.

Compute partial derivatives of `T(x, y)`:

```plaintext theme={null}
T(x, y) = x^4 + 3x^2 + 2.5 + y^3 - 5xy

∂T/∂x = 4x^3 + 6x - 5y
∂T/∂y = 3y^2 - 5x
```

The gradient (vector of partial derivatives) is:

```plaintext theme={null}
∇T = [ ∂T/∂x, ∂T/∂y ] = [ 4x^3 + 6x - 5y, 3y^2 - 5x ]
```

To reduce travel time, an optimization algorithm (like gradient descent) updates `(x, y)` in small steps opposite to `∇T`, iteratively moving toward a local minimum.

<Callout icon="lightbulb">
  Partial derivatives measure how the function changes along one variable while holding others constant. The gradient combines these rates to indicate the steepest ascent; moving opposite the gradient reduces the function value.
</Callout>

Where do we go from here? In the next part we'll show how to use these partial derivatives in an iterative optimization algorithm (gradient descent), pick a learning rate, and watch how the route (or model parameters) converge toward an optimal solution.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/582ff79b-c012-496e-8612-3ed7a8df5800/lesson/18689958-6232-45da-ae19-e55c0f87deeb" />
</CardGroup>
