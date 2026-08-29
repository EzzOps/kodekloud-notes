# Bonus Lecture Introduction to YAML

Source: https://notes.kodekloud.com/docs/Docker-Training-Course-for-the-Absolute-Beginner/Conclusion/Bonus-Lecture-Introduction-to-YAML/page

This lesson introduces YAML files and their use in representing structured configuration data in a human-readable format.

Welcome to this lesson on YAML! In this tutorial, you'll learn what YAML files are and how they are used to represent structured configuration data in a human-readable format. If you already have experience with YAML, feel free to skip ahead. However, if you're just starting out, I highly recommend following along since a solid understanding of YAML is essential for the rest of this course. If you've worked with XML or JSON before, you'll find that YAML is relatively straightforward.

Below is an example YAML file that represents server configuration data:

```yaml theme={null}
Servers:
  - name: Server1
    owner: John
    created: 12232012
    status: active
```

Even if you haven't worked with similar data formats, you'll be able to pick up YAML quickly through our coding exercises.

Next, let's compare how the same data can be represented in XML, JSON, and YAML. The image below shows a sample list of servers with XML on the left, JSON in the middle, and YAML on the right:

<Frame>
  <img alt="The image shows a diagram of a server list represented in XML, JSON, and YAML formats." />
</Frame>

## Basic Key-Value Pairs

YAML primarily uses key-value pairs to represent data. Each key is followed by a colon and a space, and then its corresponding value. For example, consider the following simple YAML structure:

```yaml theme={null}
Fruit: Apple
Vegetable: Carrot
Liquid: Water
Meat: Chicken
```

## Representing Arrays

To represent arrays (or lists) in YAML, define a key with a colon. On the next line, list each item with a dash. Below is an example that combines both key-value pairs and arrays:

```yaml theme={null}
