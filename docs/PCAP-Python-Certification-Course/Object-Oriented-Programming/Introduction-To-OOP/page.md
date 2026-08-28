# Introduction To OOP

Source: https://notes.kodekloud.com/docs/PCAP-Python-Certification-Course/Object-Oriented-Programming/Introduction-To-OOP/page

This article introduces object-oriented programming in Python, comparing it with procedural programming and explaining class creation and vehicle examples.

In Python, you can structure and organize your code using two main paradigms: the procedural approach and the object-oriented approach.

## Procedural vs. Object-Oriented Programming

The procedural approach separates data (stored in variables) from the code (grouped into functions and modules). In this method, functions work on data, but the data itself cannot invoke these functions directly.

<Frame>
  ![The image compares procedural and object-oriented programming. It explains that procedural programming distinguishes data and code, while object-oriented programming encloses them together in classes.](https://kodekloud.com/kk-media/image/upload/v1752882922/notes-assets/images/PCAP-Python-Certification-Course-Introduction-To-OOP/procedural-vs-object-oriented-programming.jpg)
</Frame>

In contrast, the object-oriented approach unifies data and code into a single entity called a class. A class acts as a blueprint or "cookie cutter" for creating objects (instances). These objects bundle together both state (attributes) and behavior (methods), allowing seamless interaction, data exchange, and method invocation while also ensuring data encapsulation and protection from unintended access.

<Callout icon="lightbulb">
  Classes serve as blueprints that not only encapsulate data but also bind functions (methods) that can operate on that data, facilitating modular and scalable code design.
</Callout>

## A Real-World Example: Vehicles

Consider vehicles as an example to understand how classes work in OOP. Despite the many types of vehicles, they all share a common characteristic—they can move. This universal trait allows us to create a general class for vehicles and then define more specific subclasses for different categories, such as land vehicles, water vehicles, air vehicles, and even space vehicles.

<Frame>
  ![The image is a flowchart categorizing vehicles into land, water, air, and space vehicles, with further subdivisions for land vehicles into wheeled, tracked, and hovercrafts.](https://kodekloud.com/kk-media/image/upload/v1752882922/notes-assets/images/PCAP-Python-Certification-Course-Introduction-To-OOP/vehicle-categorization-flowchart.jpg)
</Frame>

For instance, land vehicles can be subdivided into wheeled vehicles, tracked vehicles, and hovercrafts. In such a hierarchy, specific classes like wheeled vehicles inherit properties from more general classes such as land vehicles or even the broader vehicles class.

## Creating a Class in Python

To put the concept into practice, let's create a simple Python class for vehicles. In Python, you define a class using the `class` keyword followed by the class name and a colon. You can then create an instance (object) of that class by instantiating it. Here’s an example:

```python theme={null}
class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def move(self):
        print(f"The {self.make} {self.model} is moving.")
