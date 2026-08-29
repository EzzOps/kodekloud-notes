# Each row: [id, type, color, price, rating]
products = [
    [1, "backpack", "blue", 23.50, 4.6],
    [2, "gym-bag", "light blue", 22.80, 4.4],
    [3, "duffel", "black", 35.00, 4.7],
]

# Find products priced around $23 (within $1)
result = [row for row in products if abs(row[3] - 23.0) <= 1.0]
print(result)
# Example output:
# [[1, 'backpack', 'blue', 23.5, 4.6], [2, 'gym-bag', 'light blue', 22.8, 4.4]]
```

For richer, context-aware recommendations we extend matrices into tensors. A tensor is a multi-dimensional array — in practice often three or more dimensions. Think of a tensor like a Rubik’s cube: each slice is a matrix, and stacking slices creates additional axes of information.

A common tensor layout in recommendation systems is:

* `users × products × interactions` (or time).
* The interactions axis can enumerate clicks, purchases, ratings, adds-to-cart, or time steps.

These additional dimensions capture user behaviour across multiple modes so models can learn patterns across users, items, and interaction types.

To make the difference clear:

| Representation | Dimensions | Example use                                             |
| -------------: | :--------: | ------------------------------------------------------- |
|         Vector |     1D     | Single user preferences for colours                     |
|         Matrix |     2D     | Products × features (type, colour, price, rating)       |
|         Tensor |     3D+    | Users × Products × Interactions (clicks, ratings, time) |

<Frame>
  <img alt="The image shows a 3D matrix labeled with product features and interactions, alongside a &#x22;You Might Also Like&#x22; section with product recommendations and prices. A person is speaking in the lower-right corner." />
</Frame>

Applied to Alice: the tensor tracks not only product features but also how Alice interacted with those products (clicked, searched, added to cart, rated). By learning multi-dimensional patterns (e.g., Alice tends to click blue backpacks and rate them highly), recommendation models can surface items she’s likely to buy next — such as backpacks, blue trainers, or gym equipment related to items she viewed.

Because tensors encode richer relationships than flat lists or 2-D matrices, models built on them can make stronger, more personalized predictions. Vectors, matrices, and tensors are therefore core building blocks in search systems, recommendation engines, and many machine-learning models.

<Frame>
  <img alt="The image is a presentation slide summarizing the uses of vectors, matrices, and tensors in data representation, alongside a person explaining." />
</Frame>

Better-structured, multi-dimensional data leads to smarter systems. When customers find what they need quickly and accurately, conversion and retention improve.

Further reading and resources:

* Python Basics course: [KodeKloud — Python Basics](https://learn.kodekloud.com/user/courses/python-basics)
* Intro to tensors and deep learning: \[Tensor Fundamentals — external resources]

- [Watch Video](https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/d8fa251f-80d2-4813-8b52-ad57051b1dcf/lesson/0e04f682-86d2-47a2-a989-c8d5c1a40f8a)


# Bayes Theorem and Statistical Inference

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Probability-and-Statistics/Bayes-Theorem-and-Statistical-Inference/page

Explains Bayes' theorem and how to update probabilities with examples like spam detection and DJ identification, highlighting applications in data science and decision making under uncertainty.

Welcome — it's Justyna from KodeKloud.

In this lesson we’ll see how Bayes’ theorem turns new evidence into better decisions. We’ll define the theorem, explain how it updates probabilities, and walk through intuitive examples — from recognizing DJs at an expo to how your inbox detects spam.

<Frame>
  <img alt="The image features a woman speaking in front of a presentation slide with a cartoon wolf. The slide outlines three points about Bayes' Theorem, including its definition, real-world applications, and connection to machine learning." />
</Frame>

Probability in data science is not guessing — it’s updating. Every new observation refines our belief, like adding pieces to a puzzle.

<Frame>
  <img alt="The image discusses Bayes' Theorem, highlighting its application in data science, machine learning, and AI, with a comparison of guess accuracy illustrated through bar charts." />
</Frame>

Why Bayes matters: it gives a principled rule for combining prior knowledge with observed evidence. Common application areas include:

| Area                | How Bayes is used                                                        |
| ------------------- | ------------------------------------------------------------------------ |
| Weather forecasting | Update rain probability as sensors and satellite data arrive             |
| Security screening  | Combine initial risk scores with secondary scan evidence                 |
| Recommendations     | Update user preferences from clicks and browsing behavior                |
| Spam filtering      | Adjust spam probability based on message features (words, links, sender) |
| Healthcare          | Combine symptoms and tests to estimate disease risk                      |
| Autonomous vehicles | Merge uncertain sensor readings to estimate hazard probabilities         |

<Frame>
  <img alt="The image features a bar graph titled &#x22;Airport Security Screening,&#x22; showing &#x22;Low Risk&#x22; and &#x22;Higher Risk&#x22; categories with corresponding bar heights, alongside a woman standing on the right." />
</Frame>

A concrete illustration: spam filtering. Email classifiers extract features (words, links, sender, formatting), compute how likely those features are under “spam” versus “not spam,” and update the spam probability. If the updated (posterior) probability exceeds a threshold, the email is flagged.

<Frame>
  <img alt="The image shows a presentation slide with the title &#x22;How Does Your Email Detect a Spam?&#x22; and a woman standing next to it. The slide includes a mock email interface highlighting a spam email titled &#x22;Crypt Lottery.&#x22;" />
</Frame>

This is often implemented as a simple decision pipeline: extract evidence → compute likelihoods → update posterior → compare with threshold → act.

<Frame>
  <img alt="The image shows a flowchart explaining how systems decide if an email is spam, accompanied by a person speaking. The flowchart categorizes emails into &#x22;High Probability&#x22; or &#x22;Low Probability&#x22; of being spam, leading to actions like &#x22;Mark as Spam&#x22; or &#x22;Deliver to Inbox.&#x22;" />
</Frame>

The core formula — simple, expressive, and practical:

<Frame>
  <img alt="The image presents Bayes' Theorem with its formula displayed, featuring a person explaining the concept and a cartoon character to the side." />
</Frame>

P(A | B) = P(B | A) × P(A) / P(B)

* P(A) — prior: what you believed about A before seeing B.
* P(B | A) — likelihood: how probable B is when A is true.
* P(B) — marginal: how common B is overall.
* P(A | B) — posterior: updated belief in A after observing B.

> **lightbulb** Bayes' theorem is a procedure: start with a prior, measure how likely the evidence is under each hypothesis, and update to get the posterior. This mindset is key for principled decision-making under uncertainty.

Example 1 — DJ vs Developer (intuitive grid)
You meet someone at a tech + music expo who looks "DJ-like" (shaved head, music gear). How likely are they actually a DJ?

Assumptions:

* 90% of attendees are developers, 10% are DJs.
* 70% of DJs behave in a way you’d call “DJ-like.”
* 10% of developers also behave “DJ-like.”

Visualize 100 people:

* DJs: 10 total → 70% of those act like DJs → 7 people.
* Developers: 90 total → 10% act like DJs → 9 people.
* Total acting like DJs: 7 + 9 = 16.

So the probability someone who looks like a DJ actually is a DJ = 7 / 16 ≈ 0.4375 (≈ 44%).

Here’s the same computation expressed as Bayes’ theorem in Python-style code:

```python theme={null}
