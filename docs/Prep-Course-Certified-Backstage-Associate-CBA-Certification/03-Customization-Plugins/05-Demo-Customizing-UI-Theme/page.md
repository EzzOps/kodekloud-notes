# Demo Customizing UI Theme

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Customization-Plugins/Demo-Customizing-UI-Theme/page

Guide to create and register custom Backstage frontend themes using @backstage/theme, defining palettes, fonts, and providers so the UI reflects branded colors and typography

In this guide you'll create a custom theme for Backstage and wire it into your frontend app so the UI uses your colors, fonts, and other theme settings. This lets you provide consistent branding across the catalog, docs, and plugins.

<Callout icon="lightbulb">
  Theme configuration objects and helpers live in the `@backstage/theme` package. For the [Prep Course - Certified Backstage Associate (CBA)](https://learn.kodekloud.com/user/courses/prep-course-certified-backstage-associate-cba), remember `@backstage/theme` as the package that contains the theming helpers.
</Callout>

## What you'll do (high level)

| Step | Goal                                                    | Files / APIs                                                                       |
| ---- | ------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 1    | Add a theme definition inside the frontend app          | `packages/app/src/theme/myTheme.ts`                                                |
| 2    | Export one or more theme objects (light/dark, defaults) | `createBaseThemeOptions`, `createUnifiedTheme`, `palettes` from `@backstage/theme` |
| 3    | Register themes with the app (so users can select them) | `createApp({ themes: [...] })` and `UnifiedThemeProvider`                          |

## Where to put the theme file

In a standard Backstage monorepo, theme files belong in the frontend app package. A typical location:

* `packages/app/src/theme/myTheme.ts`

This keeps frontend-only configuration with other UI code and ensures theme compilation with your app bundle.

## Create `packages/app/src/theme/myTheme.ts`

This file defines and exports theme objects using the Backstage theme helpers. Use `createBaseThemeOptions` to obtain a compatible base and `createUnifiedTheme` to produce a theme object consumable by `UnifiedThemeProvider`.

Example `myTheme.ts`:

```typescript theme={null}
// packages/app/src/theme/myTheme.ts
import { createBaseThemeOptions, createUnifiedTheme, palettes } from '@backstage/theme';

export const myTheme = createUnifiedTheme({
  ...createBaseThemeOptions({
    palette: palettes.light,
  }),
  fontFamily: 'Comic Sans MS',
  defaultPageTheme: 'home',
});

export const funTheme = createUnifiedTheme({
  ...createBaseThemeOptions({
    palette: {
      ...palettes.light,
      mode: 'light',
      primary: {
        main: '#e03077',
      },
      secondary: {
        main: '#f50057',
      },
      navigation: {
        submenu: {
          background: '#35abe2',
        },
        background: '#f4f4f4',
        indicator: '#9d599f',
        selectedColor: '#9d599f',
        color: '#0d456b',
        navItem: {
          hoverBackground: '#35abe2',
        },
      },
      background: {
        default: '#ffffff',
        paper: '#f9f9f9',
      },
    },
  }),
  fontFamily: 'Inter, Arial, sans-serif',
  defaultPageTheme: 'home',
});
```

Notes about the example:

* `palettes.light` provides a solid base palette; you can override specific colors like `primary` and `secondary`.
* `navigation` contains Backstage-specific navigation colors and hover states.
* You can add typography, spacing, and other overrides as needed.

## Register the theme with your application

Open the app entry where `createApp` is called (commonly `packages/app/src/App.tsx`) and add theme entries to the `themes` array. Each theme entry needs:

* `id` — unique identifier
* `title` — shown in theme picker
* `variant` — e.g., `'light'` or `'dark'`
* `icon` — a JSX icon to display
* `Provider` — component that wraps the app with `UnifiedThemeProvider` and supplies the theme object

Example `App.tsx` changes:

```typescript theme={null}
// packages/app/src/App.tsx (relevant excerpts)
import React from 'react';
import { createApp } from '@backstage/app-defaults';
import { UnifiedThemeProvider } from '@backstage/theme';
import { myTheme, funTheme } from './theme/myTheme';
import LightModeIcon from '@mui/icons-material/LightMode'; // or any icon you prefer

const app = createApp({
  themes: [
    {
      id: 'my-theme',
      title: 'My Custom Theme',
      variant: 'light',
      icon: <LightModeIcon />,
      Provider: ({ children }: { children?: React.ReactNode }) => (
        <UnifiedThemeProvider theme={myTheme}>{children}</UnifiedThemeProvider>
      ),
    },
    {
      id: 'fun-theme',
      title: 'Fun Theme',
      variant: 'light',
      icon: <LightModeIcon />,
      Provider: ({ children }: { children?: React.ReactNode }) => (
        <UnifiedThemeProvider theme={funTheme}>{children}</UnifiedThemeProvider>
      ),
    },
  ],
  apis,
  bindRoutes({ bind }) {
    bind(catalogPlugin.externalRoutes, {
      createComponent: scaffolderPlugin.routes.root,
      viewTechDoc: techdocsPlugin.routes.docRoot,
      createFromTemplate: scaffolderPlugin.routes.selectedTemplate,
    });
    bind(apiDocsPlugin.externalRoutes, {
      registerApi: catalogImportPlugin.routes.importPage,
    });
  },
  // ...other options
});
```

Why this works:

* The `Provider` value replaces the default theme provider created by the app when the user chooses that theme.
* `UnifiedThemeProvider` makes the theme object available via React context so all Backstage UI components can consume it.

## How it works (APIs at a glance)

| API                      | Purpose                                                       | Example                                                            |
| ------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------ |
| `createBaseThemeOptions` | Produces base theme options compatible with Backstage UI      | `createBaseThemeOptions({ palette: palettes.light })`              |
| `createUnifiedTheme`     | Constructs a theme object that `UnifiedThemeProvider` accepts | `createUnifiedTheme({...})`                                        |
| `UnifiedThemeProvider`   | React provider to supply the theme to the component tree      | `<UnifiedThemeProvider theme={myTheme}>...</UnifiedThemeProvider>` |
| `palettes`               | Predefined palettes (e.g., `palettes.light`, `palettes.dark`) | `palettes.light`                                                   |

## Quick visual

After switching to a theme like `funTheme`, the UI reflects your palette and font choices across the catalog, navigation, and pages (primary/secondary colors, navigation highlights, and typography).

<Frame>
  <img alt="A web UI screenshot of &#x22;My Company Catalog&#x22; showing a table of components (app1, app2, auth-service, example-website, recommendation-service, shopping-cart) with columns for owner, type, lifecycle, description and action icons. The left sidebar shows navigation (Home, APIs, Docs) and a filter panel for kind, type and ownership." />
</Frame>

## Additional tips

* Provide multiple theme variants (light/dark) and let users switch between them in the UI.
* You can tweak many theme properties: typography, spacing, shadows, and fine-grained color values for specific Backstage components.
* During development, the Backstage dev server typically picks up frontend changes without restarting — but sometimes a rebuild or refresh may be required.
* For more details on theming primitives, see the `@backstage/theme` package documentation and the Backstage frontend docs:
  * [https://backstage.io/docs](https://backstage.io/docs)
  * [https://github.com/backstage/backstage/tree/master/plugins/theme](https://github.com/backstage/backstage/tree/master/plugins/theme) (repository examples)

<Callout icon="lightbulb">
  Summary: create your theme file under the frontend app, export theme objects using `createBaseThemeOptions` + `createUnifiedTheme`, and register them in `createApp(...)` with a `Provider` that wraps children with `UnifiedThemeProvider`.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/aad867ea-baf2-4ca7-b722-ad38ea794a7e/lesson/f5714cc0-79b1-4dcc-bdfa-c2f9a0749d3a" />
</CardGroup>
