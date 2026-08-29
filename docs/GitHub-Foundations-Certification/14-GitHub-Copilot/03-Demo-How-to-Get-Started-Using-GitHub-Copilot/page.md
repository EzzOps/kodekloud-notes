# Demo How to Get Started Using GitHub Copilot

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Copilot/Demo-How-to-Get-Started-Using-GitHub-Copilot/page

Guide to installing and using GitHub Copilot and Copilot Chat in Visual Studio Code with setup steps, chat modes, examples, and practical coding demonstrations.

GitHub Copilot is an AI pair-programming assistant that suggests code, completions, and can provide conversational help inside your editor. This guide shows how to install and configure GitHub Copilot and Copilot Chat in Visual Studio Code, how to open and use the chat UI, and includes practical examples you can try immediately.

* Primary resources:
  * GitHub Copilot: [https://docs.github.com/en/copilot](https://docs.github.com/en/copilot)
  * Copilot Chat: [https://docs.github.com/en/copilot/copilot-chat](https://docs.github.com/en/copilot/copilot-chat)
  * Visual Studio Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)

## Install the extensions

1. Open Visual Studio Code and open the Extensions view (Ctrl+Shift+X / Cmd+Shift+X).
2. Search for and install:
   * "GitHub Copilot" — core suggestions and completions.
   * "GitHub Copilot Chat" — conversational UI for asking and editing code. (If not installed automatically, install it separately.)
3. After installation:
   * Make sure both extensions are enabled.
   * Sign in to GitHub and authorize Copilot when prompted.

When installed and signed in, the Copilot extensions appear in the Extensions list and the Copilot Chat panel becomes available in the editor.

> **lightbulb** You can manually select which AI model Copilot Chat uses, or leave it on "Auto" so Copilot chooses the best model for your request.

## Opening Copilot Chat

After installation, look for the Copilot Chat toggle or icon (often on the Activity Bar or title bar). Click it to open the chat pane (commonly docked to the right side of the editor). The chat interface gives you a few primary actions and modes:

* Agent — run specialized workflows or automated tasks on your repository.
* Ask — pose natural-language questions about the current file or the entire workspace.
* Edit — request in-place changes that Copilot can suggest and optionally apply.
* Plan — ask Copilot to outline multi-step changes or high-level plans.

When Copilot Chat analyzes code to answer a question it will list which files and line ranges it referenced. Use that information to verify the scope of its analysis.

### Copilot Chat UI options (quick reference)

| UI Option       | Purpose                                                | Example prompt                                                 |
| --------------- | ------------------------------------------------------ | -------------------------------------------------------------- |
| Ask             | Natural-language questions scoped to file or workspace | `How many lives does the player start with?`                   |
| Agent           | Run predefined workflows and complex repo checks       | `Run test coverage report and summarize failures`              |
| Edit            | Propose code edits and optionally apply them           | `Refactor this function for clarity`                           |
| Workspace scope | Expand analysis beyond the current file                | Type `@workspace explain` in chat to instruct a workspace scan |

## Example: Asking Copilot Chat about your code

Below is a representative `index.html` for a simple game (cleaned and corrected). Use this as a sample file Copilot Chat can read to answer questions or suggest edits.

```html theme={null}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Block Buster - Enhanced Edition</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <div class="container">
    <!-- Welcome Screen -->
    <div class="screen active welcome-screen" id="welcomeScreen">
      <div class="header">
        <h1 class="title">BLOCK BUSTER</h1>
        <p class="subtitle">Enhanced Edition with Random Levels & Power-ups</p>
      </div>

      <div class="game-screen">
        <div class="welcome-content">
          <div class="game-info">
            <div class="info-row">
              <span class="info-label">GAME TYPE</span>
              <span class="info-value">Dynamic Brick Breaker</span>
            </div>
            <div class="info-row">
              <span class="info-label">LEVELS</span>
              <span class="info-value">Infinite Randomly Generated</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
```

When you open a source file (for example, `script.js`), Copilot Chat can read the file and answer contextual questions. Scope the analysis to the current file or the entire workspace by prefixing prompts with `@workspace` or selecting the workspace scope in the UI (e.g., `@workspace explain`).

### Example: power-up handling in `script.js`

This example shows a corrected and consolidated `switch` handling several power-up types. It demonstrates safe object spreading, consistent game state fields, and appropriate `break` usage.

```javascript theme={null}
switch (type) {
  case 'multiBall':
    if (gameState.balls.length > 0 && gameState.balls.length < 4) {
      const baseBall = gameState.balls[0];
      // Add two additional balls with slightly different dx directions
      gameState.balls.push({ ...baseBall, dx: Math.abs(baseBall.dx), dy: baseBall.dy });
      gameState.balls.push({ ...baseBall, dx: -Math.abs(baseBall.dx), dy: baseBall.dy });

      gameState.powerups.multiBall.active = true;
      gameState.powerups.multiBall.activationTime = currentTime;
    }
    break;

  case 'megaPaddle':
    // enlarge paddle for the duration of the power-up
    paddle.width = 200;
    gameState.powerups.megaPaddle.active = true;
    gameState.powerups.megaPaddle.activationTime = currentTime;
    break;

  case 'bulletMode':
    gameState.powerups.bulletMode.active = true;
    gameState.powerups.bulletMode.activationTime = currentTime;
    gameState.bulletFireCounter = 0; // reset counter for immediate firing
    break;

  default:
    // handle unknown power-up types if necessary
    break;
}
```

Best practices and quick reminders about the snippet:

* Always check that `gameState.balls[0]` exists before copying it to avoid exceptions.
* Maintain consistent fields on `gameState` (for example, `gameState.bulletFireCounter`) to prevent undefined references.
* Keep `break` statements at the end of each `case` block to avoid fall-through bugs.

## Using Ask / Agent / Edit modes effectively

* Ask: Use plain-language queries scoped to the current file or the full workspace (e.g., "How many levels does the game support?" or "How many lives does the player start with?"). Copilot Chat will report which files/lines it used for context.
* Agent: Run automated workflows or repository-wide analyses using specialized agents (useful for security checks, CI suggestions, or bulk refactors).
* Edit: Request concrete code edits. Copilot Chat suggests changes and can apply them; always review suggestions before accepting.

Example observations Copilot Chat might return after scanning a repository:

* "The game starts with three lives" (if the source initialization reflects this).
* "No hard-coded maximum level detected" (implying levels may be generated indefinitely).
* "Ball speed is fixed and not increased per level" (if no difficulty scaling logic exists).

If Copilot Chat finds a bug or missing behavior (for example, no difficulty scaling), ask it to propose a fix using Edit mode or to provide a plan to implement changes.

## Summary / Quick checklist

* Install GitHub Copilot and GitHub Copilot Chat extensions in Visual Studio Code.
* Open the Copilot Chat panel (Toggle Chat icon) and choose Ask, Agent, Edit, or Plan based on your goals.
* Use `@workspace` to analyze multiple files or the full repository.
* Carefully review any suggested edits before applying them.

> **lightbulb** Copilot Chat will list which files it referenced when forming an answer. Use that to verify the analysis scope and ensure Copilot had access to the relevant parts of your project.

## Links and references

* GitHub Copilot docs: [https://docs.github.com/en/copilot](https://docs.github.com/en/copilot)
* Copilot Chat docs: [https://docs.github.com/en/copilot/copilot-chat](https://docs.github.com/en/copilot/copilot-chat)
* Visual Studio Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/10478142-ccb7-4c4e-9a4d-7d9820bb8db6/lesson/71df419c-b080-4280-84fd-db0af899aae4)
