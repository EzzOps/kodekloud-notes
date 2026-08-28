# Derivatives and Gradients Part 2

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Calculus/Derivatives-and-Gradients-Part-2/page

Explains derivatives and differentiation rules including the power rule, interpreting rates of change, tangents, and applications in motion, self driving, and computer vision

Let's start with a few definitions and notation.

A derivative represents the instantaneous rate of change of a function. The process of finding a derivative is called differentiation. If `f(x)` denotes a function, then `f'(x)` denotes its derivative — the instantaneous rate of change of `f` at `x`. Understanding derivatives is essential for physics, engineering, machine learning, and computer vision.

<Frame>
  <img alt="The image explains the concepts of derivatives and differentiation along with notation examples, and features a woman presenting on the right side." />
</Frame>

Constant functions

If a function is constant — for example `f(x) = 6` — its value does not change as `x` changes. The derivative measures change, so the derivative of a constant is zero:

```text theme={null}
f(x) = 6
f'(x) = 0
```

<Frame>
  <img alt="The image shows a presentation slide about derivatives, specifically a horizontal line with no slope or change, illustrating the function ( f(x) = 6 ). A person stands to the right of the slide." />
</Frame>

Linear functions and slope

For a straight-line function the rate of change is constant. The derivative of a linear function equals its slope, computed as rise over run (vertical change divided by horizontal change). For example, `f(x) = 3x` has slope 3: if the rise is 3 and the run is 1, the slope is 3. If `f(x)` models distance over time, the speed is constant.

<Frame>
  <img alt="The image shows a diagram explaining the derivative of a linear function, featuring the equation ( f(x) = 3x ) and a graph with a straight line and slope arrows. A person is gesturing next to the diagram." />
</Frame>

Visualizing distance and speed for a linear function helps connect math to intuition: distance grows linearly and speed (derivative) is constant.

<Frame>
  <img alt="The image depicts a visual explanation of the derivative of a linear function, with two graphs showing distance and speed over time, along with a person presenting the content." />
</Frame>

Non-linear functions and tangents

For non-linear functions the slope varies with `x`. To find the slope at a specific point we draw the tangent line — the straight line that just touches the curve at that point — and measure its slope there.

Consider the quadratic `f(x) = x^2`. The slope (derivative) differs at various `x` values:

* At `x = −1`, the tangent slopes downward: `f'(−1) = −2`.
* At `x = 0`, the tangent is horizontal: `f'(0) = 0`.
* At `x = 1`, the tangent slopes upward: `f'(1) = 2`.

Plotting these derivative values against `x` yields `f'(x) = 2x` — the derivative of `x^2`.

When `f(x)` represents distance and `f'(x)` represents velocity, the steepness of the distance graph corresponds to speed: steep = fast, flat = slow, zero slope = stopped. A sign change in the derivative indicates a change in direction.

For higher powers the pattern continues. Example: for `f(x) = x^3`, the derivative is `f'(x) = 3x^2`. The distance and derivative graphs together capture slowing, stopping, and speeding up.

<Frame>
  <img alt="The image shows a comparison of a cubic function ( f(x) = x^3 ) and its derivative ( f'(x) = 3x^2 ) with corresponding graphs. A person is present on the right side of the image." />
</Frame>

The power rule

From these examples we arrive at the power rule — a compact, efficient recipe for differentiating polynomials.

```text theme={null}
If f(x) = x^n, then f'(x) = n x^(n-1)
```

Apply the power rule to `f(x) = x^4` and you get `f'(x) = 4x^3`.

<Frame>
  <img alt="The image features a presentation on calculus, specifically the power rule for derivatives, with a speaker gesturing, wearing a &#x22;KodeKloud&#x22; shirt." />
</Frame>

Common extensions and rules

The power rule pairs with two common, useful extensions:

* Constant multiple rule: if a constant `a` multiplies the power, multiply the coefficient by the power.
  ```text theme={null}
  f(x) = a x^n
  f'(x) = a * n x^(n-1)
  ```
  Example: `f(x) = 5x^3` → `f'(x) = 15x^2`.

* Linearity (sum rule): differentiate each term separately.
  Example:
  ```text theme={null}
  f(x) = 4x^3 + 5x^2 − 7
  d/dx[4x^3] = 12x^2
  d/dx[5x^2] = 10x
  d/dx[−7] = 0
  So f'(x) = 12x^2 + 10x
  ```

Quick reference table

| Rule              | Formula                             | Example                           |
| ----------------- | ----------------------------------- | --------------------------------- |
| Power rule        | `d/dx[x^n] = n x^(n-1)`             | `d/dx[x^4] = 4x^3`                |
| Constant multiple | `d/dx[a·g(x)] = a·g'(x)`            | `d/dx[5x^3] = 5·3x^2 = 15x^2`     |
| Sum/Difference    | `d/dx[g(x) ± h(x)] = g'(x) ± h'(x)` | `d/dx[4x^3 + 5x^2] = 12x^2 + 10x` |
| Constant          | `d/dx[c] = 0`                       | `d/dx[7] = 0`                     |

Back to the car example

Suppose the distance-to-roadworks as a function of time is:

```text theme={null}
f(x) = x^2 - 80x + 400
```

Differentiate term-by-term using the power rule:

```text theme={null}
f'(x) = 2x - 80
```

The derivative `f'(x)` gives the instantaneous rate of change of distance with respect to time. For instance:

```text theme={null}
f'(0) = 2*0 - 80 = -80
```

<Callout icon="lightbulb">
  `f'(0) = -80` means the distance is decreasing at 80 units per time unit at `x = 0`. The derivative is a signed rate (negative indicates motion toward the roadworks). Speed, as commonly used, is the non-negative magnitude of velocity.
</Callout>

<Frame>
  <img alt="The image features a graph displaying a parabolic curve representing distance over time, with a derivative calculation and a question about negative speed. There is also a person gesturing, a cartoon cat, and a road with a car and cones at the bottom." />
</Frame>

Find when the instantaneous rate is zero by solving `f'(x) = 0`:

```text theme={null}
2x - 80 = 0
=> x = 40
```

So `f'(40) = 0`. At `x = 40` seconds the distance is neither increasing nor decreasing — the car is at its closest point to the roadworks. Before `x = 40` the distance is decreasing (`f'(x) < 0`); after `x = 40` it is increasing (`f'(x) > 0`).

<Frame>
  <img alt="The image shows a distance-time graph with an analysis indicating speed changes at 40 seconds, and a person standing next to it." />
</Frame>

Why derivatives matter (applications)

Derivatives are fundamental across engineering and computer science. Examples:

* Self-driving cars
  * compute instantaneous speed and direction (is distance increasing or decreasing),
  * decide braking or acceleration,
  * smooth acceleration/braking for comfort,
  * predict trajectories for safe lane changes and collision avoidance.

* Computer vision and machine learning
  * an image is a grid of pixel intensities (e.g., `0` to `255`),
  * computing differences between neighboring pixels approximates discrete derivatives,
  * these discrete derivatives highlight edges and motion (sharp local changes appear as peaks),
  * repeated derivatives across rows/columns help detect shapes and moving objects.

Summary

* A derivative measures how fast a quantity changes at a point.
* The power rule (`f(x) = x^n` → `f'(x) = n x^(n-1)`) makes differentiating polynomials quick and systematic.
* Interpreting derivatives connects math to real-world systems (self-driving cars) and machine perception (edge detection).

Further reading and references

* [Khan Academy — Derivatives Intuition](https://www.khanacademy.org/math/calculus-1/cs1-derivatives)
* [MIT OpenCourseWare — Single Variable Calculus](https://ocw.mit.edu/courses/mathematics/18-01sc-single-variable-calculus-fall-2010/)
* [Stanford — Computer Vision: Edge Detection Concepts](http://cs231n.github.io/convolutional-networks/#conv)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/582ff79b-c012-496e-8612-3ed7a8df5800/lesson/b9578c6e-d4df-4333-b01b-c9f692e767cf" />
</CardGroup>
