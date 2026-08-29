# Backstage Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Backstage-Basics/Backstage-Architecture/page

Overview of Backstage architecture explaining plugin-based React frontend, Node backend, monorepo layout, plugin routes, and use of Material UI for developer portals.

This article explains the architecture of Backstage and how its pieces fit together. If you already know how typical web applications are structured, Backstage will feel familiar: it follows the same frontend → backend → storage pattern, but it is built as a plugin-oriented developer portal.

## How a typical web app works (quick recap)

A standard website usually has:

* A frontend that runs in the user's browser and renders UI.
* A backend that exposes APIs and persists data to a database.
* The frontend requests data from the backend, which queries storage or external services and returns results.

Example requests a frontend might make:

```http theme={null}
GET http://backend-url/products
```

```http theme={null}
POST http://backend-url/auth/signin
```

The backend validates and processes requests, then returns data so the frontend can update the UI. In short:

frontend → backend API → database/service → backend returns data → frontend renders it

## Backstage follows the same pattern

Backstage is a web application with a frontend and a backend, but it is designed as a modular system of plugins. Each plugin implements a feature (a catalog, CI/CD integrations, observability panels, etc.). Plugins may include:

* a frontend component (UI rendered in Backstage), and
* an optional backend component (server-side logic, API endpoints, secrets handling, or integrations with external services).

A frontend plugin asks for data either directly from a backend plugin or from third-party APIs. For instance, a GitLab plugin’s frontend might call its backend, which in turn calls the GitLab API, processes results, and returns structured data for the UI.

<Frame>
  <img alt="A diagram titled &#x22;Backstage Architecture&#x22; showing frontend and backend sections with colored plugin blocks (Catalog, GitLab, Kubernetes). Arrows indicate interactions with an external GitLab service and a backend database." />
</Frame>

Think of each plugin as a small, self-contained app: a frontend UI that can optionally be backed by server-side code. Backstage stitches those frontend plugin UIs into a single, unified web UI and aggregates backend plugin endpoints into one server surface.

### Plugin routes

Each plugin is reachable under its own route. Common examples:

* `/catalog` — service and component catalog
* `/lighthouse` — Lighthouse audits UI

Navigate to those paths in the Backstage UI to open the plugin pages.

<Frame>
  <img alt="A slide titled &#x22;Backstage Architecture&#x22; showing a screenshot of Backstage's Lighthouse plugin with a dark left navigation bar and an &#x22;Audits&#x22; table in the main pane. Two rounded buttons on the left display example URLs: http://backstage-url/catalog and http://backstage-url/lighthouse." />
</Frame>

## Typical Backstage project layout (monorepo)

When you create a Backstage app you often get a monorepo: frontend and backend code live in the same repository, typically under a `packages` folder.

| Package   | Purpose                            | Example / Notes                                                        |
| --------- | ---------------------------------- | ---------------------------------------------------------------------- |
| `app`     | Frontend application               | The React-based Backstage app rendered in the browser (`packages/app`) |
| `backend` | Backend server and backend plugins | Server-side endpoints, integrations, and services (`packages/backend`) |

You can develop and deploy the frontend and backend independently, but keeping them in a single repository simplifies local development and plugin wiring.

<Frame>
  <img alt="A screenshot of a project file tree titled &#x22;Backstage Architecture&#x22; showing folders like .yarn, dist-types, examples, node_modules and a packages folder. The packages folder contains &#x22;app&#x22; and &#x22;backend&#x22; entries, with visual labels linking &#x22;app&#x22; to Frontend and &#x22;backend&#x22; to Backend." />
</Frame>

> **lightbulb** Plugins may include only a frontend if no server-side logic or secrets are required. Add a backend component when you need to access databases, store secrets, or call third-party services securely.

## Frontend: React and components

Backstage frontends are built using React. If you are comfortable with React concepts—components, props, state, and composition—you will find Backstage plugin development straightforward.

A typical website stacks three core technologies:

* HTML — structure
* CSS — presentation
* JavaScript — behavior

React organizes UI into reusable components that encapsulate markup, styles, and behavior. Example terminal and system information (for context):

```bash theme={null}
$ kubectl get nodes
NAME               STATUS   ROLES                 AGE      VERSION
ru-node-1          Ready    control-plane,master  2y269d   v1.23.5

$ uptime
12:05:54 up 1000 days, 5:32, 1 user, load average: 0.18, 0.42, 0.73
```

Simple React component example (JSX):

```jsx theme={null}
import React from 'react';

export const Button = () => {
  const handleClick = () => {
    alert('Button clicked!');
  };

  return (
    <div>
      <h1>Don't Click The Button!!!</h1>
      <button onClick={handleClick}>Click Me</button>
    </div>
  );
};

export const MyForm = () => {
  return (
    <div>
      <input id="login" type="text" />
      <input id="password" type="password" />
      <Button />
    </div>
  );
};
```

Components compose: a parent renders child components, and each child manages its own markup and behavior. This composition makes it easy to build complex plugin UIs from small, testable pieces.

## UI design system: Material UI (MUI)

Backstage uses Material UI (MUI) to maintain a consistent look-and-feel and provide pre-built, accessible React components (buttons, cards, tables, text fields, switches, menus, etc.). Using MUI speeds development and reduces styling work for plugin authors.

<Frame>
  <img alt="A slide about Material UI (MUI) showing the MUI logo and a caption that it provides a simple, customizable, accessible library of React components. It lists pre-styled components such as Buttons, Text fields, Cards, Tables, Switch, and Menus." />
</Frame>

## Summary (key takeaways)

* Backstage is a web application composed of a React frontend, a Node-based backend, and persistent storage or third-party integrations.
* Plugins are the primary unit of functionality; each plugin can have a frontend and an optional backend.
* Plugins are reachable by their own routes (for example, `/catalog` or `/lighthouse`).
* Typical Backstage projects are organized as a monorepo with `packages/app` (frontend) and `packages/backend` (server).
* Backstage frontends are React-based and commonly use Material UI (MUI) for UI components.

## Links and References

* Backstage Documentation: [https://backstage.io/docs](https://backstage.io/docs)
* Material UI (MUI): [https://mui.com/](https://mui.com/)
* Kubernetes Concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/fcbbf923-69c3-4147-bd51-18db2bd18957/lesson/eb3ecd35-b1f4-4a92-ba1d-98d952e6c268)
