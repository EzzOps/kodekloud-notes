# Iterating Lists

Source: https://notes.kodekloud.com/docs/Python-Basics/Lists/Iterating-Lists/page

This lesson explores using a for loop in Python to iterate through a list and calculate the average age from a dataset.

In this lesson, we will explore how to use a for loop to iterate through a list in Python to calculate the average age from a dataset. The process involves summing all the ages and then dividing that total by the number of ages using the built-in len() function.

## Step 1: Calculate the Total Sum of Ages

Start by initializing a variable called total to zero. Then, iterate over each element in the list to accumulate the sum of the ages:

```python theme={null}
ages = [56, 72, 24, 46]
total = 0
for age in ages:
    total += age
```

During each iteration, the value of the current age is added to the total. After the loop completes, the total sum of the ages becomes 198.

## Step 2: Compute the Average Age

After obtaining the total sum, calculate the average by dividing the total by the number of items in the list:

```python theme={null}
average = total / len(ages)
print(average)
