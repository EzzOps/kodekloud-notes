# In-memory storage
items_db = []
current_id = 1

@app.route('/items', methods=['POST'])
def create_item():
    global current_id
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    new_item = Item(
        id=current_id,
        name=data['name'],
        description=data.get('description', '')
    )
    items_db.append(new_item)
    current_id += 1
    return jsonify(new_item.to_dict()), 201
```

As you type, Copilot suggests method bodies in real time.

## 2. Deleting All Items

Type a new route decorator and function signature:

```python theme={null}
@app.route('/deleteall', methods=['DELETE'])
def delete_all_items():
```

Copilot may auto-complete:

```python theme={null}
    global items_db
    items_db = []
    return jsonify({'message': 'All items deleted successfully'})
```

## 3. Generating Random Items

Define a “create random items” endpoint:

```python theme={null}
@app.route('/createrandom', methods=['POST'])
def create_random_items():
    global current_id
    data = request.get_json()
```

Copilot often suggests:

```python theme={null}
    if not data or 'count' not in data:
        return jsonify({'error': 'Count is required'}), 400

    count = data['count']
    for _ in range(count):
        new_item = Item(
            id=current_id,
            name=f"Random Item {current_id}",
            description=f"This is random item number {current_id}"
        )
        items_db.append(new_item)
        current_id += 1

    return jsonify([item.to_dict() for item in items_db[-count:]]), 201
```

## 4. Inline Chat: Analyze Numbers

Start with:

```python theme={null}
@app.route('/analyzenumbers', methods=['POST'])
def analyze_numbers():
    data = request.get_json()
```

Invoke Copilot’s **inline chat** and ask for number analysis. It may return:

```python theme={null}
    numbers = data.get('numbers')
    if not numbers:
        return jsonify({'error': 'No numbers provided'}), 400

    total = sum(numbers)
    average = total / len(numbers)
    return jsonify({'total': total, 'average': average})
```

### 4.1 Enhanced Validation & Stats

Refine the route for stronger validation:

```python theme={null}
@app.route('/analyzenumbers', methods=['POST'])
def analyze_numbers():
    data = request.get_json()

    if not data or 'numbers' not in data:
        return jsonify({'error': 'Numbers are required'}), 400

    numbers = data['numbers']
    if not all(isinstance(n, int) for n in numbers):
        return jsonify({'error': 'All elements must be integers'}), 400

    result = {
        'sum': sum(numbers),
        'average': sum(numbers) / len(numbers) if numbers else 0,
        'min': min(numbers) if numbers else None,
        'max': max(numbers) if numbers else None
    }

    return jsonify(result), 200

# Alternative registration:
app.add_url_rule(
    '/analyzenumbers',
    'analyze_numbers',
    analyze_numbers,
    methods=['POST']
)
```

## 5. Comment-Driven Suggestions

Write a descriptive comment, then let Copilot generate code:

```python theme={null}
# create a route to delete all items
@app.route('/items', methods=['DELETE'])
def delete_all_items():
    global items_db
    items_db = []
    return jsonify({'message': 'All items deleted successfully'})
```

## 6. Next-Edit Suggestions for Refactoring

Enable **Next-Edit Suggestions** in Copilot settings to receive automated refactors. Example: renaming `items_db` to `items_db_new`.

Before:

```python theme={null}
@app.route('/items', methods=['DELETE'])
def delete_all_items():
    global items_db
    items_db = []
    return jsonify({'message': 'All items deleted successfully'})
```

After accepting suggestion:

```python theme={null}
@app.route('/items', methods=['DELETE'])
def delete_all_items():
    global items_db_new
    items_db_new = []
    return jsonify({'message': 'All items deleted successfully'})
```

### Enabling Next-Edit Suggestions

Open GitHub Copilot settings and search for **next edit suggestions**. Toggle it on under the **Preview** options:

![The image shows a settings interface for GitHub Copilot in a code editor, displaying options for enabling auto completions and configuring language-specific settings.](https://kodekloud.com/kk-media/image/upload/v1752876813/notes-assets/images/GitHub-Copilot-Certification-Demo-Inline-Suggestions/github-copilot-settings-interface.jpg)

## Comparison of Copilot Features

| Suggestion Type       | Use Case                                     | Activation                                         |
| --------------------- | -------------------------------------------- | -------------------------------------------------- |
| Inline Completions    | Auto-complete functions and blocks           | Typing code                                        |
| Inline Chat           | Context-aware code suggestions via chat pane | Trigger inline chat (e.g., `Ctrl+Shift+I`)         |
| Comment-Driven        | Generate code from descriptive comments      | Add comment above function                         |
| Next-Edit Suggestions | Automated refactoring & renames              | Enable in Copilot settings, accept suggested edits |

## Links and References

* [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
* [Flask Quickstart](https://flask.palletsprojects.com/en/latest/quickstart/)
* [Python Packaging Guide](https://packaging.python.org/)

By combining these Copilot features, you can write, refine, and refactor Flask APIs faster and with confidence.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-certification/module/3d32a217-aca3-450a-882e-c9304c497387/lesson/ab4e6309-5ed5-4799-a0b2-275c87b2e8e0)


# Demo Multiple Suggestions

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/GitHub-Copilot-Basics/Demo-Multiple-Suggestions/page

Explore GitHub Copilot’s feature for multiple AI-generated code completions to enhance productivity and choose implementations that fit your style and requirements.

## Overview

Unlock GitHub Copilot’s power to explore and choose from multiple AI-generated code completions. This feature enhances productivity by letting you compare different implementations and pick the one that best fits your style and requirements.

## Accessing Multiple Suggestions

Use the following shortcut to open the suggestions panel:

| Platform        | Shortcut     |
| --------------- | ------------ |
| Windows / Linux | `Alt + ]`    |
| macOS           | `Option + ]` |

Once the panel appears, browse suggestions with the same shortcut and press `Tab` to insert your chosen snippet.

> **lightbulb** Use `Alt + [` (or `Option + [`) to navigate back to the previous suggestion.

## Base Code: Traffic Light Functions

Start with these core functions in your file:

```python theme={null}
def get_light_state(direction, cycle_timer):
    if direction == 'north':
        if cycle_timer < NS_GREEN_DURATION + NS_YELLOW_DURATION:
            return 'red'
        elif cycle_timer < NS_GREEN_DURATION + NS_YELLOW_DURATION + EW_GREEN_DURATION:
            return 'green'
        else:
            return 'yellow'

def draw_traffic_light(surface, direction, state):
    """
    Draws a circular traffic light for a given direction at a fixed offset from the intersection.
    """
    if direction == 'north':
        pos = (CENTER_X, STOP_LINE['north'] - LIGHT_OFFSET)
    elif direction == 'south':
        pos = (CENTER_X, STOP_LINE['south'] + LIGHT_OFFSET)
    elif direction == 'east':
        pos = (STOP_LINE['east'] - LIGHT_OFFSET, CENTER_Y)
    elif direction == 'west':
        pos = (STOP_LINE['west'] + LIGHT_OFFSET, CENTER_Y)
    # Drawing logic goes here...
```

With these helpers, you’re ready to add new features using Copilot’s multiple suggestions.

## Example 1: Adding `calculate_area`

Type this stub and invoke the suggestions panel:

```python theme={null}
def calculate_area(shape):
    """Calculate the area of a rectangle or circle."""
```

A sample completion might be:

```python theme={null}
def calculate_area(shape):
    """Calculate the area of a rectangle or circle."""
    if shape == 'rectangle':
        return CAR_SIZE['vertical'][0] * CAR_SIZE['vertical'][1]
    elif shape == 'circle':
        return 3.14 * (LIGHT_RADIUS ** 2)
    else:
        raise ValueError("Invalid shape type. Use 'rectangle' or 'circle'.")
```

Press `Tab` to insert the version you like.

## Example 2: Simulating an API Request

Ask Copilot for a basic API stub:

```python theme={null}
import random

def api_request():
    """
    Simulate a simple API request.
    Replace this with real network logic as needed.
    """
    return random.choice(['north', 'south', 'east', 'west'])
```

Explore suggestions that include error handling, retries, or logging.

## Example 3: Implementing QuickSort

Comment your goal and trigger multiple completions:

```python theme={null}
