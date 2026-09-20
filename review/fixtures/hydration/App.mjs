import React, {useState} from 'react';
const h = React.createElement;
export function App() {
  const [theme, setTheme] = useState(() => typeof window === 'undefined' ? 'light' : (localStorage.getItem('theme') || 'light'));
  return h('main', null,
    h('h1', null, 'Theme preference'),
    h('p', {id: 'theme'}, 'Current theme: ' + theme),
    h('button', {onClick: () => {localStorage.setItem('theme', 'dark'); setTheme('dark');}}, 'Save dark theme'),
    h('button', {onClick: () => {localStorage.removeItem('theme'); setTheme('light');}}, 'Reset theme'));
}
