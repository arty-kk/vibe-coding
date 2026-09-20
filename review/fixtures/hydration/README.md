# React hydration fixture

The server renders the initial theme. The browser hydrates it and must preserve a saved preference across reloads without a recoverable hydration error. Both theme controls must remain interactive.

Run `npm ci` and `npm start`, then open the printed loopback URL in a browser. Save the dark theme and reload; also reset it and reload. The page displays recoverable errors reported by React. This uses real `renderToString` and `hydrateRoot`, not a mocked rendering API.

Dependencies are pinned in package.json and package-lock.json. This fixture does not include a production framework, server actions, authentication, streaming SSR or deployment configuration.
