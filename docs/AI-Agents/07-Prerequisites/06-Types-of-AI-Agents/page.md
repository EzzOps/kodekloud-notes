# Types of AI Agents

Source: https://notes.kodekloud.com/docs/AI-Agents/Prerequisites/Types-of-AI-Agents/page

Overview of AI agent types, their decision architectures, capabilities, and guidance on selecting simple reflex, model-based, goal-based, utility-based, learning, and autonomous agents.

Welcome back!

This lesson examines the common types of AI agents, their capabilities, and when to use each. We start with a classification overview, then cover simple reflex, model-based reflex, goal-based, utility-based, learning, and autonomous agents. Finally, we compare them to show the progression from reactive systems to fully autonomous agents.

Understanding agent classes clarifies levels of intelligence, autonomy, and adaptability. Distinguishing simple reflex agents from fully autonomous systems helps you select the right architecture for chatbots, robotics, automation pipelines, or research assistants.

## Agent classification overview

AI agents are commonly classified by complexity, decision-making approach, and degree of autonomy. Each class builds on the previous: from rule-based reactivity to internal models, goal-directed planning, utility optimization, learning, and ultimately autonomous operation.

* Keywords: AI agent types, reactive agents, goal-based planning, utility optimization, learning agents, autonomous systems.
* Benefit: Choose an agent type that matches task complexity and environment dynamics to build efficient, scalable systems.

## Simple reflex agents

Simple reflex agents act only on the current percept (the immediate sensor input) using condition-action rules like “if X then do Y.” They do not store state or reason about the future.

* Strengths: fast, predictable, low compute requirements in fully observable, static environments.
* Limitations: fail in partially observable or ambiguous settings; cannot plan or use history.
* Typical examples: motion-sensor lights, basic threshold-based controllers.

Reactive cycle:

1. Sensors receive percepts describing current conditions.
2. Agent applies condition-action rules to decide “what to do now?”
3. Actuators execute the chosen action.
4. Repeat with no memory or learning.

## Model-based reflex agents

Model-based reflex agents add an internal state (a world model) enabling them to handle partial observability and reason about effects of past actions.

* Strengths: better handling of stateful, partially observable tasks; more robust than simple reflex agents.
* Typical use: robots that track cleaned areas to avoid repetition.
* Implementation pattern: maintain and update an internal state based on percepts and known dynamics.

Reactive loop with an internal model:

1. Sensors provide percepts.
2. Agent updates its internal state (model of the world).
3. Based on state and rules, it selects an action.
4. Actuators execute the action, changing the environment.

## Goal-based agents

Goal-based agents decide by selecting actions that lead toward explicit objectives. They simulate or search future states to choose behaviors consistent with goals.

* Strengths: supports intentional planning and deliberative behavior; can evaluate alternative plans.
* Typical use: route planning, scheduling, complex problem solving.

Decision loop:

1. Sensors provide percepts and agent updates internal state.
2. Agent reasons about possible futures if it takes different actions.
3. Using defined goals, it selects the action expected to best achieve the goal.
4. Actuators perform the action and the environment evolves.

<Frame>
  <img alt="The image is a diagram explaining a goal-based agent, showing how an agent interacts with the environment through sensors and actuators, using information about the state, world evolution, actions, and goals to determine appropriate actions." />
</Frame>

Goal-based agents are ideal for navigation, multi-step tasks, and any domain where planning toward a target state matters.

## Utility-based agents

Utility-based agents extend goal-based reasoning with a utility function that ranks outcomes numerically. They choose actions that maximize expected utility—balancing trade-offs like speed, safety, cost, or user preference.

* Strengths: compare multiple goal-achieving options and optimize based on preference/utility.
* Typical use: multi-criteria route selection, pricing decisions, decision-support systems.

Decision process:

1. Sensors report current percepts.
2. Agent predicts outcomes of candidate actions with its internal model.
3. Utility function evaluates desirability of each predicted outcome.
4. Agent selects the action that maximizes expected utility.
5. Actuators execute the action.

<Frame>
  <img alt="The image is a flow diagram titled &#x22;Utility-Based Agents,&#x22; illustrating the decision-making process of an agent interacting with its environment. It outlines steps involving state assessment, predictions of actions, utility evaluation, and final action selection based on perceived data." />
</Frame>

Utility-based approaches are especially valuable when several alternatives achieve the same goal but differ in risk, cost, or quality.

## Learning agents

Learning agents improve their behavior over time by observing outcomes and updating their decision policies. They combine action selection, evaluation, learning, and exploration.

Key components:

* Performance element: chooses and executes actions.
* Critic: measures performance against a standard and provides feedback.
* Learning element: updates the performance element using feedback.
* Problem generator: encourages exploratory actions to discover better strategies.

Learning cycle:

1. Sensors feed percepts to the performance element.
2. Agent acts and the critic evaluates results against performance metrics.
3. Learning element updates the policy or model based on feedback.
4. Problem generator introduces exploration to avoid local optima.
5. Updated actions execute via actuators; loop continues.

Learning agents are well-suited for dynamic environments like robotics, games, adaptive control, and recommendation systems.

<Frame>
  <img alt="The image is a diagram illustrating the components and processes within a learning agent, showing interactions between the agent and its environment. It includes sections labeled Critic, Learning Element, Problem Generator, and Performance Element." />
</Frame>

## Autonomous agents

Autonomous agents integrate sensing, internal modeling, goal pursuit, utility evaluation, planning, and continuous learning to operate with minimal human supervision. They actively explore and alter their environment to achieve broad objectives.

How they differ from generation-only models:

* Unlike models that primarily generate content on request (e.g., generative models), autonomous agents act proactively to observe, plan, and execute multi-step processes.
* They maintain long-term state and context for ongoing tasks.

Typical capabilities:

* Combine modeling, goal reasoning, utility optimization, and learning.
* Plan for extended horizons and coordinate complex workflows.
* Maintain memory and context across tasks.

A common autonomous automation loop:

1. Execute: an execution agent pulls an incomplete task, performs it, and returns results.
2. Enrich and Store: system enriches results and stores them in a `vector database` for memory and retrieval.
3. Context Retrieval: context agents query the `vector database` to fetch relevant background for the next task.
4. Create & Prioritize: a task-creation agent generates new tasks from enriched results and a prioritization agent orders them.
5. Loop: prioritized tasks feed back into execution, repeating the cycle.

Autonomous agents enable end-to-end automation for research, IT troubleshooting, fleet coordination, and complex process automation.

## Quick comparison

|         Agent type | Key capability                                | Best for                            | Example                                            |
| -----------------: | --------------------------------------------- | ----------------------------------- | -------------------------------------------------- |
|      Simple reflex | Immediate condition-action rules              | Highly observable, static tasks     | Motion-activated light                             |
| Model-based reflex | Internal state for partial observability      | Stateful robotic tasks              | Vacuum robot tracking cleaned areas                |
|         Goal-based | Planning toward explicit goals                | Navigation, scheduling              | Route planning                                     |
|      Utility-based | Optimize choices with a utility function      | Multi-criteria optimization         | Route selection balancing speed and safety         |
|           Learning | Improve behavior from feedback                | Dynamic environments, games         | Smart thermostat learning habits                   |
|         Autonomous | Integrate planning, utility, learning, memory | Open-ended, long-horizon automation | Automated research or IT troubleshooting pipelines |

## When to choose each agent

* Use simple reflex agents when the environment is fully observable and rules suffice.
* Use model-based reflex agents when you need memory or to infer unobserved state.
* Use goal-based agents when explicit objectives and planning are required.
* Use utility-based agents when you must compare trade-offs across multiple objectives.
* Use learning agents when performance must improve from experience or when the environment changes.
* Use autonomous agents for complex, long-running workflows that require coordination, memory, and self-directed task generation.

## Links and references

* [Generative models vs. autonomous agents](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai)
* [Vector databases for memory and retrieval in agent systems](https://learn.kodekloud.com/user/courses/vector-database-for-genai)

<Callout icon="lightbulb">
  Understanding these agent classes helps you select and design the right architecture for your task: from simple reactive controllers to fully autonomous systems that plan, optimize, and learn.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/3027a2f9-9ff6-40c0-8e44-121170fecef0/lesson/779bd15f-00d0-467f-bced-9c8b1f08b8c4" />
</CardGroup>
