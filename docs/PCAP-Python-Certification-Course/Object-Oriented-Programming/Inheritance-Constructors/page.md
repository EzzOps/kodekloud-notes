# module.py
print("I like to be a module")
```

When you import this module in your `main.py` file, the print statement in `module.py` executes immediately:

```python theme={null}
# main.py
import module
```

The output will be:

```text theme={null}
I like to be a module
```

This behavior occurs because Python executes the module’s code during the import process. Module initialization happens only once—even if multiple modules import the same module, Python initializes it just once.

## The **name** Variable

Every Python module comes with an extra variable called `__name__` that indicates how the module is being used. If you run `module.py` directly, `__name__` is set to `"__main__"`. However, when you import `module.py` from another file (like `main.py`), `__name__` retains the module's file name (e.g., `"module"`).

Consider the following example:

```python theme={null}
# module2.py
print(__name__)

if __name__ == "__main__":
    print("I am not in a module")
```

When executed directly:

```Python theme={null}
$ python module2.py
__main__
I am not in a module
```

When imported from another file:

```text theme={null}
$ python main.py
module2
```

This mechanism allows you to write test code inside the module (protected by an `if __name__ == "__main__":` block) that only runs when executed directly, and not when imported.

## Creating a More Functional Module

Let’s enhance `module.py` by adding a variable and a function. This example illustrates how to define a variable named `counter` accessible via dot notation when the module is imported, and also how to designate private variables by prefixing names with an underscore.

Below is an updated version of `module.py`:

```python theme={null}
#!/usr/bin/env python3
''' module.py - an example of a Python module '''

__counter = 0

def get_sum(numbers):
    global __counter
    total = 0
    for element in numbers:
        __counter += 1
        total += element
    return total

if __name__ == "__main__":
    print("I prefer to be a module, but I can do some tests for you.")
    nums = [i + 1 for i in range(5)]
    print(get_sum(nums) == 15)
```

<Callout icon="lightbulb">
  The shebang (`#!/usr/bin/env python3`) ensures compatibility on Unix-like systems. The `if __name__ == "__main__":` block runs test code only when the module is executed as a standalone script.
</Callout>

To use this module in your main application, you can write:

```python theme={null}
#!/usr/bin/env python3
from module import get_sum

zeroes = [0 for _ in range(5)]
ones = [1 for _ in range(5)]
print(get_sum(zeroes))
print(get_sum(ones))
```

The expected output is:

```Python theme={null}
0
5
```

## Understanding Module Search Paths

When you import a module, Python looks for it in a list of predefined directories stored in `sys.path`. This list includes the current working directory, site-packages, and other Python-specific paths.

You can inspect the module search path with this code:

```python theme={null}
#!/usr/bin/env python3
import sys
for p in sys.path:
    print(p)
```

For example, the output may resemble:

```Python theme={null}
/home/runner/PeachpuffAmusedLoaderpi
/opt/virtualenvs/python3/lib/python3.8/site-packages
/usr/lib/python3.8.zip
/usr/lib/python3.8
/usr/lib/python3.8/lib-dynload
```

Python also supports importing modules from zip files, treating them like directories.

## Importing Modules from a Custom Directory

Suppose you have a directory named `ownModules` that contains a module called `module1.py` with the following content:

```Python theme={null}
I am in module 1
```

Note: Although many development environments show a file explorer with project files like `module1.py`, the functionality of module importation does not depend on the visual layout of your project.

<Frame>
  ![The image shows a coding environment with a file explorer on the left, displaying Python files, and an open editor in the center with a console on the right. The file "module1.py" is currently open and appears to be empty.](https://kodekloud.com/kk-media/image/upload/v1752882919/notes-assets/images/PCAP-Python-Certification-Course-User-Defined-Modules/coding-environment-python-files-editor.jpg)
</Frame>

To instruct Python to look in this directory, append its path to `sys.path`:

```python theme={null}
#!/usr/bin/env python3
from sys import path
path.append('ownModules')
from ownModules import module1
```

Executing the code above will produce:

```Python theme={null}
I am in module 1
```

## Creating and Using Packages

As your application grows, it’s beneficial to organize related modules into packages. A package is a directory hierarchy containing modules, where the `__init__.py` file is executed when a module from the package is imported. This can be used to initialize package-level variables or to automatically import submodules.

For instance, consider a package with a submodule for basic arithmetic operations. You can import a function from a submodule using its fully qualified name:

```python theme={null}
#!/usr/bin/env python3
from sys import path
path.append('packages')
from science.basic.methods import add
print(add(1, 2))
```

The output will be:

```Python theme={null}
3
```

Alternatively, if your package is distributed as a zip file, you can include it in the module search path like this:

```python theme={null}
#!/usr/bin/env python3
from sys import path
path.append('packages/science.zip')
from science.basic.methods import add
print(add(1, 2))
```

## Conclusion

This article has covered the essentials of creating user-defined modules and packages in Python. You now understand how to:

* Create a simple module and observe its execution during import.
* Use the `__name__` variable to control code execution.
* Enhance modules by adding functions and encapsulated variables.
* Inspect and manipulate the module search path.
* Organize modules into packages for a scalable project structure.

<Callout icon="lightbulb">
  To further solidify your understanding, experiment with these examples and consider integrating them into your own projects.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/a65eb782-d2dc-4850-9046-e4bb57d38876/lesson/b2a38fb6-e9ff-4db2-8b79-08d6ec762e1f" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/a65eb782-d2dc-4850-9046-e4bb57d38876/lesson/33d8559d-185e-43c5-a734-6c638a0321d1" />
</CardGroup>


# Inheritance Constructors

Source: https://notes.kodekloud.com/docs/PCAP-Python-Certification-Course/Object-Oriented-Programming/Inheritance-Constructors/page

This article covers inheritance, constructors, method overriding, and composition in Python, explaining how to enhance class functionality and manage object behavior.

When you print an instance of a class, Python by default displays a hexadecimal number representing the object’s memory address. This number is an internal object identifier. However, you can enhance the readability of printed instances by overriding the **str** method. By doing so, when you print an instance of your class, Python will display a descriptive string instead.

Consider the following example with a simple Dog class that customizes the **str** method:

```python theme={null}
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def __str__(self):
        return self.name + ' is a ' + self.breed

pet1 = Dog("Max", "Labrador")
print(pet1)
```

## Understanding Inheritance

Inheritance is a foundational concept in object-oriented programming. It allows a new class (called the subclass) to inherit attributes and methods from an existing class (known as the superclass). This mechanism enables you to extend or modify the behavior of the existing class without duplicating code.

<Frame>
  ![The image illustrates the concept of inheritance in programming, showing a hierarchy where attributes and methods are passed from a superclass "Vehicle" to subclasses "WheeledVehicle" and "Car."](https://kodekloud.com/kk-media/image/upload/v1752882921/notes-assets/images/PCAP-Python-Certification-Course-Inheritance-Constructors/inheritance-programming-vehicle-hierarchy.jpg)
</Frame>

Subclasses are specialized versions of a parent class. In the example below, the Animal class is the base class for two subclasses, Mammal and Dog. Here, a Mammal is an Animal, and a Dog is a Mammal.

For instance, we create an Animal instance representing a crocodile (type "reptile") and a Mammal instance representing a dolphin:

```python theme={null}
class Animal:
    def __init__(self, type):
        self.type = type

class Mammal(Animal):
    def __init__(self, animal):
        super().__init__("mammal")
        self.animal = animal

    def breathe(self):
        print("Breathing...")

class Dog(Mammal):
    def __init__(self, breed):
        super().__init__("dog")
        self.breed = breed

    def bark(self):
        print("Woof")

crocodile = Animal("reptile")
dolphin = Mammal("dolphin")
pet = Dog("Labrador")
```

In this hierarchy, the Dolphin (a Mammal) can breathe due to the inherited breathe method, while the Crocodile (simply an Animal) does not have this behavior. Furthermore, the Dog class inherits breathing ability from Mammal and includes its own bark method.

## Checking Inheritance with isinstance

You can verify the type of an object using the isinstance function. This function checks if an object is an instance of a specific class (or its subclasses), making it useful for confirming whether an object supports certain properties or methods.

```python theme={null}
class Animal:
    def __init__(self, type):
        self.type = type

class Mammal(Animal):
    def __init__(self, animal):
        super().__init__("mammal")
        self.animal = animal

    def breathe(self):
        print("Breathing...")

class Dog(Mammal):
    def __init__(self, breed):
        super().__init__("dog")
        self.breed = breed

    def bark(self):
        print("Woof!")

crocodile = Animal("reptile")
dolphin = Mammal("dolphin")
pet = Dog("Labrador")

print(isinstance(pet, Dog))      # True, pet is an instance of Dog.
print(isinstance(pet, Animal))   # True, Dog is derived from Animal.
print(isinstance(dolphin, Dog))  # False, a Mammal is not a Dog.
print(isinstance(dolphin, Animal))  # True, a Mammal is an Animal.
```

The output of this code will be:

```text theme={null}
True
True
False
True
```

## Using super to Access the Superclass

The super function allows you to call a method from the superclass without explicitly naming it. This approach reduces redundancy and improves maintainability. Notice how we no longer require passing self when using super().

```python theme={null}
class Animal:
    def __init__(self, type_value):
        self.type = type_value

class Mammal(Animal):
    def __init__(self, animal):
        super().__init__("mammal")
        self.animal = animal

    def breathe(self):
        print("Breathing...")

class Dog(Mammal):
    def __init__(self, breed):
        super().__init__("dog")
        self.breed = breed

    def bark(self):
        print("Woof")

crocodile = Animal("reptile")
dolphin = Mammal("dolphin")
pet = Dog("Labrador")
```

## Multiple Inheritance

Python supports multiple inheritance, which allows a subclass to inherit from more than one superclass. This way, the subclass can access properties and methods from various parent classes. For example:

```python theme={null}
class SuperA:
    var_a = 10
    def fun_a(self):
        return 11

class SuperB:
    var_b = 20
    def fun_b(self):
        return 21

class Sub(SuperA, SuperB):
    def sub_method(self):
        pass

obj = Sub()

print(obj.var_a, obj.fun_a())  # Output: 10 11
print(obj.var_b, obj.fun_b())  # Output: 20 21
```

In this example, the Sub class acquires members from both SuperA and SuperB. The sub\_method is a placeholder where you would implement subclass-specific behavior in a real-world application.

## Method Overriding and Polymorphism

Subclasses can override methods defined in their superclass, a concept known as method overriding. When you invoke a method on an instance, Python first looks in the subclass; if the method isn't found there, it searches the superclass.

Consider the following example where ClassB (a subclass) overrides the fun method from ClassA. When coolmethod is called, it executes the fun method from ClassB, demonstrating polymorphism:

```python theme={null}
class ClassA:
    def fun(self):
        print("fun from ClassA")

    def coolmethod(self):
        return self.fun()

class ClassB(ClassA):
    def fun(self):
        print("fun from ClassB")

new_value = ClassB()
new_value.coolmethod()  # Output: fun from ClassB
```

This design pattern keeps your code clean and consistent by allowing subclasses to modify or extend the functionality of their superclass as needed.

## Composition as an Alternative

An alternative to inheritance for extending a class's capabilities is composition. With composition, you include instances of other classes within a class, enabling you to combine behaviors flexibly with reduced coupling.

<Callout icon="lightbulb">
  Composition can offer greater flexibility compared to inheritance, especially when you want to dynamically change behavior by combining different objects.
</Callout>

The example below demonstrates how composition can be used to implement behavior by combining different objects:

```python theme={null}
import time

class Tracks:
    def change_direction(self, left, on):
        print("tracks:", left, on)

class Wheels:
    def change_direction(self, left, on):
        print("wheels:", left, on)

class Vehicle:
    def __init__(self, controller):
        self.controller = controller

    def turn(self, left):
        self.controller.change_direction(left, True)
        time.sleep(0.25)
        self.controller.change_direction(left, False)

wheeled = Vehicle(Wheels())
tracked = Vehicle(Tracks())

wheeled.turn(True)
tracked.turn(False)
```

The output from this code is:

```text theme={null}
wheels: True True
wheels: True False
tracks: False True
tracks: False False
```

This example shows how you can achieve different behaviors by passing in different controllers to the Vehicle class.

## Method Resolution Order (MRO)

The Method Resolution Order (MRO) in Python defines the sequence Python follows to search for an attribute or method in a class hierarchy. When multiple classes define the same method, Python uses the MRO to determine which method to execute.

Consider the following example with four classes: A, B, C, and D, where D inherits from both B and C, and both B and C inherit from A. If both B and C define a method named middle, Python will follow the MRO—from the bottom of the inheritance chain upward and from left to right:

```python theme={null}
class ClassA:
    def top(self):
        print("In ClassA")

class ClassB(ClassA):
    def middle(self):
        print("In ClassB")

class ClassC(ClassA):
    def middle(self):
        print("In ClassC")

class ClassD(ClassB, ClassC):
    def bottom(self):
        print("In ClassD")

obj = ClassD()
obj.middle()  # This will print: In ClassB
```

Changing the order of the superclasses in ClassD would lead Python to invoke the middle method from a different class, according to the MRO.

## The Diamond Problem

The diamond problem occurs in multiple inheritance when a subclass inherits from two parent classes that both derive from a common ancestor and override a certain attribute or method. Consider the following example where ClassB and ClassC override the greeting attribute inherited from ClassA:

```python theme={null}
class ClassA:
    greeting = "Hello from ClassA"

class ClassB(ClassA):
    greeting = "Hello from ClassB"

class ClassC(ClassA):
    greeting = "Hello from ClassC"

class ClassD(ClassB, ClassC):
    pass

d = ClassD()
print(d.greeting)
```

The output is:

```text theme={null}
Hello from ClassB
```

Because Python follows the MRO, it returns the greeting from ClassB first. If you remove the greeting attribute from ClassB, Python will retrieve it from ClassC or ClassA based on the MRO. It is important to be aware of this behavior when leveraging multiple inheritance.

That concludes this article. Now it's time to put these concepts into practice!

For more information on these topics, be sure to check out our [additional Python tutorials](https://www.python.org/doc/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/7e473cae-90c2-4d9a-8e81-6509481b52ce/lesson/0c32de64-2a75-4d5b-b083-b49cd9653cca" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/pcap-python-certification-course/module/7e473cae-90c2-4d9a-8e81-6509481b52ce/lesson/607248d0-99f7-4702-808f-ef45af510922" />
</CardGroup>
