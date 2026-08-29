# Probability Distribution Part 2

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Probability-and-Statistics/Probability-Distribution-Part-2/page

Explains Bernoulli and binomial distributions, probability versus expected value, examples using rain forecasts, calculations, and applications in machine learning.

Probability quantifies the chance of a single event (for example, rain at 6 PM). Expected value (mean) describes the average outcome across many repeated experiments. Understanding both helps translate single-event forecasts into long-run expectations.

<Frame>
  <img alt="The image shows a weather forecast app interface with probabilities of rain and sunshine, alongside text comparing probability and expected value, with a person gesturing beside it." />
</Frame>

If each of 10 consecutive hours has a 70% chance of rain, we expect about 7 rainy hours on average. Expected value gives this "big picture" across repeated trials, while a single forecast provides the probability for one trial.

## Bernoulli distribution — single yes/no trial

The Bernoulli distribution models a single binary outcome: success (e.g., rain) with probability p, or failure (no rain) with probability 1 − p. The two outcomes are mutually exclusive and exhaustive. The Bernoulli random variable X takes values 1 (success) or 0 (failure).

<Frame>
  <img alt="The image is an educational slide about the Bernoulli Distribution, featuring key points, a probability distribution bar chart for rain vs. no rain, and a person speaking." />
</Frame>

Practical example: Justyna sees a 70% chance of rain at 6 PM. Under a Bernoulli model, the two outcomes are:

* Rain: probability p = 0.7
* No rain: probability 1 − p = 0.3

With such a high p, bringing an umbrella is a rational decision. Bernoulli models are the building block for binary decision-making and binary classifiers in machine learning.

## From Bernoulli to binomial — multiple repeated trials

When the same Bernoulli trial is repeated a fixed number of times (n), and trials are independent with constant success probability p, the count of successes X follows a binomial distribution.

The binomial model applies when:

* the experiment is repeated a fixed number of times (n),
* each trial has exactly two outcomes (success or failure),
* the probability of success p is constant across trials,
* trials are independent.

<Frame>
  <img alt="The image explains the conditions for a binomial distribution, featuring three points: repeated trials, only two outcomes, and constant probability. It includes an illustration of coins and a person gesturing." />
</Frame>

Return to Justyna’s 10-hour forecast: each hour is a trial (n = 10), success = rainy hour, p = 0.7, and we assume independence between hours. This fits the binomial model.

<Frame>
  <img alt="The image explains conditions that fit a binomial distribution, including repeated trials, two outcomes, constant probability, and independence, with examples relating to weather prediction. A person is also visible on the right." />
</Frame>

Key questions you can ask with the binomial model:

* What is the probability it rains in exactly 3 of the 10 hours?
* What is the probability of exactly 7 rainy hours?
* What is the chance it rains every hour?

The binomial probability mass function gives the probability of exactly x successes in n trials:

P(X = x) = C(n, x) \* p^x \* (1 − p)^(n − x)

where C(n, x) = "n choose x" is the number of distinct ways to choose which x trials are successes.

<Frame>
  <img alt="The image shows the binomial probability formula, with a person explaining it. There are also examples of calculating the probability of rain for 3 or 10 hours." />
</Frame>

The combination factor uses factorials:

C(n, x) = n! / (x! (n − x)!)

A factorial n! is n × (n − 1) × ... × 1. Factorials get large quickly, but many terms cancel when computing combinations.

<Frame>
  <img alt="The image shows the binomial probability formula with expressions for factorial calculations, alongside a person wearing a KodeKloud t-shirt." />
</Frame>

## Example calculations (n = 10, p = 0.7)

* For x = 2:
  * C(10, 2) = 45
  * P(X = 2) = 45 \* 0.7^2 \* 0.3^8 ≈ 0.00145

* For x = 7:
  * C(10, 7) = C(10, 3) = 120
  * P(X = 7) = 120 \* 0.7^7 \* 0.3^3 ≈ 0.2668

* For x = 10:
  * C(10, 10) = 1
  * P(X = 10) = 0.7^10 ≈ 0.02825

These results show that observing only 2 rainy hours is unlikely when p = 0.7, while 7 rainy hours is the single most likely exact count.

<Frame>
  <img alt="The image illustrates the binomial probability formula, calculating the probability of 7 rainy hours out of 10, with a person gesturing in the foreground." />
</Frame>

You can compute these probabilities programmatically. Concise Python example:

```python theme={null}
import math

def comb(n, k):
    return math.comb(n, k)  # Python 3.8+

def binomial_p(n, k, p):
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

n = 10
p = 0.7

for k in [2, 7, 10]:
    print(f"P(X={k}) = {binomial_p(n, k, p):.6f}")
```

Running this prints approximately:

* P(X=2) = 0.001447
* P(X=7) = 0.266828
* P(X=10) = 0.028248

Plotting the full distribution from X = 0 to 10 shows that low counts (0–2) have very small probability mass, while counts around 6–8 are much more likely. The mode (tallest bar) in this example is at 7, matching the expected value.

The expected value (mean) of a binomial distribution is straightforward:

E\[X] = n \* p

For n = 10 and p = 0.7:
E\[X] = 10 \* 0.7 = 7

<Frame>
  <img alt="The image illustrates the expected value of a binomial distribution related to rain, with a graph showing probabilities, and includes a woman explaining the concept." />
</Frame>

Why isn't the probability of exactly 7 equal to 1 even though the mean is 7? Because the mean is an average across many repeated 10-hour experiments. Any single 10-hour period can produce 5, 6, 7, or 8 rainy hours; probability mass is spread over these nearby outcomes. Over many repeated experiments, the average count will converge toward 7.

An intuitive metaphor: imagine a bag with 10 marbles, 7 green (success) and 3 red (failure). Sampling with replacement 10 times will most often yield counts clustered near 7 green draws, but not always exactly 7.

<Frame>
  <img alt="The image features a presentation slide on &#x22;Binomial Distribution: Expected Value&#x22; that details a probability scenario with a likelihood graph, next to a person speaking." />
</Frame>

## Summary: Bernoulli vs Binomial

| Distribution | What it models                  | Parameters                          | Typical use                                                     |
| ------------ | ------------------------------- | ----------------------------------- | --------------------------------------------------------------- |
| Bernoulli    | Single yes/no trial             | p (success probability)             | Single-event predictions (e.g., rain at 6 PM)                   |
| Binomial     | Count of successes in n repeats | n (trials), p (success probability) | Counts across fixed trials (e.g., rainy hours in 10-hour block) |

## Applications in machine learning and AI

* Bernoulli: models a single binary label (spam vs. not spam), foundational for logistic regression and binary classification.
* Binomial: models counts of successes across trials, useful for A/B testing (how many users click a link out of N impressions) and aggregate performance metrics.

<Frame>
  <img alt="The image features a presentation slide focused on distributions in machine learning and AI, along with a person standing in front of the slide. It lists applications of Bernoulli and Binomial distributions, such as spam detection and sentiment analysis." />
</Frame>

These simple distributions are fundamental building blocks for probabilistic modeling and many AI techniques. They help convert single-event probabilities into actionable expectations over time.

> **lightbulb** Expected value describes the long-term average, not the guaranteed outcome of a single trial. Use the binomial distribution to quantify the probability of specific counts around that mean.

## References and further reading

* [Bernoulli distribution — Wikipedia](https://en.wikipedia.org/wiki/Bernoulli_distribution)
* [Binomial distribution — Wikipedia](https://en.wikipedia.org/wiki/Binomial_distribution)
* For practical implementations and probability tools, see the Python `math.comb` documentation and scientific libraries like NumPy and SciPy.

- [Watch Video](https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/7badce97-9acb-48b8-9fb6-bd5ce7e09045/lesson/70c89dde-588d-49b9-9813-34ed74e2b3c2)
