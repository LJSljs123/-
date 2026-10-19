(function () {
  'use strict';
  const KEY = 'miying-story-trail-v1';
  const names = ['source', 'case', 'boundary'];
  let state = [false, false, false];

  function read() {
    try {
      const saved = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (Array.isArray(saved)) state = names.map((_, i) => saved[i] === true);
    } catch (_) {}
  }
  function render() {
    const status = document.getElementById('journey-status');
    const note = document.getElementById('note');
    if (!status) return;
    const complete = state.every(Boolean);
    status.hidden = !complete;
    if (note) note.hidden = complete;
    if (complete) status.textContent = '你已看完三种记载、一处分歧，并把结论留在证据边界内。';
  }
  function complete(step) {
    const index = Number(step) - 1;
    if (index < 0 || index >= state.length || state[index]) return;
    state[index] = true;
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (_) {}
    render();
  }

  read();
  window.MIYING_TRAIL = { complete };
  render();

  if (location.pathname.endsWith('/') || /\/index\.html?$/i.test(location.pathname)) {
    document.addEventListener('click', event => {
      const link = event.target.closest('#tip a[target="_blank"]');
      if (link) complete(1);
    });
  }
})();
