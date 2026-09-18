(() => {
'use strict';
const DATA = JSON.parse(document.getElementById('bible-data').textContent);
const PAGES = DATA.pages;
const BY_ID = Object.fromEntries(PAGES.map(p => [p.id, p]));
const ORDER = PAGES.map(p => p.id);
const PARTS = DATA.parts;
const PART = Object.fromEntries(PARTS.map(p => [p.key, p]));
const ANCHOR = Object.fromEntries(DATA.anchors.map(a => [a.n, a]));
const OTHER_CARDS = (DATA.aliases || []).filter(a => BY_ID[a.pid]).map(a => [a.n, a.title, a.pid, a.anchor]);
const SITE = BY_ID.home ? BY_ID.home.title : 'Revision Bible';
const CORE = DATA.anchors.filter(a => a.group === 'core').length;

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const icon = n => `<svg aria-hidden="true"><use href="#i-${n}"/></svg>`;
const store = {
  get(k, d) { try { const v = localStorage.getItem('dsab:' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem('dsab:' + k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } }
};
const mqDrawer = matchMedia('(max-width: 1023px)');

const main = $('#main'), rail = $('[data-rail]'), sidebar = $('[data-sidebar]'), tocRail = $('[data-toc-rail]');
const otpBar = $('[data-otp-bar]'), otpBtn = $('[data-otp-btn]'), otpPanel = $('[data-otp-panel]'), otpCurrent = $('[data-otp-current]');
const pager = $('[data-pager]'), crumb = $('[data-crumb]'), progress = $('[data-progress]'), scrim = $('[data-scrim]');
const menuBtn = $('[data-open-drawer]'), topbar = $('.topbar');

let current = null, heads = [], activeId = null;

/* ------------------------------------------------ labels */
function itemLabel(id) {
  const p = BY_ID[id];
  if (id === 'home') return { num: '', t: 'Home', s: '' };
  if (id === 'how-to-use') return { num: '0', t: p.title, s: '' };
  if (p.kind === 'part') return { num: '', t: 'Overview', s: '' };
  const num = p.numeral.replace(/^§/, '').replace(/^Card /, '').replace(/^Appendix /, '');
  return { num, t: p.title, s: p.sub, cov: p.cov || '' };
}
function badge(p) { return p.id === 'home' ? 'Home' : (p.numeral || '').replace('Appendix ', 'App. '); }

/* ------------------------------------------------ rail + sidebar */
function renderRail(active) {
  rail.innerHTML = PARTS.map(p => `<button type="button" role="tab" class="tab" data-part="${p.key}" data-tab="${p.key}" aria-selected="${p.key === active}" aria-label="${esc(p.key === '0' ? 'Start' : p.key === 'App' ? 'Appendices' : 'Part ' + p.key)}: ${esc(p.title)}"><span class="t-num">${esc(p.tab)}</span><span class="t-label">${esc(p.label)}</span></button>`).join('');
}
function renderSidebar(key) {
  const part = PART[key];
  sidebar.dataset.part = key;
  const headLabel = /^(0|App)$/.test(key) || !/^[IVX]+$/.test(key) ? '' : 'Part ' + key;
  let html = `<a class="sb-head" href="#/${part.items[0]}">${headLabel ? `<span class="sb-part">${esc(headLabel)}</span>` : ''}<span class="sb-title">${esc(part.title)}</span></a><ul class="sb-list">`;
  html += part.items.map(id => {
    const l = itemLabel(id);
    return `<li><a class="sb-item" href="#/${id}"${id === current ? ' aria-current="page"' : ''}><span class="sb-num">${esc(l.num)}</span><span><span class="sb-t">${esc(l.t)}</span>${l.s ? `<span class="sb-s">${esc(l.s)}</span>` : ''}</span><span class="sb-cov">${esc(l.cov || '')}</span></a></li>`;
  }).join('') + '</ul>';
  if (OTHER_CARDS.length && part.items.some(id => BY_ID[id] && BY_ID[id].kind === 'card')) {
    html += `<p class="sb-sub">Built in other parts</p><ul class="sb-list muted">` + OTHER_CARDS.map(([n, t, pid, a]) =>
      `<li><a class="sb-item" href="#/${pid}${a ? '/' + a : ''}" data-part="${BY_ID[pid].part}"><span class="sb-num">${n}</span><span class="sb-t">${esc(t)}</span><span class="sb-cov">${esc(BY_ID[pid].numeral)}</span></a></li>`).join('') + '</ul>';
  }
  sidebar.innerHTML = html;
}
rail.addEventListener('click', e => {
  const t = e.target.closest('[data-tab]');
  if (!t) return;
  const key = t.dataset.tab;
  if (mqDrawer.matches) { renderRail(key); renderSidebar(key); const f = $('.sb-item', sidebar); if (f) f.focus(); }
  else location.hash = '#/' + PART[key].items[0];
});
rail.addEventListener('keydown', e => {
  if (!['ArrowDown', 'ArrowUp'].includes(e.key)) return;
  const tabs = $$('.tab', rail); const i = tabs.indexOf(document.activeElement);
  if (i < 0) return;
  e.preventDefault(); tabs[(i + (e.key === 'ArrowDown' ? 1 : tabs.length - 1)) % tabs.length].focus();
});

/* ------------------------------------------------ drawer */
function openDrawer() {
  const key = BY_ID[current].part;
  renderRail(key); renderSidebar(key);
  document.body.classList.add('drawer-open'); scrim.hidden = false; menuBtn.setAttribute('aria-expanded', 'true');
  const a = $('[aria-current="page"]', sidebar) || $('.sb-item', sidebar);
  if (a) setTimeout(() => a.focus({ preventScroll: false }), 30);
}
function closeDrawer() {
  if (!document.body.classList.contains('drawer-open')) return;
  document.body.classList.remove('drawer-open'); scrim.hidden = true; menuBtn.setAttribute('aria-expanded', 'false');
}
menuBtn.addEventListener('click', () => document.body.classList.contains('drawer-open') ? closeDrawer() : openDrawer());
scrim.addEventListener('click', closeDrawer);
mqDrawer.addEventListener && mqDrawer.addEventListener('change', () => { closeDrawer(); if (current) { renderRail(BY_ID[current].part); renderSidebar(BY_ID[current].part); } });

/* ------------------------------------------------ toc + otp */
function tocLinks(pg) {
  return (pg.toc || []).map(t => `<a href="#/${pg.id}/${t.id}" data-toc="${t.id}" class="lvl${t.level}">${esc(t.short)}</a>`).join('');
}
function renderToc(pg) {
  const n = (pg.toc || []).length;
  tocRail.innerHTML = n ? `<p class="toc-title">On this page</p><nav class="toc">${tocLinks(pg)}</nav>` : '';
  otpPanel.innerHTML = n ? `<nav class="toc">${tocLinks(pg)}</nav>` : '';
  otpBar.hidden = n < 2;
  document.documentElement.style.setProperty('--otp', otpBar.hidden || window.innerWidth >= 1280 ? '0px' : '42px');
  closeOtp();
}
function toggleOtp(open) {
  const o = open === undefined ? otpPanel.hidden : open;
  otpPanel.hidden = !o; otpBtn.setAttribute('aria-expanded', String(o));
  if (o) { const a = $('a.active', otpPanel); if (a) a.scrollIntoView({ block: 'nearest' }); }
}
function closeOtp() { if (!otpPanel.hidden) toggleOtp(false); }
otpBtn.addEventListener('click', () => toggleOtp());

function offset() { return topbar.offsetHeight + (otpBar.hidden || otpBar.offsetParent === null ? 0 : otpBar.offsetHeight); }
function collectHeads() { heads = $$('.page h2.sec[id], .page h3.sec[id]', main); }
let saveT = null;
function onScroll() {
  const doc = document.documentElement;
  const max = doc.scrollHeight - window.innerHeight;
  progress.style.transform = `scaleX(${max > 0 ? Math.min(1, window.scrollY / max) : 0})`;
  const off = offset() + 24;
  let act = null;
  for (const h of heads) { if (!h.offsetHeight) continue; if (h.getBoundingClientRect().top <= off) act = h; else break; }
  const id = act ? act.id : null;
  if (id === activeId) return;
  activeId = id;
  $$('[data-toc]').forEach(a => a.classList.toggle('active', a.dataset.toc === id));
  const pg = BY_ID[current];
  const t = (pg.toc || []).find(x => x.id === id);
  otpCurrent.textContent = t ? t.short : (pg.toc && pg.toc[0] ? 'Top of page' : '');
  const ra = $('a.active', tocRail);
  if (ra && (ra.offsetTop < tocRail.scrollTop + 40 || ra.offsetTop > tocRail.scrollTop + tocRail.clientHeight - 60)) tocRail.scrollTop = ra.offsetTop - 120;
  clearTimeout(saveT);
  saveT = setTimeout(() => { if (current && current !== 'home') store.set('last', { pid: current, anchor: activeId }); }, 400);
}
let ticking = false;
window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; onScroll(); }); } }, { passive: true });
window.addEventListener('resize', () => { if (current) document.documentElement.style.setProperty('--otp', otpBar.hidden || window.innerWidth >= 1280 ? '0px' : '42px'); });

/* ------------------------------------------------ pager */
function renderPager(pid) {
  const i = ORDER.indexOf(pid);
  const cell = (id, dir) => {
    const p = BY_ID[id];
    return `<a class="pg pg-${dir}" href="#/${id}" data-part="${p.part}"><span class="pg-dir">${dir === 'prev' ? icon('left') + 'Previous' : 'Next' + icon('right')}</span><span class="pg-t"><span class="pg-n">${esc(badge(p))}</span> ${esc(p.title)}</span></a>`;
  };
  pager.innerHTML = (i > 0 ? cell(ORDER[i - 1], 'prev') : '') + (i < ORDER.length - 1 ? cell(ORDER[i + 1], 'next') : '');
}
function step(d) { const i = ORDER.indexOf(current) + d; if (i >= 0 && i < ORDER.length) location.hash = '#/' + ORDER[i]; }

/* ------------------------------------------------ router */
function parseHash() {
  let h = location.hash.replace(/^#\/?/, '');
  try { h = decodeURIComponent(h); } catch (e) { /* keep raw */ }
  const [pid, anchor] = h.split('/');
  return { pid: BY_ID[pid] ? pid : 'home', anchor: BY_ID[pid] && anchor ? anchor : null };
}
function mount(pid) {
  const tpl = document.getElementById('tpl-' + pid);
  main.replaceChildren(tpl.content.cloneNode(true));
  current = pid; activeId = undefined;
  const pg = BY_ID[pid];
  document.body.dataset.part = pg.part;
  document.title = (pid === 'home' ? '' : `${pg.numeral ? pg.numeral + ' ' : ''}${pg.title} · `) + SITE;
  crumb.textContent = pid === 'home' ? SITE : `${badge(pg)}  ${pg.title}`;
  renderEditBar(pg);
  renderRail(pg.part); renderSidebar(pg.part); renderToc(pg); renderPager(pid);
  hydrate(pid);
  collectHeads();
  if (pid !== 'home') {
    store.set('last', { pid, anchor: null });
    const rec = store.get('recent', []).filter(x => x !== pid); rec.unshift(pid); store.set('recent', rec.slice(0, 6));
  }
  const h1 = $('h1', main); if (h1) h1.focus({ preventScroll: true });
}
function jumpTo(id, flash) {
  const el = document.getElementById(id);
  if (!el || !main.contains(el)) return false;
  el.scrollIntoView({ block: 'start' });
  if (flash) { el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); setTimeout(() => el.classList.remove('flash'), 2500); }
  return true;
}
function route(again) {
  const { pid, anchor } = parseHash();
  const changed = pid !== current;
  if (changed) mount(pid);
  closeDrawer(); closeOtp();
  if (anchor) requestAnimationFrame(() => { jumpTo(anchor, /^b\d+$/.test(anchor)); onScroll(); });
  else if (changed || again) { window.scrollTo(0, 0); onScroll(); }
}
window.addEventListener('hashchange', () => route(false));
document.addEventListener('click', e => {
  const a = e.target.closest('a[href^="#/"]');
  if (a && a.getAttribute('href') === location.hash) { e.preventDefault(); route(true); }
});

/* ------------------------------------------------ edit on GitHub */
const editbar = $('[data-editbar]');
function ghUrl(kind, path, extra) { const r = DATA.repo; return `${r.url}/${kind}/${encodeURIComponent(r.branch).replace(/%2F/g, '/')}/${path.split('/').map(encodeURIComponent).join('/')}${extra || ''}`; }
function newPageTemplate(part) {
  const nums = PAGES.map(p => p.numeral || '');
  const maxSec = Math.max(0, ...nums.map(n => (/^§(\d+)$/.exec(n) || [0, 0])[1] * 1));
  const maxCard = Math.max(0, ...nums.map(n => (/^Card (\d+)$/.exec(n) || [0, 0])[1] * 1), ...OTHER_CARDS.map(c => c[0]));
  const letters = nums.map(n => (/^Appendix ([A-Z])$/.exec(n) || [0, ''])[1]).filter(Boolean).sort();
  const nextApp = letters.length ? String.fromCharCode(letters[letters.length - 1].charCodeAt(0) + 1) : 'A';
  const hasCards = part.items.some(id => BY_ID[id] && BY_ID[id].kind === 'card');
  const numeral = part.key === 'App' ? `Appendix ${nextApp}` : hasCards ? `Card ${maxCard + 1}` : /^[IVX]+$/.test(part.key) ? `§${maxSec + 1}` : '';
  const count = part.items.filter(id => id !== 'home' && BY_ID[id] && BY_ID[id].kind !== 'part').length + 1;
  const stem = part.key === 'App' ? `${nextApp.toLowerCase()}-new-page` : `${String(hasCards ? maxCard + 1 : /^§/.test(numeral) ? maxSec + 1 : count).padStart(2, '0')}-new-page`;
  const body = `---\nnumeral: ${numeral}\ntitle: New page title\n---\n\nFirst paragraph. See EDITING.md in the repository for callouts, tables and templates.\n\n## A section\n\n- A point\n- Another point\n\n\`\`\`java\n// a template you want to blank-page\n\`\`\`\n`;
  return { stem, body };
}
function renderEditBar(pg) {
  if (!DATA.repo || !pg.src) { editbar.hidden = true; return; }
  const part = PARTS.find(p => p.key === pg.part) || PARTS[0];
  const t = newPageTemplate(part);
  const add = ghUrl('new', part.folder, `?filename=${encodeURIComponent(t.stem + '.md')}&value=${encodeURIComponent(t.body)}`);
  const isPartFile = /\/_part\.md$/.test(pg.src), isHome = pg.id === 'home';
  editbar.innerHTML =
    `<a class="eb-btn" href="${ghUrl('edit', pg.src)}" target="_blank" rel="noopener">${icon('edit')}Edit this page</a>` +
    (isHome ? '' : `<a class="eb-btn" href="${add}" target="_blank" rel="noopener">${icon('plus')}Add a page to ${esc(part.key === 'App' ? 'the appendices' : /^[IVX]+$/.test(part.key) ? 'Part ' + part.key : part.title)}</a>`) +
    (isHome || isPartFile ? '' : `<a class="eb-btn danger" href="${ghUrl('delete', pg.src)}" target="_blank" rel="noopener">${icon('trash')}Delete this page</a>`) +
    '<p class="eb-note">Opens the Markdown file on GitHub. Commit your change and the site rebuilds in about a minute.</p>';
  editbar.hidden = false;
}
(function renderFoot() {
  const f = $('[data-foot]'); if (!f || !DATA.built) return;
  const d = new Date(DATA.built.at);
  const when = isNaN(d) ? '' : d.toLocaleString(undefined, { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
  const sha = DATA.built.sha ? (DATA.repo ? ` from <a href="${DATA.repo.url}/commit/${DATA.built.sha}" target="_blank" rel="noopener">${DATA.built.sha}</a>` : ` from ${DATA.built.sha}`) : '';
  f.innerHTML = `Built ${esc(when)}${sha}.` + (DATA.repo ? ` <a href="${DATA.repo.url}" target="_blank" rel="noopener">Source on GitHub</a>` : '');
})();
function exportLog() {
  const blob = new Blob([JSON.stringify({ app: 'dsa-revision-bible', v: 1, exported: new Date().toISOString(), log: Anchors.log }, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = `anchor-log-${todayStr()}.json`;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  toast('Exported the anchor log. Import it on your other device.');
}
function importLog(file) {
  const rd = new FileReader();
  rd.onload = () => {
    try {
      const d = JSON.parse(rd.result);
      const incoming = cleanLog(d.log || d);
      const before = Object.values(Anchors.log).reduce((s, v) => s + v.length, 0);
      Anchors.replaceAll(mergeLogs(Anchors.log, incoming));
      const after = Object.values(Anchors.log).reduce((s, v) => s + v.length, 0);
      toast(`Imported. ${after - before} new date${after - before === 1 ? '' : 's'} added.`);
    } catch (e) { toast('That file is not an anchor log export.'); }
  };
  rd.readAsText(file);
}

/* ------------------------------------------------ hydrate per page */
function hydrate(pid) {
  Anchors.editing = false;
  Anchors.paint();
  if (pid === 'home') {
    const last = store.get('last', null), box = $('[data-continue]', main);
    if (box && last && BY_ID[last.pid] && last.pid !== 'home') {
      const p = BY_ID[last.pid];
      box.hidden = false;
      box.innerHTML = `<a href="#/${p.id}${last.anchor ? '/' + esc(last.anchor) : ''}" data-part="${p.part}"><span class="c-label">Continue where you left off</span><span class="c-t"><span class="c-n">${esc(badge(p))}</span> ${esc(p.title)}</span></a>`;
    }
  }
  if ($('.tbl-index', main)) applyFilter('all');
  const tt = $('.tt-actions', main);
  if (tt && !$('[data-export]', tt)) {
    tt.insertAdjacentHTML('beforeend', '<button type="button" class="ghost-btn" data-export>Export log</button><label class="ghost-btn" style="display:inline-flex;align-items:center;cursor:pointer">Import log<input type="file" accept="application/json,.json" data-import hidden></label>');
    $('[data-export]', tt).addEventListener('click', exportLog);
    $('[data-import]', tt).addEventListener('change', e => { if (e.target.files[0]) importLog(e.target.files[0]); e.target.value = ''; });
  }
}

/* ------------------------------------------------ content interactions */
function fallbackCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  let ok = false; try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
  ta.remove(); return ok;
}
async function copyCode(btn) {
  const pre = btn.closest('figure').querySelector('pre');
  const text = pre.innerText.replace(/\n$/, '');
  let ok = false;
  try { await navigator.clipboard.writeText(text); ok = true; } catch (e) { ok = fallbackCopy(text); }
  if (!ok) { const r = document.createRange(); r.selectNodeContents(pre); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  btn.textContent = ok ? 'Copied' : 'Selected, press Ctrl C';
  setTimeout(() => { btn.textContent = 'Copy'; }, 1800);
}
main.addEventListener('click', e => {
  const t = e.target;
  let el;
  if ((el = t.closest('.copy-btn'))) return void copyCode(el);
  if ((el = t.closest('.reveal-btn'))) { const f = el.closest('figure'); f.classList.add('revealed'); const c = $('.copy-btn', f); if (c) c.focus(); return; }
  if ((el = t.closest('.log-btn'))) return void Anchors.toggleToday(+el.dataset.anchor);
  if ((el = t.closest('[data-rm]'))) return void Anchors.remove(+el.dataset.rm, el.dataset.date);
  if ((el = t.closest('.fchip'))) return void applyFilter(el.dataset.filter);
  if ((el = t.closest('[data-edit-dates]'))) {
    Anchors.editing = !Anchors.editing;
    el.setAttribute('aria-pressed', String(Anchors.editing)); el.textContent = Anchors.editing ? 'Done editing' : 'Edit dates';
    Anchors.paint();
  }
});
function applyFilter(f) {
  $$('.fchip', main).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === f)));
  let shown = 0, total = 0;
  $$('.tbl-index', main).forEach(tbl => {
    let vis = 0;
    tbl.querySelectorAll('tbody tr').forEach(tr => {
      total++;
      const p = tr.dataset.p, s = tr.dataset.status;
      const ok = f === 'all' || (f === 'A' && p === 'A') || (f === '1' && p === '1') || (f === 'todo' && s === 'Not started') || (f === 'x' && p === '×');
      tr.hidden = !ok; if (ok) { vis++; shown++; }
    });
    const wrap = tbl.closest('.table-wrap'); wrap.hidden = !vis;
    const h = wrap.previousElementSibling; if (h && h.matches('h2, h3')) h.hidden = !vis;
  });
  const c = $('[data-filter-count]', main);
  if (c) c.textContent = f === 'all' ? `${total} problems` : `${shown} of ${total}`;
  collectHeads();
}

/* ------------------------------------------------ cover templates */
const coverBtn = $('[data-cover-toggle]');
let coverOn = !!store.get('cover', false);
function setCover(on) {
  coverOn = on;
  document.body.classList.toggle('cover-on', on);
  coverBtn.setAttribute('aria-pressed', String(on));
  coverBtn.title = on ? 'Templates are covered until you reveal them (C)' : 'Cover templates (C)';
  store.set('cover', on);
  if (on) $$('.code.revealed', main).forEach(f => f.classList.remove('revealed'));
}
coverBtn.addEventListener('click', () => { setCover(!coverOn); toast(coverOn ? 'Templates covered. Write each from memory, then reveal.' : 'Templates uncovered.'); });

/* ------------------------------------------------ toast */
const toastEl = $('[data-toast]');
let toastT = null;
function toast(msg, action) {
  toastEl.innerHTML = `<span>${esc(msg)}</span>` + (action ? `<button type="button" class="toast-act">${esc(action.label)}</button>` : '');
  toastEl.hidden = false;
  if (action) $('.toast-act', toastEl).onclick = () => { hideToast(); action.fn(); };
  clearTimeout(toastT); toastT = setTimeout(hideToast, action ? 6000 : 3200);
}
function hideToast() { toastEl.hidden = true; }

/* ------------------------------------------------ timer */
const T = { min: store.get('timerMin', 15), left: 0, endAt: 0, running: false, done: false, iv: null };
T.left = T.min * 60000;
const timerBtn = $('[data-timer-btn]'), timerPop = $('[data-timer-pop]'), timerRead = $('[data-timer-read]'), timerBig = $('[data-timer-big]'), timerStart = $('[data-timer-start]');
let actx = null;
const fmtT = ms => { const s = Math.max(0, Math.ceil(ms / 1000)); return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`; };
function paintTimer() {
  timerRead.textContent = T.done ? 'Cap hit' : fmtT(T.left);
  timerBig.textContent = fmtT(T.left);
  timerStart.textContent = T.running ? 'Pause' : (T.done ? 'Start again' : T.left < T.min * 60000 ? 'Resume' : 'Start');
  timerBtn.classList.toggle('running', T.running); timerBtn.classList.toggle('done', T.done);
  $$('[data-min]', timerPop).forEach(b => b.setAttribute('aria-checked', String(+b.dataset.min === T.min)));
}
function ensureAudio() { try { actx = actx || new (window.AudioContext || window.webkitAudioContext)(); if (actx.state === 'suspended') actx.resume(); } catch (e) { actx = null; } }
function beep() {
  if (!actx) return;
  const t0 = actx.currentTime;
  [0, 0.3, 0.6].forEach(d => {
    const o = actx.createOscillator(), g = actx.createGain();
    o.type = 'sine'; o.frequency.value = 880;
    g.gain.setValueAtTime(0.0001, t0 + d); g.gain.exponentialRampToValueAtTime(0.2, t0 + d + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t0 + d + 0.24);
    o.connect(g); g.connect(actx.destination); o.start(t0 + d); o.stop(t0 + d + 0.26);
  });
}
function tick() {
  if (!T.running) return;
  T.left = T.endAt - Date.now();
  if (T.left <= 0) { T.left = 0; T.running = false; T.done = true; clearInterval(T.iv); beep(); toast('Cap hit. Stop, log the failure, move to the next anchor.'); }
  paintTimer();
}
function timerReset() { clearInterval(T.iv); T.running = false; T.done = false; T.left = T.min * 60000; paintTimer(); }
function timerToggle() {
  if (T.running) { T.left = T.endAt - Date.now(); T.running = false; clearInterval(T.iv); paintTimer(); return; }
  if (T.done) timerReset();
  ensureAudio();
  T.endAt = Date.now() + T.left; T.running = true; clearInterval(T.iv); T.iv = setInterval(tick, 250); paintTimer();
}
function toggleTimerPop(open) {
  const o = open === undefined ? timerPop.hidden : open;
  timerPop.hidden = !o; timerBtn.setAttribute('aria-expanded', String(o));
  if (o) setTimeout(() => timerStart.focus(), 20);
}
timerBtn.addEventListener('click', () => toggleTimerPop());
timerStart.addEventListener('click', timerToggle);
$('[data-timer-reset]').addEventListener('click', timerReset);
timerPop.addEventListener('click', e => {
  const b = e.target.closest('[data-min]');
  if (b) { T.min = +b.dataset.min; store.set('timerMin', T.min); timerReset(); }
  if (e.target.closest('a')) toggleTimerPop(false);
});
document.addEventListener('click', e => {
  if (!timerPop.hidden && !e.target.closest('.timer-wrap')) toggleTimerPop(false);
  if (!otpPanel.hidden && !e.target.closest('.otp-bar')) closeOtp();
});

/* ------------------------------------------------ anchors (Appendix C log) */
const LABEL = { never: 'Not logged', fresh: 'Fresh', holding: 'Holding', fire: 'On fire' };
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function todayStr() { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; }
function fmtDate(s) { const [y, m, d] = s.split('-').map(Number); return `${d} ${MONTHS[m - 1]}` + (y !== new Date().getFullYear() ? ` ’${String(y).slice(2)}` : ''); }
function daysSince(s) { const [y, m, d] = s.split('-').map(Number); const t = new Date(); return Math.round((new Date(t.getFullYear(), t.getMonth(), t.getDate()) - new Date(y, m - 1, d)) / 86400000); }
function cleanLog(l) {
  const out = {};
  if (!l || typeof l !== 'object') return out;
  for (const k of Object.keys(l)) {
    if (!ANCHOR[k] || !Array.isArray(l[k])) continue;
    const v = [...new Set(l[k].filter(x => typeof x === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(x)))].sort().slice(-12);
    if (v.length) out[k] = v;
  }
  return out;
}
const sameLog = (a, b) => JSON.stringify(cleanLog(a)) === JSON.stringify(cleanLog(b));
function mergeLogs(a, b) { const out = {}; for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) out[k] = [...(a[k] || []), ...(b[k] || [])]; return cleanLog(out); }

const Anchors = {
  log: cleanLog(store.get('anchors', {})), mode: 'local', ref: null, chain: Promise.resolve(), editing: false,
  dates(n) { return this.log[n] || []; },
  last(n) { const d = this.dates(n); return d.length ? d[d.length - 1] : null; },
  state(n) { const l = this.last(n); if (!l) return 'never'; const ds = daysSince(l); return ds <= 7 ? 'fresh' : ds <= 30 ? 'holding' : 'fire'; },
  toggleToday(n) {
    const t = todayStr(), name = ANCHOR[n] ? ANCHOR[n].name : '#' + n;
    const has = this.dates(n).includes(t);
    this.put(n, has ? this.dates(n).filter(x => x !== t) : [...this.dates(n), t]);
    if (has) toast(`Removed today’s log for ${name}.`);
    else toast(`Logged a cold solve: ${name}.`, { label: 'Undo', fn: () => this.put(n, this.dates(n).filter(x => x !== t)) });
  },
  remove(n, date) { this.put(n, this.dates(n).filter(x => x !== date)); },
  replaceAll(log) {
    this.log = cleanLog(log);
    store.set('anchors', this.log);
    if (this.mode === 'db' && this.ref) {
      const body = { v: 1, log: this.log, updated: Date.now() };
      this.chain = this.chain.then(() => this.ref.set(body)).catch(() => { store.set('anchorsDirty', true); this.mode = 'local'; this.paint(); });
    } else store.set('anchorsDirty', true);
    this.paint();
  },
  put(n, arr) {
    const next = Object.assign({}, this.log); next[n] = arr;
    this.log = cleanLog(next);
    store.set('anchors', this.log);
    if (this.mode === 'db' && this.ref) {
      const body = { v: 1, log: this.log, updated: Date.now() };
      this.chain = this.chain.then(() => this.ref.set(body)).catch(() => { store.set('anchorsDirty', true); this.mode = 'local'; this.paint(); toast('Couldn’t sync to your account. Saved on this device.'); });
    } else store.set('anchorsDirty', true);
    this.paint();
  },
  paint() {
    const t = todayStr();
    $$('.log-btn[data-anchor]', main).forEach(b => {
      const n = b.dataset.anchor, on = this.dates(n).includes(t), name = ANCHOR[n] ? ANCHOR[n].name : '';
      b.classList.toggle('on', on); b.textContent = on ? 'Logged today' : 'Log today'; b.setAttribute('aria-pressed', String(on));
      b.setAttribute('aria-label', (on ? 'Remove today’s cold solve for ' : 'Log a cold solve today for ') + name);
    });
    $$('[data-last]', main).forEach(s => { const l = this.last(s.dataset.last); s.textContent = l ? `Last ${fmtDate(l)}` : 'Not logged yet'; });
    $$('[data-dates]', main).forEach(td => {
      const n = td.dataset.dates, ds = this.dates(n).slice(-4);
      let h = '';
      for (let i = 0; i < 4; i++) {
        const d = ds[i];
        if (!d) h += '<span class="dbox" aria-hidden="true"></span>';
        else if (this.editing) h += `<button type="button" class="dbox filled" data-rm="${n}" data-date="${d}" aria-label="Remove ${fmtDate(d)}">${fmtDate(d)}${icon('close')}</button>`;
        else h += `<span class="dbox filled">${fmtDate(d)}</span>`;
      }
      const more = this.dates(n).length - 4;
      td.innerHTML = h + (more > 0 ? `<span class="st-sub">+${more} earlier</span>` : '');
    });
    $$('[data-state]', main).forEach(td => {
      const n = td.dataset.state, s = this.state(n), l = this.last(n);
      td.innerHTML = `<span class="st st-${s}">${LABEL[s]}</span>` + (l && s !== 'fresh' ? `<span class="st-sub">${daysSince(l)} days ago</span>` : '');
    });
    const sum = $('[data-anchor-summary]', main); if (sum) sum.innerHTML = this.summary();
    const sync = $('[data-sync]', main); if (sync) sync.textContent = this.mode === 'db' ? 'Synced to your account' : 'Saved in this browser. Use Export and Import to move it between devices.';
  },
  summary() {
    const c = { fresh: 0, holding: 0, fire: 0, never: 0 };
    DATA.anchors.filter(a => a.group === 'core').forEach(a => { c[this.state(a.n)]++; });
    const cells = DATA.anchors.map(a => { const s = this.state(a.n); return `<a class="acell st-${s}${a.group === 'later' ? ' later' : ''}" href="${a.href}" title="${a.n}. ${esc(a.name)}: ${LABEL[s]}"><span class="sr-only">${a.n}. ${esc(a.name)}: ${LABEL[s]}</span></a>`; }).join('');
    const none = c.never === CORE;
    return `<div class="as-stats"><p><strong>${c.fresh + c.holding}</strong> of ${CORE} cold-solved in the last 30 days</p>` +
      `<p><strong class="${c.fire ? 'tone-red' : ''}">${c.fire}</strong> on fire</p></div>` +
      (none ? '<p class="sec-note" style="margin:0!important">Nothing logged yet. Each time you cold-solve an anchor, press Log today on its card or in Appendix C.</p>' : '') +
      `<div class="agrid" aria-label="Anchor states">${cells}</div>` +
      `<p class="as-legend"><span><i class="st-fresh"></i>Fresh, 7 days or less</span><span><i class="st-holding"></i>Holding, 8 to 30 days</span><span><i class="st-fire"></i>On fire, over 30 days</span><span><i></i>Not logged</span></p>` +
      '<a class="text-link" href="#/app-c">Open the anchor log</a>';
  },
  async initSync() {
    const c = window.claude;
    if (!c || typeof c.use !== 'function') return;
    let db, user, uid, ref;
    try { [db, user] = await Promise.all([c.use('db'), c.use('user')]); } catch (e) { return; }
    if (!db || !user) return;
    try { uid = await user.id(); } catch (e) { return; }
    if (!uid) return;
    try { ref = db.doc('data/users/' + uid + '/anchors'); } catch (e) { return; }
    try {
      const snap = await ref.get();
      const remote = snap.exists ? cleanLog((snap.data() || {}).log) : {};
      const dirty = store.get('anchorsDirty', false);
      const merged = (!snap.exists || dirty) ? mergeLogs(remote, this.log) : remote;
      if (!snap.exists || !sameLog(merged, remote)) await ref.set({ v: 1, log: merged, updated: Date.now() });
      this.ref = ref; this.mode = 'db'; this.log = merged;
      store.set('anchors', merged); store.set('anchorsDirty', false);
      this.paint();
      ref.onSnapshot(s => {
        if (!s.exists) return;
        const l = cleanLog((s.data() || {}).log);
        if (!sameLog(l, this.log)) { this.log = l; store.set('anchors', l); this.paint(); }
      }, () => { this.mode = 'local'; this.paint(); });
    } catch (e) { this.mode = 'local'; this.paint(); }
  }
};

/* ------------------------------------------------ search */
const searchEl = $('[data-search]'), input = $('[data-search-input]'), results = $('[data-search-results]');
let index = null, hits = [], sel = 0, lastFocus = null;
const norm = s => String(s).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
  .replace(/[‘’`´]/g, "'").replace(/[“”]/g, '"').replace(/[–—−]/g, '-').replace(/\s+/g, ' ').trim();
function textOf(el) {
  if (el.matches('[data-code]')) return $('pre', el).textContent;
  if (el.tagName === 'TR') return Array.from(el.cells).map(td => cellText(td)).filter(Boolean).join(' | ');
  let t = el.textContent;
  $$('button, .code-head, .cover, .log-last, .st-sub', el).forEach(b => { if (b.textContent) t = t.replace(b.textContent, ' '); });
  return t;
}
function cellText(td) {
  let t = td.textContent;
  $$('button, .log-last, .st-sub', td).forEach(b => { if (b.textContent) t = t.replace(b.textContent, ' '); });
  return t.replace(/\s+/g, ' ').trim();
}
function buildIndex() {
  if (index) return;
  index = [];
  for (const pg of PAGES) {
    const tpl = document.getElementById('tpl-' + pg.id);
    if (!tpl) continue;
    const ptitle = `${pg.numeral} ${pg.title}`;
    index.push({ pid: pg.id, id: null, kind: 'page', title: ptitle, text: pg.sub || '', nt: norm(`${ptitle} ${pg.sub || ''} ${pg.kind === 'card' ? 'card pattern' : ''}`), nc: '' });
    let head = '', headId = null;
    for (const el of tpl.content.querySelectorAll('h2.sec[id], h3.sec[id], [data-b]')) {
      if (el.matches('h2.sec[id], h3.sec[id]')) {
        head = el.textContent.replace(/\s+/g, ' ').trim(); headId = el.id;
        index.push({ pid: pg.id, id: el.id, kind: 'head', title: head, text: '', nt: norm(head), nc: norm(ptitle) });
        continue;
      }
      const text = textOf(el).replace(/\s+/g, ' ').trim();
      if (!text || el.matches('.dq')) continue;
      index.push({ pid: pg.id, id: el.id, kind: el.matches('[data-code]') ? 'code' : 'text', title: head || pg.title, text, nt: norm(text), nc: norm(head + ' ' + ptitle) });
    }
  }
}
const W = { page: 60, head: 36, text: 12, code: 10 };
function scoreAll(q) {
  const nq = norm(q);
  const terms = nq.split(' ').filter(Boolean);
  if (!terms.length) return [];
  const out = [];
  for (const e of index) {
    let s = 0, own = 0, ok = true;
    for (const t of terms) {
      const inT = e.nt.includes(t), inC = e.nc.includes(t);
      if (!inT && !inC) { ok = false; break; }
      if (inT) { own++; s += W[e.kind]; const i = e.nt.indexOf(t); if (i === 0 || /[^a-z0-9]/.test(e.nt[i - 1])) s += 6; }
      else s += 3;
    }
    if (!ok || !own) continue;
    if (terms.length > 1 && e.nt.includes(nq)) s += e.kind === 'text' || e.kind === 'code' ? 18 : 40;
    if (e.kind === 'head' && e.nt === nq) s += 40;
    s -= Math.min(8, e.nt.length / 300);
    out.push([s, e]);
  }
  out.sort((a, b) => b[0] - a[0]);
  const per = {}, res = [];
  for (const [, e] of out) {
    per[e.pid] = (per[e.pid] || 0) + 1;
    if (per[e.pid] > 6) continue;
    res.push(e);
    if (res.length >= 40) break;
  }
  return res;
}
function direct(q) {
  const s = q.trim().toLowerCase().replace(/\s+/g, ' ');
  const tocHas = (pid, a) => (BY_ID[pid].toc || []).find(t => t.id === a);
  const mk = (pid, a, label) => (BY_ID[pid] ? { pid, id: a || null, kind: 'jump', title: label || BY_ID[pid].title } : null);
  let m;
  if ((m = s.match(/^§?\s*(\d{1,2})(?:\.(\d{1,2}))?$/))) {
    const pid = 's' + +m[1]; if (!BY_ID[pid]) return null;
    if (m[2]) { const a = `${+m[1]}-${+m[2]}`, t = tocHas(pid, a); return t ? mk(pid, a, t.short) : mk(pid); }
    return mk(pid);
  }
  if ((m = s.match(/^card\s*(\d{1,2})$/))) {
    const n = +m[1];
    if (n >= 1 && n <= 12) return mk('card-' + n);
    const o = OTHER_CARDS.find(x => x[0] === n); return o ? mk(o[2], o[3], `Card ${n}: ${o[1]}`) : null;
  }
  if ((m = s.match(/^(?:app(?:endix)?\.?\s*)([a-k])(\d{1,2})?$/))) {
    const pid = 'app-' + m[1]; const a = m[2] ? m[1] + m[2] : null; const t = a && tocHas(pid, a);
    return t ? mk(pid, a, t.short) : mk(pid);
  }
  if ((m = s.match(/^g([1-8])$/))) { const t = tocHas('s13', '13-' + m[1]); return mk('s13', '13-' + m[1], t && t.short); }
  if ((m = s.match(/^d([1-8])$/))) { const a = '14-' + (+m[1] + 2), t = tocHas('s14', a); return mk('s14', a, t && t.short); }
  if ((m = s.match(/^shape\s*([a-e])$/))) { const a = '12-' + ('abcde'.indexOf(m[1]) + 1), t = tocHas('s12', a); return mk('s12', a, t && t.short); }
  if ((m = s.match(/^(?:template\s*)?(\d{1,2})([a-e])$/))) { const pid = 'card-' + +m[1], a = 't-' + +m[1] + m[2]; if (!BY_ID[pid]) return null; const t = tocHas(pid, a); return t ? mk(pid, a, t.short) : null; }
  if ((m = s.match(/^part\s*(0|iv|iii|ii|i|[1-4])$/))) { const k = { '0': 'how-to-use', i: 'part-1', '1': 'part-1', ii: 'part-2', '2': 'part-2', iii: 'part-3', '3': 'part-3', iv: 'part-4', '4': 'part-4' }[m[1]]; return mk(k); }
  return null;
}
function snippet(text, q) {
  const terms = norm(q).split(' ').filter(t => t.length > 0).map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  if (!text) return '';
  const lower = text.toLowerCase();
  let first = -1;
  for (const t of norm(q).split(' ')) { const i = lower.indexOf(t); if (i >= 0 && (first < 0 || i < first)) first = i; }
  const start = Math.max(0, first - 50), end = Math.min(text.length, (first < 0 ? 0 : first) + 130);
  let s = esc(text.slice(start, end));
  if (terms.length) s = s.replace(new RegExp('(' + terms.map(t => esc(t).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')', 'gi'), '<mark>$1</mark>');
  return (start > 0 ? '… ' : '') + s + (end < text.length ? ' …' : '');
}
function hrefOf(h) { return '#/' + h.pid + (h.id ? '/' + h.id : ''); }
function renderResults(q) {
  const qs = q.trim();
  if (!qs) {
    const rec = store.get('recent', []).filter(id => BY_ID[id]);
    const sugg = [['app-a', null], ['app-e', null], ['s9', '9-2'], ['s20', null], ['app-k', null], ['s7', '7-7']];
    hits = [...rec.map(id => ({ pid: id, id: null, kind: 'recent', title: BY_ID[id].title })),
      ...sugg.filter(([id]) => !rec.includes(id) || true).map(([pid, a]) => ({ pid, id: a, kind: 'sugg', title: a ? ((BY_ID[pid].toc.find(t => t.id === a) || {}).short || BY_ID[pid].title) : BY_ID[pid].title }))];
    let html = '', i = 0;
    const group = (kind, label) => { const g = hits.filter(h => h.kind === kind); if (!g.length) return; html += `<p class="sr-group">${label}</p>`; g.forEach(h => { html += item(h, i++, ''); }); };
    hits = [...hits.filter(h => h.kind === 'recent'), ...hits.filter(h => h.kind === 'sugg')];
    group('recent', 'Recently opened'); group('sugg', 'Often needed');
    results.innerHTML = html; sel = 0; paintSel(); return;
  }
  const d = direct(qs);
  hits = scoreAll(qs);
  if (d) hits = [d, ...hits.filter(h => !(h.pid === d.pid && (h.id || null) === d.id))];
  if (!hits.length) { results.innerHTML = `<p class="sr-empty">No matches for “${esc(qs)}”. Try a pattern, a problem name, or a Java class like TreeMap.</p>`; return; }
  results.innerHTML = hits.map((h, i) => item(h, i, qs)).join('');
  sel = 0; paintSel();
}
function item(h, i, q) {
  const p = BY_ID[h.pid];
  const title = h.kind === 'page' ? p.title : h.title;
  const snip = h.kind === 'text' || h.kind === 'code' ? snippet(h.text, q) : (h.kind === 'page' && p.sub ? esc(p.sub) : (h.kind === 'head' || h.kind === 'jump' || h.kind === 'sugg') && h.id ? esc(p.title) : '');
  return `<div class="sr-item" role="option" id="sr-${i}" data-i="${i}" aria-selected="false"><span class="sr-badge" data-part="${p.part}">${esc(badge(p))}</span><span class="sr-title">${esc(title)}</span>${snip ? `<span class="sr-snip">${snip}</span>` : ''}</div>`;
}
function paintSel() {
  $$('.sr-item', results).forEach(el => el.setAttribute('aria-selected', String(+el.dataset.i === sel)));
  const el = $(`#sr-${sel}`, results);
  if (el) { el.scrollIntoView({ block: 'nearest' }); input.setAttribute('aria-activedescendant', el.id); }
}
function openHit(i) {
  const h = hits[i]; if (!h) return;
  closeSearch();
  const target = hrefOf(h);
  if (location.hash === target) route(true); else location.hash = target;
}
let qT = null;
input.addEventListener('input', () => { clearTimeout(qT); qT = setTimeout(() => renderResults(input.value), 60); });
input.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown') { e.preventDefault(); if (hits.length) { sel = (sel + 1) % hits.length; paintSel(); } }
  else if (e.key === 'ArrowUp') { e.preventDefault(); if (hits.length) { sel = (sel - 1 + hits.length) % hits.length; paintSel(); } }
  else if (e.key === 'Enter') { e.preventDefault(); clearTimeout(qT); if (input.value.trim() && !results.querySelector('.sr-item')) renderResults(input.value); openHit(sel); }
});
results.addEventListener('mousemove', e => { const it = e.target.closest('.sr-item'); if (it && +it.dataset.i !== sel) { sel = +it.dataset.i; paintSel(); } });
results.addEventListener('click', e => { const it = e.target.closest('.sr-item'); if (it) openHit(+it.dataset.i); });
function openSearch() {
  buildIndex();
  lastFocus = document.activeElement;
  searchEl.hidden = false; document.body.classList.add('no-scroll');
  input.value = ''; renderResults('');
  setTimeout(() => input.focus(), 10);
  closeDrawer(); toggleTimerPop(false);
}
function closeSearch() {
  if (searchEl.hidden) return;
  searchEl.hidden = true; document.body.classList.remove('no-scroll');
  if (lastFocus && lastFocus.focus && document.contains(lastFocus)) lastFocus.focus({ preventScroll: true });
}
$$('[data-open-search]').forEach(b => b.addEventListener('click', openSearch));
$$('[data-close-search]').forEach(b => b.addEventListener('click', closeSearch));

/* ------------------------------------------------ keyboard */
const isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
const kbd = $('[data-kbd]'); if (kbd) kbd.textContent = isMac ? '⌘ K' : 'Ctrl K';
document.addEventListener('keydown', e => {
  const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.isContentEditable;
  if ((e.ctrlKey || e.metaKey) && !e.altKey && e.key.toLowerCase() === 'k') { e.preventDefault(); searchEl.hidden ? openSearch() : closeSearch(); return; }
  if (e.key === 'Escape') {
    if (!searchEl.hidden) closeSearch();
    else if (document.body.classList.contains('drawer-open')) { closeDrawer(); menuBtn.focus(); }
    else if (!timerPop.hidden) { toggleTimerPop(false); timerBtn.focus(); }
    else closeOtp();
    return;
  }
  if (typing || e.ctrlKey || e.metaKey || e.altKey || !searchEl.hidden) return;
  if (e.key === '/') { e.preventDefault(); openSearch(); }
  else if (e.key === '[') step(-1);
  else if (e.key === ']') step(1);
  else if (e.key === 'c' || e.key === 'C') coverBtn.click();
});

/* ------------------------------------------------ boot */
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
setCover(coverOn);
paintTimer();
route(false);
Anchors.initSync();
(window.requestIdleCallback || (f => setTimeout(f, 800)))(() => buildIndex());
})();
