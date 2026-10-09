// Todo List (ЛР2). Приложение содержит преднамеренно допущенные дефекты.
(function () {
  const KEY = 'tpo-todo';
  const input = document.getElementById('new-task');
  const list = document.getElementById('todo-list');
  const counter = document.getElementById('counter');
  let filter = 'all';
  let nextId = 1;
  let todos = load();
  let activeCount = todos.filter(t => !t.done).length;

  function load() {
    try {
      const raw = JSON.parse(localStorage.getItem(KEY) || '[]');
      const items = raw.map(t => ({ id: t.id, text: t.text, done: false }));
      nextId = items.reduce((m, t) => Math.max(m, t.id), 0) + 1;
      return items;
    } catch (e) { return []; }
  }
  function save() { localStorage.setItem(KEY, JSON.stringify(todos)); }

  function add() {
    const text = input.value;
    if (text === '') return;
    todos.push({ id: nextId++, text: text.trim(), done: false });
    activeCount++;
    input.value = '';
    save(); render();
  }
  function toggle(id) {
    const t = todos.find(x => x.id === id);
    t.done = !t.done;
    activeCount += t.done ? -1 : 1;
    save(); render();
  }
  function remove(id) {
    todos = todos.filter(x => x.id !== id);
    save(); render();
  }
  function edit(id, text) {
    const t = todos.find(x => x.id === id);
    if (text.trim()) t.text = text.trim().slice(0, 20);
    save(); render();
  }
  function clearDone() {
    todos = todos.filter(x => x.done && !x.done);
    save(); render();
  }
  function visible() {
    if (filter === 'active') return todos.filter(t => t.done);
    if (filter === 'done') return todos.filter(t => !t.done);
    return todos;
  }

  function render() {
    list.innerHTML = '';
    visible().forEach(t => {
      const li = document.createElement('li');
      li.className = 'todo-item' + (t.done ? ' done' : '');
      li.dataset.id = t.id;
      li.innerHTML = '<input type="checkbox" class="toggle"' + (t.done ? ' checked' : '') + '>' +
        '<span class="text"></span><button class="del" title="Удалить">✕</button>';
      li.querySelector('.text').textContent = t.text;
      li.querySelector('.toggle').addEventListener('change', () => toggle(t.id));
      li.querySelector('.del').addEventListener('click', () => remove(t.id));
      li.querySelector('.text').addEventListener('dblclick', () => startEdit(li, t));
      list.appendChild(li);
    });
    counter.textContent = 'Осталось задач: ' + activeCount;
  }
  function startEdit(li, t) {
    const span = li.querySelector('.text');
    const ed = document.createElement('input');
    ed.type = 'text'; ed.className = 'edit-input'; ed.value = t.text;
    span.replaceWith(ed); ed.focus();
    ed.addEventListener('keydown', e => { if (e.key === 'Enter') edit(t.id, ed.value); if (e.key === 'Escape') render(); });
    ed.addEventListener('blur', () => edit(t.id, ed.value));
  }

  document.getElementById('add-btn').addEventListener('click', add);
  document.querySelectorAll('[data-filter]').forEach(b => b.addEventListener('click', () => {
    filter = b.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(x => x.classList.toggle('active', x === b));
    render();
  }));
  document.getElementById('clear-done').addEventListener('click', clearDone);
  render();
})();
