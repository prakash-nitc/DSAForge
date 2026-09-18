"""Build the DSA Revision Bible website.

    python build/build.py            # content/ -> dist/index.html
    python build/build.py --watch    # rebuild whenever a file changes
"""
import datetime
import html
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from mdparse import parse_file, seg_text

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTENT = ROOT / 'content'
OUT = ROOT / 'dist' / 'index.html'
PALETTE = ['slate', 'ochre', 'blue', 'green', 'brick', 'violet', 'teal', 'rose']
WARN = []


def warn(msg):
    WARN.append(msg)


def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


def slugify(s, maxlen=48):
    s = s.lower().replace('&', ' and ').replace("'", '').replace('’', '')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    if len(s) > maxlen:
        s = s[:maxlen].rsplit('-', 1)[0]
    return s or 'section'


def natural_key(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', p.name)]


def rel(p):
    return p.relative_to(ROOT).as_posix()


# ================================================================ load content

CARD_SECTION_IDS = [
    (r'^The knobs', 'knobs', 'Knobs'), (r'^Trigger signals', 'triggers', 'Triggers'), (r'^Anchors', 'anchors', 'Anchors'),
    (r'^Your sheet', 'your-sheet', 'Your sheet'), (r'^Decay signatures', 'decay', 'Decay signatures'),
    (r'^Java bugs', 'java-bugs', 'Java bugs'), (r'^Complexity$', 'complexity', 'Complexity'),
    (r'^Interview follow-ups', 'follow-ups', 'Follow-ups'), (r'^Additions', 'additions', 'Additions'),
]


def heading_id_and_short(text, kind):
    m = re.match(r'^(\d{1,2})\.(\d{1,2})\s+(.*)$', text)
    if m:
        return f'{m.group(1)}-{m.group(2)}', f'{m.group(1)}.{m.group(2)} {m.group(3)}'
    m = re.match(r'^Template\s+(\w+)\s+—\s+(.*)$', text)
    if m:
        return 't-' + m.group(1).lower(), f'{m.group(1)} {m.group(2)}'
    m = re.match(r'^([A-K]\d{1,2})\s+·\s+(.*)$', text)
    if m:
        return m.group(1).lower(), f'{m.group(1)} {m.group(2)}'
    if kind == 'card':
        for pat, hid, short in CARD_SECTION_IDS:
            if re.search(pat, text):
                return hid, short
    return slugify(text), text


def make_page(pid, part, numeral, title, kind, blocks, src, meta):
    pg = dict(id=pid, part=part['key'], numeral=numeral, title=title, kind=kind, blocks=blocks, src=src, meta=meta, toc=[])
    used = set()
    for b in blocks:
        if b['kind'] != 'h':
            continue
        b['rel'] = 2 if (kind == 'card' or b['level'] <= 2) else 3
        hid, short = heading_id_and_short(b['text'], kind)
        if b.get('explicit_id'):
            hid = b['explicit_id']
        base, k = hid, 2
        while hid in used:
            hid, k = f'{base}-{k}', k + 1
        used.add(hid)
        b['id'], b['short'] = hid, short
        pg['toc'].append(dict(id=hid, title=b['text'], short=short, level=b['rel']))
    return pg


def load():
    parts, pages, seen = [], [], set()

    def unique(pid, src):
        base, k = pid, 2
        while pid in seen:
            pid, k = f'{base}-{k}', k + 1
        if pid != base:
            warn(f'{src}: id "{base}" is already used, this page became "{pid}"')
        seen.add(pid)
        return pid

    for d in sorted([d for d in CONTENT.iterdir() if d.is_dir()], key=natural_key):
        pm = d / '_part.md'
        meta, blocks = parse_file(pm) if pm.exists() else ({}, [])
        key = meta.get('key') or re.sub(r'^\d+[-_]?', '', d.name) or d.name
        color = meta.get('color', 'slate').lower()
        if color not in PALETTE:
            warn(f'{rel(pm)}: color "{color}" is not one of {", ".join(PALETTE)}; using slate')
            color = 'slate'
        part = dict(key=key, tab=meta.get('tab', key), label=meta.get('label', key), title=meta.get('title', key),
                    color=color, folder=rel(d), items=[])
        if blocks or meta.get('numeral'):
            pid = unique(meta.get('id') or 'part-' + slugify(key), rel(pm))
            pages.append(make_page(pid, part, meta.get('numeral', ''), part['title'], 'part', blocks, rel(pm), meta))
            part['items'].append(pid)
        for f in sorted([f for f in d.glob('*.md') if not f.name.startswith('_')], key=natural_key):
            meta, blocks = parse_file(f)
            numeral = meta.get('numeral', '').strip()
            kind = 'card' if numeral.startswith('Card ') else 'appendix' if numeral.startswith('Appendix') else 'chapter'
            title = meta.get('title') or next((b['text'] for b in blocks if b['kind'] == 'h'), f.stem)
            pid = unique(meta.get('id') or slugify(re.sub(r'^\d+[-_]?', '', f.stem)), rel(f))
            pages.append(make_page(pid, part, numeral, title, kind, blocks, rel(f), meta))
            part['items'].append(pid)
        parts.append(part)
    home_meta, home_blocks = parse_file(CONTENT / '_home.md') if (CONTENT / '_home.md').exists() else ({}, [])
    return parts, pages, home_meta, home_blocks


# ================================================================ references

REF_RE = re.compile(r'''
   (?P<sec>§\s?(?P<sn>\d{1,2})(?:\.(?P<sm>\d{1,2}))?)
 | (?P<cards>\bCards?\s+(?P<clist>\d{1,2}(?:\s*(?:\+|,|and|&amp;|&)\s*\d{1,2})*))
 | (?P<app>\bAppendix\s+(?P<al>[A-Z])(?P<an>\d{1,2})?\b)
 | (?P<part>\bPart\s+(?P<pn>IV|III|II|I|V|0)\b)
 | (?P<shape>\bShape\s+(?P<sl>[A-E])\b)
 | (?P<tpl>\bTemplate\s+(?P<tc>[A-Z]?\d{1,2}[A-E]?)\b)
 | (?P<g>\b(?P<gc>G[1-9])\b)
 | (?P<d>\b(?P<dc>D[1-9])\b)
''', re.X)
KINDS = ('sec', 'cards', 'app', 'part', 'shape', 'tpl', 'g', 'd')


class Site:
    def __init__(self, parts, pages, home_meta, home_blocks):
        self.parts, self.pages = parts, pages
        self.home_meta, self.home_blocks = home_meta, home_blocks
        self.page = {p['id']: p for p in pages}
        self.part_of = {pid: part['key'] for part in parts for pid in part['items']}
        self.part_of['home'] = parts[0]['key'] if parts else '0'
        self.numeral = {}
        for p in pages:
            if p['numeral']:
                self.numeral.setdefault(p['numeral'], p['id'])
        self.cards = {}
        for p in pages:
            m = re.match(r'^Card (\d+)$', p['numeral'])
            if m:
                self.cards[int(m.group(1))] = (p['id'], None)
        self.aliases = []
        for p in pages:
            c = p['meta'].get('card')
            if c:
                n, _, a = c.partition('/')
                if n.strip().isdigit() and int(n) not in self.cards:
                    self.cards[int(n)] = (p['id'], a.strip() or None)
                    self.aliases.append(dict(n=int(n), title=p['title'].split(' — ')[0], pid=p['id'], anchor=a.strip() or None))
        self.aliases.sort(key=lambda x: x['n'])
        self.codes, self.shapes = {}, {}
        for p in pages:
            for b in p['blocks']:
                if b['kind'] != 'h':
                    continue
                m = re.search(r'\bTemplate\s+(\w+)\b', b['text'])
                if m:
                    self.codes.setdefault(m.group(1).upper(), (p['id'], b['id']))
                m = re.search(r'\bShape\s+([A-E])\b', b['text'])
                if m:
                    self.shapes.setdefault(m.group(1), (p['id'], b['id']))
        self.links = 0

    def toc_ids(self, pid):
        return {t['id'] for t in self.page[pid]['toc']} if pid in self.page else set()

    def target(self, kind, m):
        if kind == 'sec':
            pid = self.numeral.get(f"§{int(m.group('sn'))}")
            if not pid:
                return None
            if m.group('sm'):
                a = f"{int(m.group('sn'))}-{int(m.group('sm'))}"
                return (pid, a if a in self.toc_ids(pid) else None)
            return (pid, None)
        if kind == 'app':
            pid = self.numeral.get(f"Appendix {m.group('al')}")
            if not pid:
                return None
            a = (m.group('al') + m.group('an')).lower() if m.group('an') else None
            return (pid, a if a and a in self.toc_ids(pid) else None)
        if kind == 'part':
            pid = self.numeral.get(f"Part {m.group('pn')}")
            return (pid, None) if pid else None
        if kind == 'shape':
            return self.shapes.get(m.group('sl'))
        if kind == 'tpl':
            return self.codes.get(m.group('tc').upper())
        if kind == 'g':
            return self.codes.get(m.group('gc'))
        if kind == 'd':
            return self.codes.get(m.group('dc'))
        return None

    def link(self, text, tgt, cur):
        pid, a = tgt
        if pid == cur and not a:
            return text
        self.links += 1
        return f'<a class="xref" href="{href(pid, a)}">{text}</a>'

    def linkify(self, t, cur):
        days = bool(re.search(r'§1[34] D\d', t))

        def rep(m):
            kind = next(k for k in KINDS if m.group(k))
            if kind == 'd' and days:
                return m.group(0)
            if kind == 'cards':
                whole, lst = m.group(0), m.group('clist')
                nums = re.findall(r'\d{1,2}', lst)
                if len(nums) == 1:
                    t2 = self.cards.get(int(nums[0]))
                    return self.link(whole, t2, cur) if t2 else whole
                head = whole[:whole.index(lst)]
                return head + re.sub(r'\d{1,2}', lambda mm: self.link(mm.group(0), self.cards[int(mm.group(0))], cur)
                                     if int(mm.group(0)) in self.cards else mm.group(0), lst)
            tgt = self.target(kind, m)
            return self.link(m.group(0), tgt, cur) if tgt else m.group(0)

        return REF_RE.sub(rep, t)

    def resolve_href(self, h, where):
        """Markdown link target -> (url, pid-or-None, badge)."""
        if re.match(r'^(https?:|mailto:)', h):
            return h, None, ''
        if h.startswith('#/'):
            pid, _, a = h[2:].partition('/')
            if pid not in self.page and pid != 'home':
                warn(f'{where}: link "{h}" points to a page that does not exist')
            return h, pid, self.page[pid]['numeral'] if pid in self.page else ''
        if h in self.page:
            return f'#/{h}', h, self.page[h]['numeral']
        m = REF_RE.fullmatch(h.strip())
        if m:
            kind = next(k for k in KINDS if m.group(k))
            tgt = self.cards.get(int(m.group('clist'))) if kind == 'cards' and m.group('clist').isdigit() else self.target(kind, m)
            if tgt:
                return href(*tgt), tgt[0], h.strip()
        warn(f'{where}: could not resolve link target "{h}"')
        return h, None, h


def href(pid, anchor=None):
    return f'#/{pid}' + (f'/{anchor}' if anchor else '')


# ================================================================ rendering

FMT = HtmlFormatter(nowrap=True)
KEEP = {'k', 'kd', 'kn', 'kr', 'kt', 'kc', 'nc', 'na', 'nf', 'nd', 'nb', 's', 'sc', 's1', 's2', 'sa', 'se', 'sd',
        'mi', 'mf', 'mh', 'm', 'il', 'mb', 'c1', 'cm', 'cp', 'c', 'ch', 'cs'}
REMAP = {'kd': 'k', 'kn': 'k', 'kr': 'k', 's1': 's', 's2': 's', 'sa': 's', 'se': 's', 'sc': 's', 'sd': 's', 'mf': 'mi',
         'mh': 'mi', 'm': 'mi', 'il': 'mi', 'mb': 'mi', 'cm': 'c1', 'cp': 'c1', 'c': 'c1', 'ch': 'c1', 'cs': 'c1',
         'nf': 'na', 'nd': 'na', 'nb': 'kt'}


def highlight_html(src, lang):
    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        return esc(src)
    h = highlight(src, lexer, FMT)

    def span(m):
        cls, inner = m.group(1), m.group(2)
        if cls == 'n':
            raw = html.unescape(inner)
            if re.fullmatch(r'[A-Z][A-Z0-9_]+', raw):
                return f'<span class="cn">{inner}</span>'
            if re.fullmatch(r'[A-Z]\w*', raw):
                return f'<span class="ty">{inner}</span>'
            return inner
        if cls in KEEP:
            return f'<span class="{REMAP.get(cls, cls)}">{inner}</span>'
        return inner

    return re.sub(r'<span class="([\w-]+)">(.*?)</span>', span, h, flags=re.S).rstrip('\n')


P_CHIP = {'A': ('p-a', 'Anchor'), '1': ('p-1', 'Do it'), '2': ('p-2', 'If slack'), '3': ('p-3', 'Low value'), '×': ('p-x', 'Skip')}
STATUS_CHIP = {'Revised': 's-rev', 'Solved': 's-sol', 'Not started': 's-new'}
FILTER_BAR = ('<div class="filter-bar" role="group" aria-label="Filter problems">'
              '<button type="button" class="fchip" data-filter="all" aria-pressed="true">All</button>'
              '<button type="button" class="fchip" data-filter="A" aria-pressed="false">Anchors</button>'
              '<button type="button" class="fchip" data-filter="1" aria-pressed="false">Priority 1</button>'
              '<button type="button" class="fchip" data-filter="todo" aria-pressed="false">Not started</button>'
              '<button type="button" class="fchip" data-filter="x" aria-pressed="false">Skip list</button>'
              '<span class="filter-count" data-filter-count></span></div>')


def norm_name(s):
    return re.sub(r'[^a-z0-9]+', ' ', s.replace('w/', 'with').lower()).strip()


class Renderer:
    def __init__(self, site):
        self.s = site
        self.anchors, self.anchor_by_name = [], {}
        self.collect_anchors()

    # ---------------------------------------------------------------- anchors
    def tracker_cols(self, heads):
        low = [h.lower() for h in heads]
        name = next((k for k, h in enumerate(low) if h in ('anchor', 'anchor problem')), None)
        num = low.index('#') if '#' in low else None
        pat = next((k for k, h in enumerate(low) if h in ('pattern', 'topic')), None)
        when = next((k for k, h in enumerate(low) if h.startswith('activate')), None)
        return num, name, pat, when

    def collect_anchors(self):
        s = self.s
        occurrences = {}
        for p in s.pages:
            last_h = None
            for b in p['blocks']:
                if b['kind'] == 'h':
                    last_h = b['id']
                if b['kind'] != 'table':
                    continue
                heads = [c['text'] for c in b['header']]
                num, name, pat, when = self.tracker_cols(heads)
                if p['meta'].get('tracker') == 'true' and num is not None and name is not None:
                    for r in b['rows']:
                        n = r[num]['text']
                        if not n.isdigit():
                            continue
                        self.anchors.append(dict(n=int(n), name=r[name]['text'], pattern=r[pat]['text'] if pat is not None else '',
                                                 when=r[when]['text'] if when is not None else '',
                                                 group='later' if when is not None else 'core', tracker=p['id']))
                elif heads[:2] == ['#', 'Anchor']:
                    for r in b['rows']:
                        occurrences.setdefault(norm_name(r[1]['text']), (p['id'], last_h))
        seen = set()
        for a in self.anchors:
            if a['n'] in seen:
                warn(f'anchor number {a["n"]} is used twice in the tracker table')
            seen.add(a['n'])
            self.anchor_by_name[norm_name(a['name'])] = a['n']
            occ = occurrences.get(norm_name(a['name']))
            if occ:
                a['href'] = href(*occ)
                continue
            pat = a['pattern'].lower()
            pg = next((p for p in s.pages if pat and p['kind'] != 'part' and
                       (p['title'].lower().startswith(pat) or pat in p['title'].lower() or
                        (pat == 'dp' and p['title'].lower().startswith('dynamic programming')))), None)
            a['href'] = href(pg['id']) if pg else href(a['tracker'])

    # ---------------------------------------------------------------- inline
    def segs(self, segs, cur, tones=True, link=True):
        out = []
        for x in segs:
            t = esc(x['text'])
            if link and not x['mono'] and not x.get('href'):
                t = self.s.linkify(t, cur)
            if x['mono']:
                t = f'<code>{t}</code>'
            if x['i']:
                t = f'<em>{t}</em>'
            if x['b']:
                t = f'<strong>{t}</strong>'
            if tones and x['tone'] in ('red', 'green', 'amber', 'blue', 'muted'):
                t = f'<span class="tone-{x["tone"]}">{t}</span>'
            if x.get('href'):
                url, _, _ = self.s.resolve_href(x['href'], cur)
                ext = ' target="_blank" rel="noopener"' if url.startswith('http') else ''
                t = f'<a class="xref" href="{attr(url)}"{ext}>{t}</a>'
            out.append(t)
        merged = ''.join(out)
        merged = re.sub(r'</a>(\s*)<a class="xref" href="([^"]+)"([^>]*)>', lambda m: m.group(1) + f'</a><a class="xref" href="{m.group(2)}"{m.group(3)}>', merged)
        return merged.replace('\n', '<br>')

    # ---------------------------------------------------------------- blocks
    def heading(self, b):
        lvl = 'h2' if b['rel'] == 2 else 'h3'
        t = b['text']
        for pat in (r'^(\d{1,2}\.\d{1,2})\s+(.*)$', r'^(Template\s+\w+)\s+—\s+(.*)$', r'^([A-K]\d{1,2})\s+·\s+(.*)$'):
            m = re.match(pat, t)
            if m:
                return f'<{lvl} id="{b["id"]}" class="sec"><span class="hnum">{esc(m.group(1))}</span> {esc(m.group(2))}</{lvl}>'
        return f'<{lvl} id="{b["id"]}" class="sec">{esc(t)}</{lvl}>'

    def para(self, b, ctx):
        cls = 'note' if b.get('note') else ('keyline' if b.get('strong') else '')
        c = f' class="{cls}"' if cls else ''
        return f'<p id="{ctx.bid()}" data-b{c}>{self.segs(b["segs"], ctx.pid, tones=not b.get("note"))}</p>'

    def lst(self, b, ctx):
        tag = 'ol' if b.get('ordered') else 'ul'
        items = ''.join(f'<li id="{ctx.bid()}" data-b>{self.segs(it, ctx.pid)}</li>' for it in b['items'])
        return f'<{tag} class="bul{" num" if tag == "ol" else ""}">{items}</{tag}>'

    def callout(self, b, ctx):
        title = f'<p class="callout-title">{esc(b["title"])}</p>' if b.get('title') else ''
        body = ''.join(f'<p>{self.segs(p, ctx.pid)}</p>' for p in b['paras'])
        return f'<aside id="{ctx.bid()}" data-b class="callout callout-{b["tone"]}">{title}{body}</aside>'

    def cell(self, c, ctx):
        return '<br>'.join(self.segs(ps, ctx.pid) for ps in c['paras'])

    def facts(self, b):
        heads = [c['text'] for c in b['header']]
        return '<dl class="facts">' + ''.join(f'<div class="fact"><dt>{esc(h)}</dt><dd>{esc(c["text"])}</dd></div>'
                                              for h, c in zip(heads, b['rows'][0])) + '</dl>'

    def table(self, b, ctx):
        s = self.s
        heads = [c['text'] for c in b['header']]
        is_anchor = heads[:2] == ['#', 'Anchor']
        is_index = len(heads) >= 3 and heads[:3] == ['Problem', 'Status', 'P']
        is_cards = heads[:2] == ['Card', 'Pattern']
        is_topics = heads[:2] == ['§', 'Topic']
        th = ''.join(f'<th scope="col">{esc(h)}</th>' for h in heads) + ('<th scope="col" class="col-log">Cold solves</th>' if is_anchor else '')
        rows = []
        for r in b['rows']:
            tds, extra = [], ''
            for ci, c in enumerate(r):
                inner, cls = self.cell(c, ctx), ''
                if is_index and ci == 1:
                    inner = f'<span class="chip {STATUS_CHIP.get(c["text"], "s-new")}">{esc(c["text"])}</span>'
                elif is_index and ci == 2:
                    k, label = P_CHIP.get(c['text'], ('p-3', c['text']))
                    inner, cls = f'<span class="chip pchip {k}" title="{attr(label)}">{esc(c["text"])}</span>', ' class="c-p"'
                elif (is_cards or is_topics) and ci == 1 and r[0]['text'].isdigit():
                    n = int(r[0]['text'])
                    tgt = s.cards.get(n) if is_cards else ((s.numeral.get(f'§{n}'), None) if s.numeral.get(f'§{n}') else None)
                    if tgt:
                        inner = f'<a class="xref strong" href="{href(*tgt)}">{inner}</a>'
                elif ci == 0 and c['text'].isdigit() and heads and heads[0] in ('#', 'Card', '§', 'Level'):
                    cls = ' class="c-num"'
                tds.append(f'<td{cls}>{inner}</td>')
            if is_index:
                extra = f' data-status="{attr(r[1]["text"])}" data-p="{attr(r[2]["text"])}"'
            if is_anchor:
                n = self.anchor_by_name.get(norm_name(r[1]['text']))
                if n:
                    tds.append(f'<td class="col-log"><button type="button" class="log-btn" data-anchor="{n}">Log today</button>'
                               f'<span class="log-last" data-last="{n}"></span></td>')
                else:
                    tds.append('<td></td>')
            rows.append(f'<tr id="{ctx.bid()}" data-b{extra}>{"".join(tds)}</tr>')
        klass = 'tbl' + (' tbl-index' if is_index else '') + (' tbl-anchors' if is_anchor else '')
        if len(heads) + (1 if is_anchor else 0) >= 6:
            klass += ' tbl-wide'
        return (f'<div class="table-wrap"><table class="{klass}"><thead><tr>{th}</tr></thead>'
                f'<tbody>{"".join(rows)}</tbody></table></div>')

    def tracker(self, b, ctx):
        heads = [c['text'] for c in b['header']]
        num, name, pat, when = self.tracker_cols(heads)
        rows = []
        for r in b['rows']:
            if not r[num]['text'].isdigit():
                continue
            a = next(x for x in self.anchors if x['n'] == int(r[num]['text']))
            w = f'<span class="tr-when">{esc(a["when"])}</span>' if a['when'] else ''
            rows.append(f'<tr id="{ctx.bid()}" data-b data-anchor-row="{a["n"]}"><td class="c-num">{a["n"]}</td>'
                        f'<td class="tr-anchor"><a class="xref strong" href="{a["href"]}">{esc(a["name"])}</a>'
                        f'<span class="tr-pattern">{esc(a["pattern"])}</span>{w}</td>'
                        f'<td class="tr-dates" data-dates="{a["n"]}"></td><td class="tr-state" data-state="{a["n"]}"></td>'
                        f'<td class="tr-act"><button type="button" class="log-btn" data-anchor="{a["n"]}">Log today</button></td></tr>')
        return ('<div class="table-wrap"><table class="tbl tbl-tracker"><thead><tr><th scope="col">#</th><th scope="col">Anchor</th>'
                '<th scope="col">Last four cold solves</th><th scope="col">State</th><th scope="col"><span class="sr-only">Log</span></th>'
                f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

    def code(self, b, ctx):
        lang, flags, lines = b['lang'], b['flags'], b['lines']
        if lang == 'decision-tree':
            return self.dtree(lines, ctx)
        if lang == 'rules':
            return self.rules(lines, ctx)
        if lang == 'log':
            return self.logrow(lines, ctx, b['caption'] or 'Example row')
        if lang == 'talk-track':
            return self.script(lines, ctx, b['caption'] or 'Talk-track')
        src = '\n'.join(lines)
        if lang and lang not in ('text', 'txt', 'plain', 'format'):
            cover = 'cover' in flags or (lang == 'java' and not ({'idiom', 'nocover'} & set(flags)))
            ui = ('<div class="cover"><p>Write it from memory first.</p><button type="button" class="reveal-btn">Reveal template</button></div>'
                  if cover else '')
            label = {'java': 'Java', 'python': 'Python', 'py': 'Python', 'cpp': 'C++', 'c++': 'C++', 'js': 'JavaScript',
                     'javascript': 'JavaScript', 'sql': 'SQL', 'c': 'C'}.get(lang, lang.title())
            return (f'<figure id="{ctx.bid()}" data-b data-code class="code"{" data-cover" if cover else ""}>'
                    f'<div class="code-head"><span class="code-lang">{esc(b["caption"] or label)}</span>'
                    f'<button type="button" class="copy-btn" aria-label="Copy code">Copy</button></div>'
                    f'<pre><code>{highlight_html(src, lang)}</code></pre>{ui}</figure>')
        cap = f'<figcaption>{esc(b["caption"])}</figcaption>' if b['caption'] else ''
        return f'<figure id="{ctx.bid()}" data-b class="fmt">{cap}<pre>{esc(src)}</pre></figure>'

    def rules(self, lines, ctx):
        items = []
        for l in lines:
            m = re.match(r'^\s*(\d{1,2})\.\s+(.*)$', l)
            if not m:
                continue
            parts = re.split(r'(?<=\.)\s+', m.group(2), maxsplit=1)
            rest = self.s.linkify(esc(parts[1]), ctx.pid) if len(parts) > 1 else ''
            items.append(f'<li id="{ctx.bid()}" data-b><span class="rule-n">{m.group(1)}</span><p><strong>{esc(parts[0])}</strong> {rest}</p></li>')
        return f'<ol class="rules">{"".join(items)}</ol>'

    def logrow(self, lines, ctx, cap):
        rows = ''.join(f'<div class="kv"><dt>{esc(m.group(1).strip())}</dt><dd>{esc(m.group(2))}</dd></div>'
                       for m in (re.match(r'^([A-Z0-9+\- ]+?)\s{2,}(.*)$', l) for l in lines) if m)
        return f'<figure id="{ctx.bid()}" data-b class="fmt"><figcaption>{esc(cap)}</figcaption><dl class="logrow">{rows}</dl></figure>'

    def script(self, lines, ctx, cap):
        items = []
        for l in lines:
            m = re.match(r'^\s*(".*?")?\s*(\[.*\])?\s*$', l)
            if m and (m.group(1) or m.group(2)):
                q = f'<span class="say">{esc(m.group(1).strip(chr(34)))}</span>' if m.group(1) else ''
                d = f'<span class="do">{esc(m.group(2).strip("[]"))}</span>' if m.group(2) else ''
                items.append(f'<li>{q}{d}</li>')
        return f'<figure id="{ctx.bid()}" data-b class="script"><figcaption>{esc(cap)}</figcaption><ol>{"".join(items)}</ol></figure>'

    def dt_target(self, ref):
        s = self.s
        ref = ref.strip()
        m = re.match(r'^(\d{1,2}[A-E])$', ref)
        if m:
            return s.codes.get(ref.upper())
        m = REF_RE.fullmatch(ref)
        if m:
            kind = next(k for k in KINDS if m.group(k))
            if kind == 'cards':
                return s.cards.get(int(m.group('clist'))) if m.group('clist').isdigit() else None
            return s.target(kind, m)
        return None

    def dtree(self, lines, ctx):
        groups, lead, cur = [], None, None
        for l in lines:
            if not l.strip():
                continue
            mb = re.match(r"^\s*[|'`]-\s*(.+?)\s*\.{2,}\s*(.+?)\s*(?:\((.+?)\))?\s*$", l)
            mq = re.match(r'^(.+?\?)\s*\.{2,}\s*(.+?)\s*\((.+?)\)\s*$', l)
            if mb and cur is not None:
                cur['br'].append((mb.group(1), mb.group(2).strip(), mb.group(3)))
            elif mq:
                cur = dict(q=mq.group(1).strip(), br=[('', mq.group(2), mq.group(3))])
                groups.append(cur)
            elif l.strip().endswith('?'):
                cur = dict(q=l.strip(), br=[])
                groups.append(cur)
            elif not groups:
                lead = (lead + ' ' if lead else '') + l.strip()
        out = [f'<p class="dtree-lead" id="{ctx.bid()}" data-b>{self.s.linkify(esc(lead), ctx.pid)}</p>'] if lead else []
        for g in groups:
            gid = 'q-' + re.sub(r'[^a-z0-9]+', '-', g['q'].lower()).strip('-')[:40]
            ctx.extra_toc.append(dict(id=gid, title=g['q'], short=g['q'], level=2))
            rows = []
            for cue, pattern, refs in g['br']:
                refs_l = [r.strip() for r in (refs or '').split(',') if r.strip()]
                tgt = self.dt_target(refs_l[0]) if refs_l else None
                inner = ((f'<span class="dq-cue">{esc(cue)}</span>' if cue else '') +
                         f'<span class="dq-pattern">{esc(pattern)}</span><span class="dq-ref">{esc(", ".join(refs_l))}</span>')
                rows.append(f'<li><a class="dq-row" href="{href(*tgt)}">{inner}</a></li>' if tgt else f'<li><div class="dq-row">{inner}</div></li>')
            single = ' dq-single' if len(g['br']) == 1 and not g['br'][0][0] else ''
            out.append(f'<section class="dq{single}" id="{ctx.bid()}" data-b><h2 class="dq-q sec" id="{gid}">{esc(g["q"])}</h2><ul>{"".join(rows)}</ul></section>')
        return f'<div class="dtree">{"".join(out)}</div>'

    # ---------------------------------------------------------------- pages
    def numeral_html(self, numeral):
        m = re.match(r'^§(\d+)$', numeral)
        if m:
            return f'<span class="nm-big">§{m.group(1)}</span>'
        m = re.match(r'^(Card|Appendix|Part)\s+(\S+)$', numeral)
        if m:
            return f'<span class="nm-label">{m.group(1)}</span><span class="nm-big">{esc(m.group(2))}</span>'
        return f'<span class="nm-big">{esc(numeral)}</span>' if numeral else ''

    def page(self, pg):
        ctx = Ctx(pg['id'])
        blocks = pg['blocks']
        body, facts, lede = [], '', ''
        first_index = next((k for k, b in enumerate(blocks) if b['kind'] == 'table' and [c['text'] for c in b['header']][:3] == ['Problem', 'Status', 'P']), None)
        filter_at = None
        if first_index is not None:
            filter_at = first_index
            while filter_at > 0 and blocks[filter_at - 1]['kind'] == 'h':
                filter_at -= 1
        tracker_tools_done = False
        for k, b in enumerate(blocks):
            if k == filter_at:
                body.append(FILTER_BAR)
            kind = b['kind']
            if kind == 'h':
                body.append(self.heading(b))
            elif kind == 'p':
                if k == 0 and pg['kind'] == 'part' and b.get('note'):
                    lede = f'<p class="lede">{self.segs(b["segs"], pg["id"], tones=False)}</p>'
                else:
                    body.append(self.para(b, ctx))
            elif kind == 'list':
                body.append(self.lst(b, ctx))
            elif kind == 'callout':
                body.append(self.callout(b, ctx))
            elif kind == 'table':
                heads = [c['text'] for c in b['header']]
                num, name, _, _ = self.tracker_cols(heads)
                if pg['meta'].get('tracker') == 'true' and num is not None and name is not None:
                    if not tracker_tools_done:
                        body.append('<div class="tracker-tools"><span class="sync-state" data-sync></span><span class="tt-actions">'
                                    '<button type="button" class="ghost-btn" data-edit-dates aria-pressed="false">Edit dates</button></span></div>')
                        tracker_tools_done = True
                    body.append(self.tracker(b, ctx))
                elif k == 0 and len(b['rows']) == 1:
                    facts = self.facts(b)
                else:
                    body.append(self.table(b, ctx))
            elif kind == 'code':
                body.append(self.code(b, ctx))
            elif kind == 'placeholder':
                warn(f'{pg["src"]}: {{{{{b["name"]}}}}} only works on the home page')
        if ctx.extra_toc:
            pg['toc'] = pg['toc'] + ctx.extra_toc
        title, sub = split_title(pg['title'])
        head = (f'<header class="page-head"><div class="numeral">{self.numeral_html(pg["numeral"])}</div>'
                f'<h1 tabindex="-1">{esc(title)}</h1>' + (f'<p class="subtitle">{esc(sub)}</p>' if sub else '') + facts + lede + '</header>')
        extra = self.part_index(pg) if pg['kind'] == 'part' else ''
        if extra:
            pg['toc'] = pg['toc'] + [dict(id='in-this-part', title='In this part', short='In this part', level=2)]
        return f'<article class="page" data-page="{pg["id"]}" data-part="{pg["part"]}">{head}<div class="page-body">{"".join(body)}{extra}</div></article>'

    def part_index(self, pg):
        part = next(p for p in self.s.parts if p['key'] == pg['part'])
        rows = []
        for item in part['items']:
            if item == pg['id']:
                continue
            p = self.s.page[item]
            t, sub = split_title(p['title'])
            num = re.sub(r'^(Card |Appendix )', '', p['numeral'])
            rows.append(f'<li><a href="{href(item)}"><span class="pi-num">{esc(num)}</span><span class="pi-title">{esc(t)}</span>'
                        + (f'<span class="pi-sub">{esc(sub)}</span>' if sub else '') + '</a></li>')
        return f'<h2 class="sec" id="in-this-part">In this part</h2><ol class="part-index">{"".join(rows)}</ol>' if rows else ''

    # ---------------------------------------------------------------- home
    def board(self):
        s = self.s
        tbl = next((b for p in s.pages for b in p['blocks'] if b['kind'] == 'table' and [c['text'] for c in b['header']][:2] == ['Card', 'Pattern']), None)
        if not tbl:
            return '<p class="sec-note">Add a table with the columns Card | Pattern | Your state | Priority to the Part II overview to fill this board.</p>'
        items = []
        for r in tbl['rows']:
            if not r[0]['text'].isdigit():
                continue
            n = int(r[0]['text'])
            name, state = r[1]['text'], r[2]['text'] if len(r) > 2 else ''
            prio = r[3]['text'] if len(r) > 3 else ''
            tgt = s.cards.get(n)
            m = re.match(r'^(\d+)\s*/\s*(\d+)', state)
            if m:
                solved, total = int(m.group(1)), int(m.group(2))
                cells = ''.join(f'<i class="{"on" if k < solved else ""}"></i>' for k in range(min(total, 60)))
                tally = f'<span class="tally" role="img" aria-label="{solved} of {total} solved">{cells}</span>'
                count = f'<span class="b-count">{solved}/{total}</span>'
            else:
                tally, count = f'<span class="tally tally-none">{esc(state)}</span>', '<span class="b-count"></span>'
            where = f'<span class="b-where">{esc(s.page[tgt[0]]["numeral"])}</span>' if tgt and s.page[tgt[0]]['kind'] != 'card' else ''
            inner = (f'<span class="b-n">{n}</span><span class="b-name">{esc(name)}{where}</span>{tally}{count}<span class="b-prio">{esc(prio)}</span>')
            items.append(f'<li><a href="{href(*tgt)}" data-part="{s.part_of[tgt[0]]}">{inner}</a></li>' if tgt else f'<li><div class="b-row">{inner}</div></li>')
        return f'<ol class="board">{"".join(items)}</ol>'

    def go_buttons(self, segs, cls):
        s = self.s
        out = []
        for x in segs:
            if not x.get('href'):
                continue
            url, pid, badge = s.resolve_href(x['href'], 'content/_home.md')
            part = f' data-part="{s.part_of.get(pid, "")}"' if pid else ''
            out.append(f'<a class="{cls}" href="{attr(url)}"{part}><span class="go-id">{esc(badge)}</span><span class="go-t">{esc(x["text"].strip())}</span></a>')
        return ''.join(out)

    def home(self):
        meta, blocks = self.s.home_meta, self.s.home_blocks
        ctx = Ctx('home')
        title = [t.strip() for t in meta.get('title', 'Revision Bible').split('|')]
        hero = [f'<h1 tabindex="-1" class="home-title">{"".join(f"<span>{esc(t)}</span> " for t in title).strip()}</h1>']
        if meta.get('tagline'):
            hero.append(f'<p class="home-sub">{esc(meta["tagline"])}</p>')
        toc, secs, k = [], [], 0
        while k < len(blocks) and blocks[k]['kind'] != 'h':
            if blocks[k]['kind'] == 'p':
                hero.append(f'<p class="home-cta">{self.segs(blocks[k]["segs"], "home")}</p>')
            k += 1
        open_sec = False
        for b in blocks[k:]:
            kind = b['kind']
            if kind == 'h':
                if open_sec:
                    secs.append('</section>')
                hid = b.get('explicit_id') or slugify(b['text'])
                toc.append(dict(id=hid, short=b['text'], level=2))
                secs.append(f'<section class="home-sec"><h2 class="sec" id="{hid}">{esc(b["text"])}</h2>')
                open_sec = True
            elif kind == 'table':
                rows = []
                for r in b['rows']:
                    when, what = r[0]['text'], (r[1]['text'] if len(r) > 2 else '')
                    gos = self.go_buttons([x for c in r[1:] for ps in c['paras'] for x in ps], 'go')
                    rows.append(f'<li class="entry"><div class="entry-text"><p class="entry-when">{esc(when)}</p>'
                                + (f'<p class="entry-what">{esc(what)}</p>' if what else '') + f'</div><div class="entry-go">{gos}</div></li>')
                secs.append(f'<ul class="entries">{"".join(rows)}</ul>')
            elif kind == 'list':
                items = ''.join(f'<li>{self.go_buttons(it, "keep-link")}</li>' for it in b['items'])
                secs.append(f'<ul class="keep">{items}</ul>')
            elif kind == 'placeholder':
                if b['name'] == 'pattern-board':
                    secs.append(self.board())
                elif b['name'] == 'anchor-summary':
                    secs.append('<div class="anchor-summary" data-anchor-summary></div>')
                else:
                    warn(f'content/_home.md: unknown component {{{{{b["name"]}}}}}')
            elif kind == 'p':
                secs.append(f'<p class="sec-note">{self.segs(b["segs"], "home")}</p>')
            elif kind == 'callout':
                secs.append(self.callout(b, ctx))
            elif kind == 'code':
                secs.append(self.code(b, ctx))
        if open_sec:
            secs.append('</section>')
        html_ = (f'<article class="page home" data-page="home" data-part="{self.s.part_of["home"]}"><header class="home-head">'
                 f'{"".join(hero)}<div class="continue" data-continue hidden></div></header>{"".join(secs)}</article>')
        return html_, toc


class Ctx:
    def __init__(self, pid):
        self.pid, self.n, self.extra_toc = pid, 0, []

    def bid(self):
        self.n += 1
        return f'b{self.n}'


def split_title(t):
    return tuple(t.split(' — ', 1)) if ' — ' in t else (t, '')


# ================================================================ assemble

DARK = ("color-scheme:dark;--paper:#0E1522;--paper-2:#131C2C;--paper-3:#1B2638;--ink:#E3E8F1;--ink-2:#AAB4C6;--ink-3:#8590A6;"
        "--rule:#223049;--rule-2:#2F3F5C;--link:#8DB4F5;--focus:#7FA9F5;--code-bg:#0B111C;--mark:#6A5314;"
        "--pal-slate:#9AA4B8;--pal-ochre:#E3A84E;--pal-blue:#72A8F2;--pal-green:#5CC093;--pal-brick:#F08A6C;--pal-violet:#B299E6;--pal-teal:#52C7D2;--pal-rose:#EE86B2;"
        "--tone-red:#F28B87;--tone-green:#82CE92;--tone-amber:#E8BD6A;--tone-blue:#82B2F5;--tone-muted:#8590A6;"
        "--ok:#45B872;--ok-soft:#2C5C3E;--bad:#E5574D;"
        "--c-info:#142037;--c-info-b:#6F9BE0;--c-do:#12251B;--c-do-b:#5DB87B;--c-warn:#2A1618;--c-warn-b:#E57A74;--c-neutral:#161F2E;--c-neutral-b:#8590A6;"
        "--sx-k:#C4A5FF;--sx-t:#6ED0DB;--sx-s:#93D69C;--sx-n:#F59C82;--sx-c:#E6BC6E;--sx-f:#93B9FA;"
        "--shadow:0 18px 48px rgba(0,0,0,.55);")


def repo_info():
    repo = os.environ.get('GITHUB_REPOSITORY') or ''
    branch = os.environ.get('GITHUB_REF_NAME') or ''
    sha = os.environ.get('GITHUB_SHA') or ''
    server = os.environ.get('GITHUB_SERVER_URL') or 'https://github.com'
    if not sha:
        try:
            sha = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, timeout=5).stdout.strip()
        except Exception:
            sha = ''
    return repo, branch, sha, server


def build():
    WARN.clear()
    parts, pages, home_meta, home_blocks = load()
    site = Site(parts, pages, home_meta, home_blocks)
    r = Renderer(site)
    html_by = {}
    home_html, home_toc = r.home()
    html_by['home'] = home_html
    for pg in pages:
        html_by[pg['id']] = r.page(pg)

    repo, branch, sha, server = repo_info()
    repo = repo or home_meta.get('repo', '')
    branch = branch or home_meta.get('branch', 'main')
    home_title = ' '.join(t.strip() for t in home_meta.get('title', 'Revision Bible').split('|'))
    meta = [dict(id='home', part=site.part_of['home'], numeral='Home', title=home_title, sub='', kind='home', toc=home_toc, src='content/_home.md')]
    for pg in pages:
        t, sub = split_title(pg['title'])
        entry = dict(id=pg['id'], part=pg['part'], numeral=pg['numeral'], title=t, sub=sub, kind=pg['kind'], src=pg['src'],
                     toc=[dict(id=x['id'], short=x['short'], level=x['level']) for x in pg['toc']])
        if pg['kind'] == 'card':
            n = int(pg['numeral'].split()[1])
            tbl = next((b for p in pages for b in p['blocks'] if b['kind'] == 'table' and [c['text'] for c in b['header']][:2] == ['Card', 'Pattern']), None)
            row = next((x for x in (tbl['rows'] if tbl else []) if x[0]['text'] == str(n)), None)
            m = re.match(r'^(\d+)\s*/\s*(\d+)', row[2]['text']) if row and len(row) > 2 else None
            entry['cov'] = f'{m.group(1)}/{m.group(2)}' if m else ''
        meta.append(entry)

    data = dict(pages=meta,
                parts=[dict(key=p['key'], tab=p['tab'], label=p['label'], title=p['title'], items=(['home'] if k == 0 else []) + p['items'],
                            folder=p['folder']) for k, p in enumerate(parts)],
                anchors=[dict(n=a['n'], name=a['name'], pattern=a['pattern'], group=a['group'], href=a['href']) for a in r.anchors],
                aliases=site.aliases,
                repo=dict(url=f'{server}/{repo}', branch=branch) if repo else None,
                built=dict(at=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), sha=sha[:7]))

    order = ['home'] + [pg['id'] for pg in pages]
    templates = '\n'.join(f'<template id="tpl-{pid}">{html_by[pid]}</template>' for pid in order)
    part_css = ''.join(f'[data-part="{p["key"]}"]{{--part:var(--pal-{p["color"]})}}' for p in parts)
    css = (HERE / 'app.css').read_text(encoding='utf-8').replace('__DARK__', DARK) + part_css
    out = ((HERE / 'shell.html').read_text(encoding='utf-8')
           .replace('<!--__TITLE__-->', esc(home_title))
           .replace('/*__CSS__*/', css)
           .replace('<!--__TEMPLATES__-->', templates)
           .replace('/*__DATA__*/', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
           .replace('/*__JS__*/', (HERE / 'app.js').read_text(encoding='utf-8')))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out, encoding='utf-8')
    (OUT.parent / '.nojekyll').write_text('')
    print(f'Built {rel(OUT)}: {len(out) / 1024:.0f} KB, {len(order)} pages, {site.links} cross-links, {len(r.anchors)} anchors')
    for w in WARN:
        print('  warning:', w)
    return WARN


def watch():
    def stamp():
        files = list(CONTENT.rglob('*.md')) + [HERE / n for n in ('app.css', 'app.js', 'shell.html', 'build.py', 'mdparse.py')]
        return max(f.stat().st_mtime for f in files if f.exists())
    last = None
    print('Watching content/ for changes. Open dist/index.html in your browser and refresh after each rebuild. Ctrl+C to stop.')
    while True:
        s = stamp()
        if s != last:
            last = s
            try:
                build()
            except Exception as e:  # keep watching after a bad edit
                print('  build failed:', e)
        time.sleep(1)


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(errors='replace')  # Windows consoles
    except Exception:
        pass
    if '--watch' in sys.argv:
        watch()
    else:
        build()
        if '--strict' in sys.argv and WARN:
            sys.exit(1)
