import React from 'react';
import {hydrateRoot} from 'react-dom/client';
import {App} from './App.mjs';
let errors = 0;
hydrateRoot(document.getElementById('root'), React.createElement(App), {
  onRecoverableError(error) {
    document.getElementById('errors').textContent = 'Hydration errors: ' + (++errors);
    document.getElementById('error-detail').textContent = error.message;
  }
});
