# Demo Community Plugins

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Customization-Plugins/Demo-Community-Plugins/page

Guide to adding and configuring the GitHub Actions community plugin in Backstage, including frontend and backend installation, OAuth authentication, entity annotations, and UI integration.

This guide demonstrates how to add a Backstage community plugin to your instance and integrate it into an entity page. We use the GitHub Actions community plugin as an example and walk through:

* Locating the plugin in the Backstage community repository
* Installing frontend and backend packages
* Registering a backend provider for authentication
* Adding the plugin's UI to an entity page
* Annotating a component so the plugin can surface CI/CD data

## Finding the plugin

Community plugins are discoverable on the Backstage Plugins page and in the Backstage repository on GitHub. Searching for "GitHub Actions" leads you to the plugin folder and README in the [backstage/backstage/plugins](https://github.com/backstage/backstage/tree/master/plugins) area. Community plugins may include both frontend and backend packages (e.g., `plugin-name` and `plugin-name-backend`) or only frontend code. The GitHub Actions community plugin is primarily a frontend plugin but depends on backend auth/proxy support to perform authenticated requests.

<Frame>
  <img alt="A screenshot of a GitHub repository file view showing a folder tree on the left and a list of files (including README.md, package.json, CHANGELOG.md) on the right for a &#x22;GitHub Actions Plugin&#x22; workspace. The README content for the plugin is visible in the lower right." />
</Frame>

## Frontend-only plugins and backend proxies

Many frontend-only community plugins require a backend to handle authentication, hide API tokens, or proxy requests. For example, the Dynatrace plugin is a frontend app that uses a backend proxy to add API tokens server-side so tokens are never exposed in the browser.

Example: adding a Dynatrace tab to an entity (JSX):

```jsx theme={null}
// packages/app/src/components/catalog/EntityPage.tsx (example)
const serviceEntityPage = (
  <EntityLayout>
    [...]
    <EntityLayout.Route
      path="/dynatrace"
      title="Dynatrace"
      if={isDynatraceAvailable}
    >
      <DynatraceTab />
    </EntityLayout.Route>
  </EntityLayout>
);
```

Example proxy configuration (YAML) that forwards requests from the frontend to a backend proxy at `/dynatrace`, which adds the `Authorization` header using a backend environment variable:

```yaml theme={null}
proxy:
  endpoints:
    '/dynatrace':
      target: 'https://example.dynatrace.com/api/v2'
      headers:
        Authorization: 'Api-Token ${DYNATRACE_ACCESS_TOKEN}'

dynatrace:
  baseUrl: 'https://example.dynatrace.com'
```

## Installing the GitHub Actions plugin (frontend)

Install the frontend package inside your `packages/app` workspace:

```bash theme={null}
