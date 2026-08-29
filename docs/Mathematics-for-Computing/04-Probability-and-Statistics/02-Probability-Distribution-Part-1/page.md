# DJ example
p_dj = 0.10
p_style_given_dj = 0.70
p_dev = 0.90
p_style_given_dev = 0.10

p_style = p_style_given_dj * p_dj + p_style_given_dev * p_dev
p_dj_given_style = (p_style_given_dj * p_dj) / p_style

p_style, p_dj_given_style  # (0.16, 0.4375)
```

<Frame>
  <img alt="The image shows a woman gesturing beside a pie chart, which indicates that 90% are developers and 10% are DJs." />
</Frame>

<Frame>
  <img alt="The image shows a diagram with probabilities related to different roles and a woman standing beside it, explaining the content." />
</Frame>

<Frame>
  <img alt="The image illustrates probabilities and conditional probabilities related to DJs and developers, possibly using Bayes' Theorem, with a character asking about finding the probability of someone acting like a DJ." />
</Frame>

Both the 100-person grid and Bayes’ calculation give the same counterintuitive result: even strong-looking evidence can be outweighed by base rates (priors).

<Frame>
  <img alt="The image illustrates Bayes' Theorem with graphs showing how beliefs update with new evidence, and features a person speaking next to the graphs." />
</Frame>

Example 2 — Spam filtering with the word "lottery"
Suppose we scan 1,000 emails:

| Category | Count | Contains "lottery" |
| -------- | ----: | -----------------: |
| Spam     |   100 |                  8 |
| Not spam |   900 |                  2 |
| Total    |  1000 |                 10 |

From this:

* P(spam) = 100 / 1000 = 0.10
* P("lottery" | spam) = 8 / 100 = 0.08
* P("lottery") = (8 + 2) / 1000 = 0.01

Apply Bayes:

P(spam | "lottery") = P("lottery" | spam) × P(spam) / P("lottery")\
\= 0.08 × 0.10 / 0.01 = 0.8

So, given the observed frequencies, an email containing "lottery" has an 80% posterior probability of being spam.

<Frame>
  <img alt="The image shows the results of a model scanning 1,000 emails for the word &#x22;lottery,&#x22; with a table categorizing emails as spam or not spam. A person is presenting the information next to the table." />
</Frame>

<Frame>
  <img alt="The image shows a person speaking in front of a dark background with Bayes' Theorem and its application to a spam probability problem displayed onscreen." />
</Frame>

Decision rule
Spam filters then compare the posterior probability to a threshold (e.g., 70%). If the posterior exceeds the threshold, the message is marked as spam. This threshold encodes the operational trade-off between false positives and false negatives.

<Frame>
  <img alt="The image illustrates a decision-making rule for marking emails as spam if the likelihood exceeds a 70% threshold, with a person standing beside the explanation." />
</Frame>

Summary

* Bayes’ theorem converts priors and likelihoods into posteriors — a formal way to update beliefs.
* It’s fundamental in spam filtering, medical testing, recommender systems, sensor fusion, and many ML tasks.
* Always consider the prior (base rate): a single piece of evidence can be misleading without it.

<Frame>
  <img alt="The image shows a woman in a KodeKloud T-shirt standing next to a chart labeled &#x22;Chance of being a DJ,&#x22; with the text indicating that only 10% are DJs and 10% of developers act like DJs." />
</Frame>

Bayes’ theorem is more than a formula — it’s a disciplined way to combine past knowledge and fresh observations to make better decisions under uncertainty.

Links and references

* [Bayes' theorem — Wikipedia](https://en.wikipedia.org/wiki/Bayes%27_theorem)
* [Naive Bayes classifiers — scikit-learn](https://scikit-learn.org/stable/modules/naive_bayes.html)
* Bishop, C. M. “Pattern Recognition and Machine Learning” — chapter on probabilistic models and inference

- [Watch Video](https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/7badce97-9acb-48b8-9fb6-bd5ce7e09045/lesson/0f8cd34b-333f-408a-b9a6-9c5219a44fea)


# Probability Distribution Part 1

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Probability-and-Statistics/Probability-Distribution-Part-1/page

Introductory explanation of probability distributions using Bernoulli, binomial, and normal examples applied to weather forecasting and decision making

Welcome — it's Justyna from KodeKloud.

In this lesson we introduce probability: the mathematics of uncertainty. Probability is not guesswork or certainty — it quantifies how likely events are. We use it across domains: weather forecasting, medical decision-making, traffic modeling, and machine learning. This article explains how probability distributions help make uncertain outcomes (like rain) actionable. We'll cover simple yes/no events (Bernoulli), repeated yes/no experiments (Binomial, briefly referenced), and the Normal distribution (overview) with a focus on how these ideas improve weather predictions.

<Frame>
  <img alt="The image shows a presentation slide with two points about probability distributions, alongside an animated character on the left and a person on the right." />
</Frame>

Why does a forecast say “70% chance of rain”? That phrasing causes confusion: does it mean 70% of the time, 70% of the area, or something else? Below we clarify the typical interpretation and show how distributions formalize that uncertainty.

Data scientists, machine learning engineers, and meteorological analysts each use probability differently:

* Data Scientists analyze historical weather to estimate patterns and probabilities.
* Machine Learning Engineers train models that output probability estimates.
* Meteorologists integrate models, observations, and expertise to produce forecast probabilities.

<Frame>
  <img alt="The image shows a weather app indicating a 70% chance of rain in Tampa, FL, alongside the question &#x22;Why does a 70% chance of rain confuse us?&#x22; and a person gesturing with their hands." />
</Frame>

<Frame>
  <img alt="The image depicts a presentation slide titled &#x22;Job Relevance&#x22; featuring illustrations of three roles: Data Scientist (Weather Tech), Machine Learning Engineer, and Meteorological Data Analyst. A person is also present beside the illustrations, gesturing as if explaining." />
</Frame>

Meet Jane. It's Thursday evening and she checks the weather app to decide what to wear and whether to bring an umbrella. The app shows a 70% chance of rain at 6–7 p.m.

<Frame>
  <img alt="The image features an illustration of a person with an umbrella checking a weather app, and a person speaking next to the app's display. The app shows rain probability and weather conditions throughout the day." />
</Frame>

Interpretation: the forecast means there is a 70% chance that rain will occur somewhere in the forecast area at some point during that hour. It does not specify how long it will rain or exactly where within the area it will rain. Forecast probabilities are statements about likelihoods, not precise timings or durations.

<Frame>
  <img alt="The image shows a woman standing next to a weather forecast display with a 70% chance of rain, alongside an illustration of a person holding an umbrella in the rain." />
</Frame>

Forecasts come from models and observations combined with probability theory. To formalize that process we use random variables and probability distributions.

## Random variables: discrete vs continuous

A random variable maps outcomes to numbers so we can analyze uncertainty mathematically.

| Type       | What it represents             | Examples                                               |
| ---------- | ------------------------------ | ------------------------------------------------------ |
| Discrete   | Countable outcomes             | `die roll = {1,2,3,4,5,6}`, `number of customers = 15` |
| Continuous | Measured values on a continuum | `height = 170.2 cm`, `temperature = 21.7 °C`           |

<Frame>
  <img alt="The image explains the concept of random variables with illustrations of discrete (things that we count) and continuous random variables (things that we measure), featuring a person and a graphical representation." />
</Frame>

Non-numeric outcomes (like “rain” vs “no rain”) can be encoded numerically so probability models apply. For example: `rain = 1`, `no rain = 0`. These encoded values let us treat categorical events as random variables.

A probability distribution assigns probabilities to each possible outcome. For a fair six-sided die:\
`P(1) = 1/6, P(2) = 1/6, ..., P(6) = 1/6`, which we can visualize as a bar chart.

<Frame>
  <img alt="The image demonstrates a probability distribution of a fair die roll, showing equal likelihood for each outcome with a chart and dice illustrations. A person is presenting the concept, wearing a KodeKloud shirt." />
</Frame>

Next, we focus on distributions especially relevant to forecasting: Bernoulli (single yes/no), Binomial (repeated trials), and the Normal distribution (continuous clustering around a mean).

## Bernoulli distribution — single yes/no events

The Bernoulli distribution models a single trial with two outcomes: success (1) or failure (0). Typical use cases include “raining vs not raining”, “spam vs not spam”, or “positive vs negative test”.

For a Bernoulli random variable X with success probability `p`, the probability mass function (PMF) can be written compactly:

```text theme={null}
P(X = x) = p^x * (1 - p)^(1 - x)   for x in {0, 1}
```

This expression gives the two probabilities explicitly:

* `P(X = 1) = p`
* `P(X = 0) = 1 − p`

Example: if `p = 0.7` for rain:

```text theme={null}
P(X = 1) = 0.7     (rain occurs)
P(X = 0) = 0.3     (no rain)
```

<Frame>
  <img alt="The image illustrates a Bernoulli distribution with a graph comparing the probability of rain vs no rain and includes a cartoon character discussing probability with a person standing next to the graph." />
</Frame>

A fair coin flip is a Bernoulli trial with `p = 0.5`. If both bars are 50% each, outcomes are equally likely.

<Frame>
  <img alt="The image explains the Bernoulli Distribution using a coin flip example, illustrating equal probabilities for heads and tails, alongside a cartoon character asking a question." />
</Frame>

Why use the compact PMF formula? Because it:

* Encodes both outcomes in one expression,
* Is trivial to implement in code and statistical libraries,
* Serves as a building block for more complex models (e.g., Binomial, logistic regression, Bernoulli likelihoods in Bayesian inference).

Short calculation recap for `p = 0.7`:

```text theme={null}
P(X = 1) = p^1 * (1 - p)^0 = 0.7
P(X = 0) = p^0 * (1 - p)^1 = 0.3
```

<Frame>
  <img alt="The image illustrates the Bernoulli formula with a graph comparing the probability of rain vs no rain and includes a cartoon character discussing probability with a person standing next to the graph." />
</Frame>

Where does `p` come from? From data and models. Meteorologists combine historical observations, model ensembles, and simulations to estimate probabilities. For example, if 7 out of 10 model ensemble members predict rain, that supports `p ≈ 0.7`. Probabilities summarize evidence, not guarantee single outcomes.

<Frame>
  <img alt="The image explains the Bernoulli formula, showing calculations for the probability of rain and not raining, with a cat character and a person alongside it." />
</Frame>

## Expected value of a Bernoulli

The expected value (mean) E\[X] describes the long-run average outcome after many independent trials. For Bernoulli X:

```text theme={null}
E[X] = (1 × P(X = 1)) + (0 × P(X = 0)) = 1 × p + 0 × (1 − p) = p
```

So when `p = 0.7`, `E[X] = 0.7`. That is why a 70% predicted probability can be read as a long-run fraction of occurrences.

<Frame>
  <img alt="The image features a presentation slide on the Bernoulli Distribution, showing the expected value (mean) calculation with a probability distribution chart for rain vs. no rain. There's also a person standing to the side of the slide." />
</Frame>

Bernoulli distributions are compact but powerful: they underpin binary classifiers, components of weather simulation pipelines, A/B tests, and probabilistic modeling in machine learning.

> **lightbulb** The Bernoulli distribution models single yes/no outcomes. Its expected value equals the success probability `p`, which is why a predicted probability (like 70%) can be interpreted as the long-run fraction of successes.

## Quick references and further reading

* Bernoulli distribution — Wikipedia: [https://en.wikipedia.org/wiki/Bernoulli\_distribution](https://en.wikipedia.org/wiki/Bernoulli_distribution)
* NOAA forecasting and probabilistic guidance: [https://www.noaa.gov/](https://www.noaa.gov/)
* Intro to probability and statistics for machine learning — scikit-learn documentation: [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)

For the next lesson we'll build on Bernoulli trials to discuss repeated trials (Binomial distribution) and continuous-valued distributions such as the Normal distribution and how they apply to forecasting and model evaluation.

- [Watch Video](https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/7badce97-9acb-48b8-9fb6-bd5ce7e09045/lesson/f26f893c-133d-4cc6-8999-ea511dfdf434)
