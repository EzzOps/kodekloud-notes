# Demo How to Get started Using GitHub Copilot 2

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Copilot/Demo-How-to-Get-started-Using-GitHub-Copilot-2/page

Guide demonstrating GitHub Copilot in VS Code using comment-driven autocomplete and Agent edit mode to add features, fix code, add sound, improve collision detection, and save high scores

This lesson demonstrates two practical ways to use GitHub Copilot in VS Code: comment-driven autocomplete and the Agent (edit) mode for analyzing and improving code. We'll walk through short examples from a small browser game project (showing how to add sound effects, improve collision detection, and save a high score).

<Callout icon="lightbulb">
  Make sure you have the GitHub Copilot Chat extension installed in VS Code and that Copilot is enabled for the workspace. For reference, see the official [GitHub Copilot documentation](https://docs.github.com/copilot).
</Callout>

Quick feature overview:

| Feature                     | Purpose                                            | Example action                                                                      |
| --------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Comment-driven autocomplete | Generate implementations from inline comments      | Add `// Function to save the high score to local storage` and accept the suggestion |
| Agent / Edit mode           | Explain, refactor, or enhance selected code blocks | Ask the Agent to add sound effects and robust collision checks                      |

***

## 1) Autocomplete by commenting

Copilot can infer intent from a comment and propose a context-aware implementation based on nearby code and the repository.

Example context (existing snippet):

```javascript theme={null}
document.addEventListener('keyup', (e) => {
  if (e.key === 'ArrowLeft') keyboard.left = false;
  if (e.key === 'ArrowRight') keyboard.right = false;
});
```

Now add this comment in the file:

```javascript theme={null}
// Function to save the high score to local storage
```

Copilot will propose an implementation grounded in the project context. Accepting the suggestion (for example, pressing Tab) gives a concise, usable function like this:

```javascript theme={null}
// Function to save the high score to local storage
function saveHighScore() {
  localStorage.setItem('blockBusterHighScore', gameState.highScore);
}

// ===== INITIAL SETUP =====
document.getElementById('welcomeHighScore').textContent = gameState.highScore;
```

Note how Copilot inferred the localStorage key and the `gameState.highScore` property from the surrounding project context and also reminded you to wire up the UI initial setup.

<Callout icon="warning">
  Avoid storing large or complex objects in localStorage unless intentional. Prefer storing a single value (e.g., a number or string). For example, store `gameState.highScore` instead of the entire `gameState` object.
</Callout>

***

## 2) Use the Agent / Edit mode to analyze and improve functions

The Agent/edit mode is powerful for selecting an existing block of code and requesting targeted edits: explanations, bug fixes, performance improvements, or feature additions (like sound effects). You can preview the generated diff and accept or reject changes.

Below is a typical collision detection function before changes:

```javascript theme={null}
// ==== COLLISION DETECTION ====
function collisionDetection() {
  gameState.balls.forEach(ball => {
    bricks.forEach(brick => {
      if (brick.status === 1) {
        let collision = false;

        if (brick.shape === 'circle') {
          const dx = ball.x - (brick.x + brick.radius);
          const dy = ball.y - (brick.y + brick.radius);
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < ball.radius + brick.radius) {
            collision = true;
            ball.dy = -ball.dy;
          }
        } else {
          if (ball.x > brick.x &&
              ball.x < brick.x + brick.width &&
              ball.y > brick.y &&
              ball.y < brick.y + brick.height) {
            collision = true;
            ball.dy = -ball.dy;
          }
        }
      }
    });
  });
}
```

Common Agent tasks here:

* Fix incorrect math or typos.
* Replace overly simplified collision tests with radius-aware checks.
* Add sound playback hooks on collisions.
* Mark bricks as cleared so they aren't processed again.

### Preload sound effects once

A good practice is preloading audio assets and providing a small `playSound` helper so the Agent can simply call `playSound('brickHit')` when needed:

```javascript theme={null}
// Preload sound effects once
const soundEffects = {
  brickHit: new Audio('sounds/brick-hit.mp3'),
  paddleHit: new Audio('sounds/paddle-hit.mp3'),
  wallHit: new Audio('sounds/wall-hit.mp3')
};

soundEffects.brickHit.volume = 0.4;
soundEffects.paddleHit.volume = 0.4;
soundEffects.wallHit.volume = 0.3;

function playSound(name) {
  const audio = soundEffects[name];
  if (!audio) return;
  audio.currentTime = 0;
  audio.play().catch(() => {});
}
```

### Improved collision detection with sound and robust checks

After requesting improvements from the Agent, you might end up with a cleaned-up and corrected collision handler that:

* Uses proper circle-circle and circle-rectangle collision checks (taking ball radius into account).
* Calls `playSound` for collisions.
* Marks bricks as cleared (`brick.status = 0`) to prevent repeated collisions.

```javascript theme={null}
function collisionDetection() {
  gameState.balls.forEach(ball => {
    bricks.forEach(brick => {
      if (brick.status === 1) {
        let collision = false;

        if (brick.shape === 'circle') {
          // Circle-circle collision
          const dx = ball.x - (brick.x + brick.radius);
          const dy = ball.y - (brick.y + brick.radius);
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < ball.radius + brick.radius) {
            collision = true;
            ball.dy = -ball.dy;
          }
        } else {
          // Circle-rectangle collision approximation using ball radius
          if (ball.x + ball.radius > brick.x &&
              ball.x - ball.radius < brick.x + brick.width &&
              ball.y + ball.radius > brick.y &&
              ball.y - ball.radius < brick.y + brick.height) {
            collision = true;
            ball.dy = -ball.dy;
          }
        }

        if (collision) {
          // Handle the brick being hit
          brick.status = 0; // mark brick as cleared
          playSound('brickHit');
          // Optionally update score or other game state here
        }
      }
    });
  });
}
```

### Paddle collision helper with sound

Encapsulating paddle collision logic in a helper improves readability and makes it easier for the Agent to target only this function in future edits:

```javascript theme={null}
function checkPaddleCollision(ball, paddle) {
  if (ball.y + ball.radius > paddle.y &&
      ball.y - ball.radius < paddle.y + paddle.height &&
      ball.x + ball.radius > paddle.x &&
      ball.x - ball.radius < paddle.x + paddle.width) {
    playSound('paddleHit');
    ball.dy = Math.abs(ball.dy); // ensure ball moves upward
  }
}
```

When you use the Agent/edit mode, remember to preview the diff. The Agent references your current file contents to produce context-aware suggestions, which helps avoid simple typos (for example, replacing an incorrect `Math.any` call with the correct `Math.sqrt`) and adding necessary preloads and sound calls.

***

## Save high score (final, corrected)

Here's a compact, correct save function and an initial UI setup snippet that you can accept directly via autocomplete or allow the Agent to add for you:

```javascript theme={null}
// Function to save the high score to local storage
function saveHighScore() {
  localStorage.setItem('blockBusterHighScore', gameState.highScore);
}
```

```javascript theme={null}
// ===== INITIAL SETUP =====
document.getElementById('welcomeHighScore').textContent = gameState.highScore;
```

***

These two Copilot features—comment-driven autocomplete and the Agent/edit mode—let you quickly add small features (like saving high scores), inject media (sound effects), and iteratively refactor or fix logic in place. Always review proposed diffs and test after applying changes. For more, see:

* GitHub Copilot docs: [https://docs.github.com/copilot](https://docs.github.com/copilot)
* MDN Web Docs — localStorage: [https://developer.mozilla.org/docs/Web/API/Window/localStorage](https://developer.mozilla.org/docs/Web/API/Window/localStorage)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/10478142-ccb7-4c4e-9a4d-7d9820bb8db6/lesson/08e02619-8b6b-46a2-9a8b-53c769d3fe95" />
</CardGroup>
