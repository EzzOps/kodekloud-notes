# Bitwise Operators

Source: https://notes.kodekloud.com/docs/Python-Basics/Logic-and-Bit-Operations/Bitwise-Operators/page

Explains Python bitwise operators, their behavior, examples, shifting, compound assignments, and two's complement implications for flags, masks, and low-level integer manipulation.

Bitwise operators let you manipulate individual bits of integer values by operating on their binary representations. These operators are commonly used for flags, masks, low-level data manipulation, and performance-sensitive code.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Bitwise Operators&#x22; showing four black boxes with green symbols (&, |, ~, ^) labeled Conjunction, Disjunction, Negation, and Exclusive. The title is centered above the evenly spaced icons." />
</Frame>

How each operator works:

| Operator    | Symbol | Description                                                                             | Example                                    |      |           |
| ----------- | ------ | --------------------------------------------------------------------------------------- | ------------------------------------------ | ---- | --------- |
| Bitwise AND | `&`    | Returns 1 for each bit position where both operands have 1                              | `15 & 22` → `6`                            |      |           |
| Bitwise OR  | \`     | \`                                                                                      | Returns 1 where at least one operand has 1 | \`15 | 22`→`31\` |
| Bitwise XOR | `^`    | Returns 1 where exactly one operand has 1 (exclusive OR)                                | `15 ^ 22` → `25`                           |      |           |
| Bitwise NOT | `~`    | Flips every bit. In Python this produces the two's‑complement negative: `~n == -n - 1`  | `~22` → `-23`                              |      |           |
| Left shift  | `<<`   | Moves bits left (multiplying non-negative integers by powers of two)                    | `22 << 1` → `44`                           |      |           |
| Right shift | `>>`   | Moves bits right (dividing non-negative integers by powers of two using floor division) | `22 >> 1` → `11`                           |      |           |

Note: Bitwise operators operate on integers only; they are not defined for floating-point numbers in Python. For official behavior and details, see the Python documentation on numeric types and bitwise operations.

Bitwise AND example (15 & 22)

15 in binary: 00001111\
22 in binary: 00010110

Bitwise AND compares each corresponding bit and returns 1 only where both bits are 1:

```python theme={null}
print(15 & 22)  # 6
```

The result 6 corresponds to binary 00000110.

Bitwise OR example (15 | 22)

Bitwise OR returns 1 for a bit position if either (or both) input bits are 1:

```python theme={null}
print(15 | 22)  # 31
```

The result 31 corresponds to binary 00011111.

Bitwise XOR example (15 ^ 22)

Bitwise XOR returns 1 only when exactly one of the bits is 1.

<Frame>
  <img alt="A dark interface screen showing a puzzle titled &#x22;Exactly 1&#x22; with four colored boxes containing 0s and 1s connected by caret (^) symbols, suggesting exclusive choices. The boxes are outlined in red and green and centered beneath a small upward arrow." />
</Frame>

```python theme={null}
print(15 ^ 22)  # 25
```

The result 25 corresponds to binary 00011001.

Bitwise NOT example (\~22)

Bitwise NOT flips every bit. In Python this yields the two's‑complement negative value; the identity \~n == -n - 1 holds for integers:

<Frame>
  <img alt="A dark UI-style image showing two stacked black tiles on the left with green numbers &#x22;22&#x22; and &#x22;-23&#x22;, and two horizontal rows of small rounded tiles to the right containing 0s and 1s, where the 1s are highlighted green and the 0s red." />
</Frame>

```python theme={null}
print(~22)  # -23
```

Compound assignment forms

You can combine bitwise operations with assignment to update a variable in place. The long and abbreviated forms are equivalent:

```python theme={null}
