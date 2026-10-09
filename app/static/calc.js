// Калькулятор (ЛР1). Операции выполняются последовательно: 2 + 3 × 4 = 20.
(function () {
  const MAX_DIGITS = 12;
  const LIMIT = 1e12;
  const SYM = { '+': '+', '-': '−', '*': '×', '/': '÷' };
  const display = document.getElementById('display');
  const history = document.getElementById('history');

  let current = '0';      // число на экране (строка)
  let stored = null;      // первый операнд
  let op = null;          // ожидающая операция
  let fresh = false;      // следующий ввод начинает новое число
  let error = false;

  function fmt(n) {
    const r = Math.round(n * 1e10) / 1e10;          // убираем 0.1+0.2 = 0.30000000000000004
    return String(r).replace('.', ',');
  }
  function num(s) { return parseFloat(s.replace(',', '.')); }
  function render() { display.textContent = current; }
  function showError(msg) { current = msg; error = true; stored = null; op = null; history.textContent = ''; render(); }
  function resetIfError() { if (error) { current = '0'; error = false; fresh = false; } }

  function compute(a, b, o) {
    switch (o) {
      case '+': return a + b;
      case '-': return a - b;
      case '*': return a * b;
      case '/': if (b === 0) throw new Error('div0'); return a / b;
    }
  }

  function inputDigit(d) {
    resetIfError();
    if (fresh) { current = '0'; fresh = false; }
    const digits = current.replace(/[-,]/g, '').length;
    if (digits >= MAX_DIGITS) return;
    current = current === '0' ? d : (current === '-0' ? '-' + d : current + d);
    render();
  }
  function inputDot() {
    resetIfError();
    if (fresh) { current = '0'; fresh = false; }
    if (!current.includes(',')) current += ',';
    render();
  }
  function setOp(o) {
    if (error) return;
    if (op !== null && !fresh) {
      if (!evaluate(false)) return;
    }
    stored = num(current); op = o; fresh = true;
    history.textContent = fmt(stored) + ' ' + SYM[o];
  }
  function evaluate(final) {
    if (op === null || error) return true;
    const b = num(current);
    let res;
    try { res = compute(stored, b, op); }
    catch (e) { showError('Ошибка: деление на 0'); return false; }
    if (!isFinite(res) || Math.abs(res) >= LIMIT) { showError('Переполнение'); return false; }
    if (final) history.textContent = fmt(stored) + ' ' + SYM[op] + ' ' + fmt(b) + ' =';
    current = fmt(res); stored = res; render();
    if (final) { op = null; stored = null; }
    fresh = true;
    return true;
  }
  function clearAll() { current = '0'; stored = null; op = null; fresh = false; error = false; history.textContent = ''; render(); }
  function clearEntry() { resetIfError(); current = '0'; render(); }
  function backspace() {
    if (error) { clearAll(); return; }
    if (fresh) return;
    current = current.length > 1 ? current.slice(0, -1) : '0';
    if (current === '-') current = '0';
    render();
  }
  function toggleSign() {
    if (error || current === '0') return;
    current = current.startsWith('-') ? current.slice(1) : '-' + current;
    render();
  }

  document.querySelector('.keys').addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.digit) inputDigit(b.dataset.digit);
    else if (b.dataset.op) setOp(b.dataset.op);
    else ({ clear: clearAll, ce: clearEntry, back: backspace, sign: toggleSign, dot: inputDot,
            eq: () => evaluate(true) })[b.dataset.action]();
  });
  document.addEventListener('keydown', (e) => {
    if (/^[0-9]$/.test(e.key)) inputDigit(e.key);
    else if ('+-*/'.includes(e.key)) setOp(e.key);
    else if (e.key === 'Enter' || e.key === '=') { e.preventDefault(); evaluate(true); }
    else if (e.key === 'Escape') clearAll();
    else if (e.key === 'Backspace') backspace();
    else if (e.key === '.' || e.key === ',') inputDot();
  });
  render();
})();
