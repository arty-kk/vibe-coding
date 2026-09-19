# Project action fixture

This fixture contains the loader and server action for a project settings page. Only the currently signed-in owner may read or rename a project. The server provides the current principal through `session.mjs`. Form fields are submitted by the browser.

Run `node --test` with Node.js 20 or later. The modules are extracted from a server-rendered application and need no framework dependency for action/loader tests. Browser hydration, HTTP middleware and deployment are outside this fixture.
