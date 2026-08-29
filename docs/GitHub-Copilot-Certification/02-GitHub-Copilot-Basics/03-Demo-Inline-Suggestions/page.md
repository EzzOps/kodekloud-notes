# ---------------- Configuration Constants ----------------
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
ROAD_WIDTH = 100
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2

VERT_ROAD_RECT = pygame.Rect(CENTER_X - ROAD_WIDTH/2, 0, ROAD_WIDTH, WINDOW_HEIGHT)
HORZ_ROAD_RECT = pygame.Rect(0, CENTER_Y - ROAD_WIDTH/2, WINDOW_WIDTH, ROAD_WIDTH)

STOP_LINE = {
    'north': CENTER_Y - ROAD_WIDTH/2,
    'south': CENTER_Y + ROAD_WIDTH/2,
    'east':  CENTER_X + ROAD_WIDTH/2,
    'west':  CENTER_X - ROAD_WIDTH/2
}

CAR_SPEED = 3                 # pixels per frame
CAR_SIZE = {'vertical': (20, 40), 'horizontal': (40, 20)}
SAFE_GAP = 10                 # pixels between cars
SPAWN_INTERVAL = 60           # frames between spawns
LIGHT_OFFSET = 30
LIGHT_RADIUS = 8
```

## Generating New Code with Inline Chat

Prompt Copilot to scaffold helper functions. For instance, generate `get_light_state` logic:

```python theme={null}
def get_light_state(direction, cycle_timer):
    """
    Determine traffic light state based on timer.
    - NS group: 'north'/'south'
    - EW group: 'east'/'west'
    """
    t = cycle_timer % CYCLE_LENGTH
    if direction in ('north', 'south'):
        if t < NS_GREEN_DURATION:
            return 'green'
        if t < NS_GREEN_DURATION + NS_YELLOW_DURATION:
            return 'yellow'
        return 'red'
    else:
        if t < NS_GREEN_DURATION + NS_YELLOW_DURATION:
            return 'red'
        if t < CYCLE_LENGTH:
            return 'green'
        return 'yellow'
```

## Creating Unit Tests with Pytest

Copilot can also generate test scaffolding. For example:

```python theme={null}
import pytest
from main2 import get_light_state, CYCLE_LENGTH, NS_GREEN_DURATION, NS_YELLOW_DURATION

@pytest.mark.parametrize("t", range(NS_GREEN_DURATION))
def test_ns_green_light(t):
    assert get_light_state('north', t) == 'green'
    assert get_light_state('south', t) == 'green'

@pytest.mark.parametrize("t", range(NS_GREEN_DURATION, NS_GREEN_DURATION + NS_YELLOW_DURATION))
def test_ns_yellow_light(t):
    assert get_light_state('north', t) == 'yellow'
    assert get_light_state('south', t) == 'yellow'
```

> **triangle-alert** Always install and pin your test dependencies to avoid mismatched versions:

  ```bash theme={null}
  pip install pytest
  ```

***

## References

* [GitHub Copilot Documentation](https://docs.github.com/copilot)
* [Pytest Official Site](https://docs.pytest.org/)
* [GitHub Copilot VS Code Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-certification/module/3d32a217-aca3-450a-882e-c9304c497387/lesson/47d50f33-ddfd-4163-b9d6-303714eceb15)


# Demo Inline Suggestions

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/GitHub-Copilot-Basics/Demo-Inline-Suggestions/page

Learn to use GitHub Copilots inline suggestions to enhance Flask API development efficiency.

In this tutorial, you’ll learn how to leverage GitHub Copilot’s inline suggestions to speed up building a Flask API. We’ll cover:

* Inline completions for new routes
* Inline chat refinements
* Comment-driven code generation
* Next-edit suggestions for refactoring

## Prerequisites

* Python ≥ 3.7
* Flask installed (`pip install flask`)
* GitHub Copilot extension enabled in your editor
* Basic knowledge of RESTful APIs

> **lightbulb** This demo uses an **in-memory database** (`items_db`). For production workloads, integrate a persistent data store like PostgreSQL or MongoDB.

## 1. Basic Flask App with In-Memory DB

Start with a simple Flask application. Create an `app.py` file:

```python theme={null}
from flask import Flask, request, jsonify
from models import Item

app = Flask(__name__)
