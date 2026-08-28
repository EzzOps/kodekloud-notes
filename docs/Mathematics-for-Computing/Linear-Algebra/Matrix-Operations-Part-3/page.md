# Sensor's matrix (rows: objects; columns: distance, height, movement)
S = [
    [5.0,  2.5, 0.0],
    [10.0, 3.0, 0.0],
    [12.0, 1.8, 1.0]
]

# Transformation matrix (diagonal: scale distance by 1.1, height by 1/3)
T = [
    [1.1,     0.0, 0.0],
    [0.0, 1.0/3.0, 0.0],
    [0.0,     0.0, 1.0]
]
```

These are tiny matrices for clarity — real sensor arrays can be large and are usually processed by optimized numerical libraries. In this example:

* The `1.1` in the (1,1) position increases recorded distance by 10% (compensating for how the sensor measures distance).
* The `1/3` in the (2,2) position scales height down by a factor of 3. The sensor’s maximum measurable height is 3 units, so dividing by 3 brings height into the range \[0, 1], making it easier to combine with other sensor channels.
* The `1` in the (3,3) position leaves the movement channel unchanged.

<Frame>
  <img alt="The image shows a graphical representation of a sensor's matrix being multiplied by a transformation matrix, with a person gesturing and a speech bubble asking about the division by 3." />
</Frame>

Because T is a diagonal matrix, multiplying S × T is equivalent to scaling each column of S by the corresponding diagonal element of T:

* First column (distance) multiplied by 1.1
* Second column (height) multiplied by 1/3
* Third column (movement) multiplied by 1

Column-wise scaling is a useful property of diagonal matrices — much cheaper to compute than a full matrix multiply and easy to reason about.

Manual column-wise computation:

* Row 1:
  * distance: 5 × 1.1 = 5.5
  * height: 2.5 × (1/3) = 0.833333...
  * movement: 0 × 1 = 0

* Row 2:
  * distance: 10 × 1.1 = 11.0
  * height: 3.0 × (1/3) = 1.0
  * movement: 0 × 1 = 0

* Row 3:
  * distance: 12 × 1.1 = 13.2
  * height: 1.8 × (1/3) = 0.6
  * movement: 1 × 1 = 1

So the resulting matrix R = S × T is:

```python theme={null}
R = [
    [5.5, 0.8333333333, 0.0],
    [11.0, 1.0,          0.0],
    [13.2, 0.6,          1.0]
]
```

For a quick view (rounded to two decimals where useful):

| Distance | Height | Movement |
| -------- | ------ | -------- |
| 5.5      | 0.83   | 0        |
| 11.0     | 1.00   | 0        |
| 13.2     | 0.60   | 1        |

Each sensor can apply its own transformation matrix so that all sensors “see” the scene in a common scale and coordinate system after transformation. This is why linear algebra is so useful in sensor fusion and robotics.

Exactly!

Before we move on, a concise summary: matrix multiplication applies linear transformations (scales, rotations, or mixes of channels) to many datapoints at once. Diagonal matrices scale individual channels independently; non-diagonal matrices can mix channels.

Now consider the next complication: the vehicle itself is moving. Can you still trust the raw sensor readings?

As the car moves forward, distances to objects change and those objects can appear taller (closer objects take up more of the sensor’s view). If you don’t correct for the car’s motion, your map of the environment will be distorted.

Example scenario: the car detects two objects — a tree (further away) and a pedestrian (closer). The sensor stores its observations in a data matrix while the car’s motion is encoded in a movement matrix that describes how camera motion mixes the sensor channels. A non-zero off-diagonal entry (for example, 0.2) indicates some distance information leaked into the height measurement, making objects appear taller when the car moves.

<Frame>
  <img alt="The image shows a diagram illustrating distances and heights of a tree and a pedestrian relative to a vehicle, alongside a person presenting, wearing a &#x22;KodeKloud&#x22; shirt." />
</Frame>

To correct for motion-induced distortion you apply the inverse of the movement matrix to the observed sensor matrix. The inverse “undoes” the mixing and scaling introduced by the vehicle’s motion so that the measurements reflect stable world coordinates again.

<Callout icon="lightbulb">
  Diagonal transformation matrices scale each corresponding column of the data matrix; their inverse rescales columns back to the original units. For non-diagonal movement matrices, the inverse reverses how channels (distance, height, etc.) were mixed.
</Callout>

Next up: we’ll dive into inverse matrices — how to compute them, when they exist, and how they let us remove the effect of motion from sensor readings so the vehicle builds an accurate map of its surroundings.

References and further reading

* [Matrix multiplication — Wikipedia](https://en.wikipedia.org/wiki/Matrix_multiplication)
* [Matrix inverse — Wikipedia](https://en.wikipedia.org/wiki/Invertible_matrix)
* [Introduction to linear algebra (concepts & applications)](https://mathinsight.org/matrix_inverse)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/d8fa251f-80d2-4813-8b52-ad57051b1dcf/lesson/c8c87999-c8d9-4739-9804-412eae4012d1" />
</CardGroup>


# Matrix Operations Part 3

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Linear-Algebra/Matrix-Operations-Part-3/page

Explains how to compute and verify the inverse of a 2×2 matrix, why the determinant matters, and applications to correcting sensor data and solving linear systems.

In this lesson we compute the inverse of a 2×2 matrix, verify the result by multiplication, and explain why the determinant determines invertibility. Understanding 2×2 inversion is a foundation for solving linear systems, correcting sensor data, and many other applied problems in engineering and computer vision.

What is a matrix inverse?

* For numbers: a × a^ = 1.
* For matrices: A × A^ = I, where I is the identity matrix (1s on the diagonal, 0s elsewhere).
  Multiplying any matrix by the identity leaves it unchanged, so the inverse is the matrix analog of a reciprocal.

Formula for the inverse of a 2×2 matrix

Given A:

\[ \[a, b],
\[c, d] ]

The inverse (when it exists) is:

A^ = (1 / (ad − bc)) × adj(A)

where:

* `ad − bc` is the determinant of A.
* `adj(A)` (the adjugate) is formed by swapping `a` and `d`, and negating `b` and `c`:

adj(A) = \[ \[ d, −b ],
\[ −c, a ] ]

<Frame>
  <img alt="The image explains how to find the inverse of a 2x2 matrix, showing the formula involving the determinant and adjoint. A person is also present, likely giving an explanation." />
</Frame>

Step-by-step example

Let A have entries `a = 2, b = 3, c = 1, d = 4`.

1. Compute the determinant:

det(A) = ad − bc = 2×4 − 3×1 = 8 − 3 = 5

2. Form the adjugate by swapping `a` and `d` and negating `b` and `c`:

adj(A) = \[ \[ 4, −3 ],
\[ −1, 2  ] ]

3. Multiply the adjugate by `1/det(A)`:

A^ = (1/5) × \[ \[ 4, −3 ],
\[ −1, 2  ] ]

<Frame>
  <img alt="The image is a tutorial on finding the inverse of a 2x2 matrix, showing the formula and an example calculation. A woman stands to the right, gesturing with her hands." />
</Frame>

Verify by multiplication

To confirm A^ is correct, multiply A by A^ and check you get the identity matrix `I = [ [1,0], [0,1] ]`. Do the four scalar dot-products in the usual order:

* row 1 of A × column 1 of A^
* row 1 of A × column 2 of A^
* row 2 of A × column 1 of A^
* row 2 of A × column 2 of A^

Compute the raw products before scaling by `1/5`, then apply the scalar factor:

* (row1·col1) = 2×4 + 3×(−1) = 8 − 3 = 5
* (row1·col2) = 2×(−3) + 3×2 = −6 + 6 = 0
* (row2·col1) = 1×4 + 4×(−1) = 4 − 4 = 0
* (row2·col2) = 1×(−3) + 4×2 = −3 + 8 = 5

Raw result matrix = \[ \[5, 0], \[0, 5] ].
Multiplying by the scalar `1/5` gives `I = [ [1,0], [0,1] ]`, confirming the inverse.

<Frame>
  <img alt="The image shows a mathematical matrix multiplication process with a result, alongside a person gesturing in front of a black background." />
</Frame>

Why the determinant matters

The determinant `ad − bc` appears in the denominator of the inverse formula. If the determinant is zero, the formula would divide by zero and no inverse exists. Such matrices are called singular or non-invertible.

Example of a zero determinant:

det = 2×6 − 4×3 = 12 − 12 = 0

<Callout icon="warning">
  If the determinant equals zero the matrix has no inverse. Such matrices are called singular.
</Callout>

You can apply this determinant test to any small square matrix: only square matrices with nonzero determinant have inverses.

<Frame>
  <img alt="The image shows a presentation slide titled &#x22;Let's Try!&#x22; with matrices and their determinants, including checks and crosses indicating correctness. A person stands next to the slide, gesturing with their hands." />
</Frame>

Quick reference table

| Item              | Formula / Rule                              | Notes                               |
| ----------------- | ------------------------------------------- | ----------------------------------- |
| Inverse (2×2)     | `A^{-1} = (1/(ad-bc)) × [[d, -b], [-c, a]]` | Requires `ad − bc ≠ 0`              |
| Determinant (2×2) | `ad − bc`                                   | If zero → singular (no inverse)     |
| Verification      | `A × A^{-1} = I`                            | Multiply and check you get identity |

Practical example: correcting sensor readings for movement

Imagine sensor readings distorted by vehicle motion. The motion can be modeled by a movement matrix that transforms the true sensor matrix. To recover the original readings, multiply the measured sensor matrix by the appropriate correction matrix (the inverse of the movement matrix).

<Frame>
  <img alt="The image shows a woman in front of a graphical representation of a matrix calculation involving a car, a palm tree, and a cone of light. The matrix indicates &#x22;Distance&#x22; and &#x22;Height&#x22; values." />
</Frame>

Apply the same inversion steps: compute `(1/det)` and the adjugate (swap `a` and `d`, negate `b` and `c`), then multiply that inverse by the sensor readings matrix to correct them.

<Frame>
  <img alt="The image illustrates the calculation of the inverse of a 2x2 matrix, labeled as the &#x22;Movement Matrix,&#x22; and explains the determinant and adjoint of the matrix." />
</Frame>

After computing the inverse, multiply the sensor matrix by the correction matrix (again: row×column for each entry) and simplify to obtain corrected values.

<Frame>
  <img alt="The image shows a mathematical problem involving matrix multiplication, labeled &#x22;Sensor's Matrix&#x22; and &#x22;Movement Matrix,&#x22; with a person speaking or presenting in front of it. The background is a dark purple." />
</Frame>

Compact example calculation

```text theme={null}
Sensor's Matrix
[ 8    5.2 ]
[ 4    2.5 ]

Movement Matrix (correction)
[ 1    -0.2 ]
[ 0     1   ]

Multiplication (Sensor × Movement)
[ 8×1 + 5.2×0    8×(-0.2) + 5.2×1  ]
[ 4×1 + 2.5×0    4×(-0.2) + 2.5×1  ]

Result
[ 8    3.6 ]
[ 4    1.7 ]
```

This small example shows how a correction (movement) matrix can restore readings closer to the intended values. In real systems, matrices are larger and numerically precise; matrix inversion and multiplication are central to sensor fusion, calibration, and real-time decision-making.

<Frame>
  <img alt="The image discusses the importance of matrices for self-driving cars, highlighting real-time decision-making and sensor data merging. A person is positioned in the lower right corner." />
</Frame>

Summary

* For a 2×2 matrix A = \[ \[a, b], \[c, d] ], the inverse is `A^{-1} = (1/(ad−bc)) × adj(A)`.
* The determinant `ad − bc` must be nonzero for the inverse to exist.
* Verification via `A × A^{-1} = I` confirms correctness.
* Applications: inverse and multiplication are used for correcting sensor measurements, calibration, and many applied linear-algebra tasks in robotics and autonomous systems.

Further reading and references

* [Khan Academy — Matrix inverses](https://www.khanacademy.org/math/linear-algebra/matrix-transformations/inverse-of-a-matrix)
* [MIT OCW — Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra/)
* [Wikipedia — Matrix inverse](https://en.wikipedia.org/wiki/Inverse_matrix)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/d8fa251f-80d2-4813-8b52-ad57051b1dcf/lesson/d1a68dcf-0b26-48fa-a1bd-4411472a1077" />
</CardGroup>
