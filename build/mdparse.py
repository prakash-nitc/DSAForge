"""Parse the Bible's Markdown dialect into the block model the renderer uses.

Supported (see EDITING.md):
  front matter  ---\\nkey: value\\n---
  ## / ###      section headings, optional {#custom-id}
  paragraphs    *whole paragraph in italics* renders as a note
  - / 1.        lists (one level)
  > [!NOTE] / [!TIP] / [!WARNING] / plain >   callouts (first **bold** line = title)
  | tables |    GitHub pipe tables, <br> for a line break inside a cell
  ```java       Java template (blurred in cover mode);  ```java idiom = reference, never covered
  ```text Caption   monospace format block;  ```rules  ```decision-tree  ```log  ```talk-track
  {{pattern-board}} {{anchor-summary}}   home-page components
  inline        **bold** *italic* `code` [link](target) [text]{.red|.green|.amber}  \\* escapes
"""
import re

PUNCT = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
ALERTS = {'NOTE': 'info', 'IMPORTANT': 'info', 'TIP': 'do', 'WARNING': 'warn', 'CAUTION': 'warn'}
TONES = ('red', 'green', 'amber', 'blue', 'muted')


# ------------------------------------------------------------------ inline

def _find_close_bracket(s, i):
    """s[i] == '['; return index of the matching ']' or -1."""
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '`':
            k = s.find('`', j + 1)
            j = (k + 1) if k > 0 else j + 1
            continue
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return -1


def _tokenize(s):
    toks = []
    buf = []

    def flush():
        if buf:
            toks.append(('text', ''.join(buf)))
            buf.clear()

    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == '\\' and i + 1 < n and s[i + 1] in PUNCT:
            buf.append(s[i + 1])
            i += 2
            continue
        if c == '`':
            m = re.match(r'`+', s[i:])
            fence = m.group(0)
            k = s.find(fence, i + len(fence))
            if k > 0:
                flush()
                code = s[i + len(fence):k]
                if code.startswith(' ') and code.endswith(' ') and code.strip():
                    code = code[1:-1]
                toks.append(('code', code))
                i = k + len(fence)
                continue
        if s.startswith('<br>', i) or s.startswith('<br/>', i) or s.startswith('<br />', i):
            flush()
            toks.append(('br',))
            i = s.index('>', i) + 1
            continue
        if c == '[':
            j = _find_close_bracket(s, i)
            if j > 0:
                rest = s[j + 1:]
                m = re.match(r'\(([^()\s]+(?:\([^()]*\))?[^()\s]*|[^()]+)\)', rest)
                mt = re.match(r'\{\.(\w+)\}', rest)
                if m:
                    flush()
                    toks.append(('link', m.group(1).strip(), _parse_tree(s[i + 1:j])))
                    i = j + 1 + len(m.group(0))
                    continue
                if mt and mt.group(1) in TONES:
                    flush()
                    toks.append(('tone', mt.group(1), _parse_tree(s[i + 1:j])))
                    i = j + 1 + len(mt.group(0))
                    continue
        if c == '*':
            m = re.match(r'\*+', s[i:])
            run = len(m.group(0))
            prev = s[i - 1] if i > 0 else ' '
            nxt = s[i + run] if i + run < n else ' '
            flush()
            toks.append({'n': run, 'orig': run, 'open': not nxt.isspace(), 'close': not prev.isspace()})
            i += run
            continue
        buf.append(c)
        i += 1
    flush()
    return toks


def _emphasis(toks):
    i = 0
    while i < len(toks):
        t = toks[i]
        if isinstance(t, dict) and t['close'] and t['n'] > 0:
            j = i - 1
            while j >= 0 and not (isinstance(toks[j], dict) and toks[j]['open'] and toks[j]['n'] > 0):
                j -= 1
            if j < 0:
                i += 1
                continue
            o = toks[j]
            use = 2 if (o['n'] >= 2 and t['n'] >= 2) else 1
            node = ('b' if use == 2 else 'i', toks[j + 1:i])
            o['n'] -= use
            t['n'] -= use
            toks[j + 1:i] = [node]
            i = j + 2
            continue
        i += 1
    out = []
    for t in toks:
        if isinstance(t, dict):
            if t['n']:
                out.append(('text', '*' * t['n']))
        else:
            out.append(t)
    return out


def _parse_tree(s):
    return _emphasis(_tokenize(s))


def _flatten(nodes, b=False, i=False, tone=None, href=None, out=None):
    out = [] if out is None else out

    def add(text, mono=False):
        seg = dict(text=text, b=b, i=i, tone=tone, mono=mono, href=href)
        if out and not mono and not out[-1]['mono'] and all(out[-1][k] == seg[k] for k in ('b', 'i', 'tone', 'href')):
            out[-1]['text'] += text
        else:
            out.append(seg)

    for nd in nodes:
        if isinstance(nd, dict):
            if nd['n']:
                add('*' * nd['n'])
            continue
        kind = nd[0]
        if kind == 'text':
            add(nd[1])
        elif kind == 'code':
            add(nd[1], mono=True)
        elif kind == 'br':
            add('\n')
        elif kind == 'b':
            _flatten(nd[1], True, i, tone, href, out)
        elif kind == 'i':
            _flatten(nd[1], b, True, tone, href, out)
        elif kind == 'tone':
            _flatten(nd[2], b, i, nd[1], href, out)
        elif kind == 'link':
            _flatten(nd[2], b, i, tone, nd[1], out)
    return out


def parse_inline(s):
    return _flatten(_parse_tree(s))


def seg_text(segs):
    return ''.join(x['text'] for x in segs)


# ------------------------------------------------------------------ blocks

FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})\s*(.*)$')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
LIST_ITEM = re.compile(r'^\s{0,3}([-*+]|\d{1,3}[.)])\s+(.*)$')
TABLE_DELIM = re.compile(r'^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$')
HR = re.compile(r'^\s{0,3}([-*_])(\s*\1){2,}\s*$')
PLACEHOLDER = re.compile(r'^\{\{\s*([\w-]+)\s*\}\}$')


def split_front_matter(text):
    meta = {}
    if text.startswith('---'):
        end = re.search(r'^---\s*$', text[3:], re.M)
        if end:
            fm = text[3:3 + end.start()]
            text = text[3 + end.end():]
            for line in fm.splitlines():
                if not line.strip() or line.lstrip().startswith('#') or ':' not in line:
                    continue
                k, v = line.split(':', 1)
                v = v.strip()
                if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
                    v = v[1:-1]
                meta[k.strip().lower()] = v
    return meta, text


def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'):
        s = s[:-1]
    cells, buf, i = [], [], 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s) and s[i + 1] == '|':
            buf.append('\\|')
            i += 2
            continue
        if s[i] == '|':
            cells.append(''.join(buf).strip())
            buf = []
        else:
            buf.append(s[i])
        i += 1
    cells.append(''.join(buf).strip())
    return cells


def make_cell(raw):
    paras = [parse_inline(p.strip()) for p in re.split(r'<br\s*/?>', raw) if p.strip()]
    return dict(paras=paras, span=1, text=' '.join(seg_text(p) for p in paras).strip())


def para_block(segs):
    vis = [x for x in segs if x['text'].strip()]
    all_i = bool(vis) and all(x['i'] for x in vis)
    all_b = bool(vis) and all(x['b'] for x in vis)
    return dict(kind='p', segs=segs, text=seg_text(segs), note=all_i and not all_b, strong=all_b and not all_i)


def is_block_start(line, nxt):
    return bool(FENCE.match(line) or HEADING.match(line) or line.lstrip().startswith('>') or LIST_ITEM.match(line)
                or PLACEHOLDER.match(line.strip()) or HR.match(line)
                or (line.lstrip().startswith('|') and nxt is not None and TABLE_DELIM.match(nxt)))


def parse_blocks(text):
    lines = text.split('\n')
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        nxt = lines[i + 1] if i + 1 < n else None
        if not line.strip():
            i += 1
            continue
        m = FENCE.match(line)
        if m:
            fence, info = m.group(2), m.group(3).strip()
            body = []
            i += 1
            while i < n and not re.match(r'^\s*' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*$', lines[i]):
                body.append(lines[i])
                i += 1
            i += 1
            parts = info.split(None, 1)
            lang = parts[0].lower() if parts else ''
            rest = parts[1] if len(parts) > 1 else ''
            flags = [w for w in rest.split() if w in ('idiom', 'nocover', 'cover')]
            caption = ' '.join(w for w in rest.split() if w not in ('idiom', 'nocover', 'cover'))
            blocks.append(dict(kind='code', lines=body, lang=lang, flags=flags, caption=caption))
            continue
        m = HEADING.match(line)
        if m:
            level = len(m.group(1))
            t = m.group(2)
            hid = None
            mi = re.search(r'\s*\{#([\w.-]+)\}\s*$', t)
            if mi:
                hid = mi.group(1)
                t = t[:mi.start()]
            text_plain = seg_text(parse_inline(t)).strip()
            blocks.append(dict(kind='h', level=2 if level <= 2 else 3, text=text_plain, explicit_id=hid))
            i += 1
            continue
        if PLACEHOLDER.match(line.strip()):
            blocks.append(dict(kind='placeholder', name=PLACEHOLDER.match(line.strip()).group(1)))
            i += 1
            continue
        if HR.match(line):
            i += 1
            continue
        if line.lstrip().startswith('>'):
            inner = []
            while i < n and lines[i].lstrip().startswith('>'):
                inner.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            tone = 'neutral'
            if inner and re.match(r'^\[!(\w+)\]\s*$', inner[0].strip()):
                tone = ALERTS.get(re.match(r'^\[!(\w+)\]', inner[0].strip()).group(1).upper(), 'info')
                inner = inner[1:]
            paras, buf = [], []
            for l in inner + ['']:
                if l.strip():
                    buf.append(l.strip())
                elif buf:
                    paras.append(parse_inline(' '.join(buf)))
                    buf = []
            title = None
            first = [x for x in paras[0] if x['text'].strip()] if paras else []
            if len(paras) > 1 and first and all(x['b'] for x in first):
                title = seg_text(paras[0]).strip()
                paras = paras[1:]
            blocks.append(dict(kind='callout', tone=tone, title=title, paras=paras))
            continue
        if line.lstrip().startswith('|') and nxt is not None and TABLE_DELIM.match(nxt):
            header = [make_cell(c) for c in split_row(line)]
            rows = []
            i += 2
            while i < n and lines[i].lstrip().startswith('|'):
                cells = [make_cell(c) for c in split_row(lines[i])]
                cells = (cells + [make_cell('') for _ in header])[:len(header)]
                rows.append(cells)
                i += 1
            blocks.append(dict(kind='table', header=header, rows=rows))
            continue
        m = LIST_ITEM.match(line)
        if m:
            ordered = m.group(1)[0].isdigit()
            items = []
            while i < n:
                m = LIST_ITEM.match(lines[i])
                if m:
                    items.append([m.group(2).strip()])
                    i += 1
                elif lines[i].strip() and items and not is_block_start(lines[i], lines[i + 1] if i + 1 < n else None):
                    items[-1].append(lines[i].strip())
                    i += 1
                else:
                    break
            blocks.append(dict(kind='list', ordered=ordered, items=[parse_inline(' '.join(x)) for x in items]))
            continue
        buf = []
        while i < n and lines[i].strip() and not (buf and is_block_start(lines[i], lines[i + 1] if i + 1 < n else None)):
            buf.append(lines[i].strip())
            i += 1
        blocks.append(para_block(parse_inline(' '.join(buf))))
    return blocks


def parse_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read().replace('\r\n', '\n')
    meta, body = split_front_matter(text)
    return meta, parse_blocks(body)
