# Partial Derivatives and Gradient Descent Part 2

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Calculus/Partial-Derivatives-and-Gradient-Descent-Part-2/page

Explains partial derivatives, gradients, and gradient descent applied to optimization and routing examples such as travel-time minimization.

This guide continues the practical exploration of partial derivatives and how the gradient drives gradient descent. We keep the original sequence of examples and diagrams to clarify each concept and show real-world applications like route optimization.

## 1. Simple example: f(x, y) = x^2 + y^2

When computing a partial derivative, treat all other variables as constants.

* ∂f/∂x: treat y as constant → derivative of x^2 is 2x, derivative of y^2 is 0. So `∂f/∂x = 2x`.
* ∂f/∂y: treat x as constant → derivative of y^2 is 2y, derivative of x^2 is 0. So `∂f/∂y = 2y`.

Together these partials form the gradient vector, which points in the direction of the steepest increase of the function.

<Frame>
  <img alt="The image features a presentation slide titled &#x22;Why Gradient?&#x22; with a cartoon character, a mountainous landscape with a sunrise, and a person speaking next to it." />
</Frame>

Gradient (in vector form):

```latex theme={null}
\nabla f = \left[\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}\right]
\nabla f = [2x, 2y]
```

Evaluate at (1, 1):

```latex theme={null}
f(x,y) = x^2 + y^2
\nabla f = [2x, 2y]

\text{At }(1,1):
\nabla f = [2(1), 2(1)] = [2, 2]
```

Interpretation: both components are positive, so moving in +x or +y increases f. To decrease f (i.e., go "downhill"), move opposite the gradient: in direction `-∇f`.

## 2. A slightly more complex function: f(x, y) = x^3 + y^3 + xy

Next example introduces higher powers and an interaction term.

<Frame>
  <img alt="The image shows a presentation about partial derivatives with a mathematical function ( f(x, y) = x^3 + y^3 + xy ), alongside a person gesturing as if explaining the concept." />
</Frame>

Compute partial derivatives term-by-term:

* ∂f/∂x: derivative of `x^3` is `3x^2`; `y^3` is constant → 0; derivative of `xy` w\.r.t. x is `y`.\
  So `∂f/∂x = 3x^2 + y`.

* ∂f/∂y: derivative of `y^3` is `3y^2`; `x^3` is constant → 0; derivative of `xy` w\.r.t. y is `x`.\
  So `∂f/∂y = 3y^2 + x`.

Gradient:

```latex theme={null}
\nabla f = [3x^2 + y, \; 3y^2 + x]
```

Evaluate at (1, 1):

```latex theme={null}
\nabla f(1,1) = [3(1)^2 + 1, \; 3(1)^2 + 1] = [4, 4]
```

This `[4, 4]` indicates the steepest increase direction at `(1,1)`. To reduce the function value, move opposite this vector.

## 3. Travel-time model: Susie's delivery route

We now apply partial derivatives to a travel-time model. Let T(x, y) be Susie’s travel time depending on distance `x` and speed-limit-related variable `y`.

Example model:

T(x,y) = x^4 + 3x^2 + 2.5 + y^3 - 5xy

<Frame>
  <img alt="The image shows a woman in front of a black background with mathematical equations and a 3D graph. Labels like &#x22;Travel Time,&#x22; &#x22;Speed Limit,&#x22; and &#x22;Starting Distance&#x22; are on the graph." />
</Frame>

Differentiate term-by-term:

* ∂T/∂x:
  * d/dx(`x^4`) = `4x^3`
  * d/dx(`3x^2`) = `6x`
  * d/dx(`2.5`) = `0`
  * d/dx(`y^3`) = `0` (y constant)
  * d/dx(`-5xy`) = `-5y`
    \=> `∂T/∂x = 4x^3 + 6x - 5y`

* ∂T/∂y:
  * d/dy(`y^3`) = `3y^2`
  * d/dy(`-5xy`) = `-5x`
    All other terms are constant in y => `∂T/∂y = 3y^2 - 5x`

Gradient:

```latex theme={null}
\nabla T = [4x^3 + 6x - 5y, \; 3y^2 - 5x]
```

Evaluate at (1, 1):

```latex theme={null}
\text{At }(1,1):
\nabla T = [4(1)^3 + 6(1) - 5(1), \; 3(1)^2 - 5(1)]
\nabla T = [4 + 6 - 5, \; 3 - 5] = [5, -2]
```

Interpretation: the gradient `[5, -2]` points to the direction that increases travel time most rapidly. A positive first component means increasing `x` (distance) tends to increase time; a negative second component means increasing `y` (speed-limit variable) tends to reduce time. Thus, to reduce travel time, move opposite the gradient.

> **lightbulb** Gradient descent update (one step): `new_position = current_position - learning_rate * gradient`. Recompute partial derivatives at the new position and repeat until convergence.

The app uses this iterative process: recompute partial derivatives with updated conditions (traffic, speed, closures), step opposite the gradient to reduce travel time, and refine the route in real time.

## 4. Real-time routing example (Susie on a scooter)

Susie trusts the app’s computed route. If traffic changes, the app updates variables and recomputes the gradient to adapt the route.

<Frame>
  <img alt="The image shows a person on a scooter with Uber Eats branding, holding a phone, alongside a map and app interface graphics. A woman is also present, gesturing as if speaking or explaining something." />
</Frame>

Quick recap (how the app minimizes travel time):

* Model travel time as a multivariable function (distance, speed, traffic, signals).
* Compute partial derivatives to measure local sensitivity of time to each variable.
* Combine partials into the gradient: the direction of greatest increase.
* Use gradient descent: iteratively step in the negative-gradient direction to decrease travel time.

<Frame>
  <img alt="The image shows a summary of how math helps find the fastest route, with three points listed on a black background. A woman stands to the right, speaking, with the text &#x22;KodeKloud&#x22; on her shirt." />
</Frame>

## 5. Where this math is used

Gradient-based optimization is foundational in many modern systems:

* Recommendation engines (Netflix, Spotify) — minimize prediction error.
* Self-driving vehicles — continuous control optimization with sensor inputs.
* Logistics (Amazon, Uber Eats) — routing and fuel/time minimization.
* Machine learning — neural network training via variants of gradient descent.

<Frame>
  <img alt="The image features a presentation slide explaining the use of machine learning in Netflix, Spotify, self-driving cars, and delivery services, alongside a person in a black shirt." />
</Frame>

## Quick reference: common derivative rules

| Rule                                            | Example                                            |
| ----------------------------------------------- | -------------------------------------------------- |
| Power rule                                      | d/dx(`x^n`) = `n x^{n-1}`                          |
| Constant                                        | d/dx(`c`) = `0`                                    |
| Treat other variables as constants for partials | For `f(x,y)`, `∂/∂x (y^3) = 0`                     |
| Product with one variable                       | d/dx(`xy`) w\.r.t. x = `y` (y treated as constant) |

## Final takeaway

* Partial derivatives quantify how each independent variable affects the output locally.
* The gradient bundles partials into the direction of steepest ascent.
* Gradient descent follows the negative gradient to find minima, making it a powerful tool for optimization in routing, ML, control systems, and more.

Further reading:

* [Gradient Descent — Wikipedia](https://en.wikipedia.org/wiki/Gradient_descent)
* [Khan Academy: Partial Derivatives](https://www.khanacademy.org/math/multivariable-calculus)

- [Watch Video](https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/582ff79b-c012-496e-8612-3ed7a8df5800/lesson/c9062502-0dfe-4208-b83d-7e2bccf5c451)
