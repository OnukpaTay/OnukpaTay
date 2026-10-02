#!/usr/bin/env python3
"""Read a deliverables register and print the rollups a status deck needs.

    python3 read_register.py register.xlsx
    python3 read_register.py new.xlsx --compare old.xlsx

Handles the parsing traps these files carry: merged cells that must be filled
only inside their real range, mixed date formats in one column, and registers
that are live snapshots rather than cumulative lists.

Requires openpyxl.
"""
import argparse, datetime, re, sys
from collections import OrderedDict

try:
    import openpyxl
except ImportError:
    sys.exit("pip install openpyxl")

HEADERS = {
    'project':     ('project',),
    'deliverable': ('deliverable',),
    'due':         ('date', 'finish', 'due'),
    'planned':     ('planned',),
    'actual':      ('actual',),
    'owner':       ('person', 'responsible', 'owner'),
    'remark':      ('remark', 'comment', 'note', 'status'),
}


def find_header_row(ws):
    """The header row is the first with 3+ cells matching known column names."""
    for r in range(1, min(ws.max_row, 20) + 1):
        hits = 0
        for c in range(1, min(ws.max_column, 30) + 1):
            v = str(ws.cell(r, c).value or '').strip().lower()
            if v and any(k in v for words in HEADERS.values() for k in words):
                hits += 1
        if hits >= 3:
            return r
    return 4


def map_columns(ws, hrow):
    cols = {}
    for c in range(1, min(ws.max_column, 30) + 1):
        v = str(ws.cell(hrow, c).value or '').strip().lower()
        if not v:
            continue
        for key, words in HEADERS.items():
            if key not in cols and any(w in v for w in words):
                cols[key] = c
                break
    return cols


def merge_map(ws):
    """Value of each cell covered by a merged range, keyed (row, col).

    Filling a column straight down is wrong: it carries a value into rows the
    merge never covered and silently inflates counts.
    """
    m = {}
    for rng in ws.merged_cells.ranges:
        top = ws.cell(rng.min_row, rng.min_col).value
        for r in range(rng.min_row, rng.max_row + 1):
            for c in range(rng.min_col, rng.max_col + 1):
                m[(r, c)] = top
    return m


def parse_dates(raw):
    """Resolve a column of mixed real dates and text dates to real dates.

    Text entries with a day above 12 are unambiguous, so they reveal whether the
    sheet is written day-first or month-first; everything else follows that.
    """
    day_first = True
    for v in raw:
        if isinstance(v, str):
            p = re.split(r'[/\-.]', v.strip())
            if len(p) == 3 and p[0].isdigit() and p[1].isdigit():
                a, b = int(p[0]), int(p[1])
                if a > 12:
                    day_first = True
                    break
                if b > 12:
                    day_first = False
                    break
    out = []
    for v in raw:
        if isinstance(v, datetime.datetime):
            out.append(v.date())
        elif isinstance(v, datetime.date):
            out.append(v)
        elif isinstance(v, str) and v.strip():
            p = re.split(r'[/\-.]', v.strip())
            try:
                a, b, y = int(p[0]), int(p[1]), int(p[2])
                if y < 100:
                    y += 2000
                out.append(datetime.date(y, b, a) if day_first else datetime.date(y, a, b))
            except Exception:
                out.append(None)
        else:
            out.append(None)
    return out, day_first


def num(v):
    if v in (None, ''):
        return 0.0
    if isinstance(v, str):
        v = v.strip().rstrip('%')
        try:
            f = float(v)
        except ValueError:
            return 0.0
        return f / 100 if f > 1 else f
    return float(v)


def load(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[wb.sheetnames[0]]
    hrow = find_header_row(ws)
    cols = map_columns(ws, hrow)
    if 'deliverable' not in cols:
        sys.exit(f"could not find a deliverable column in {path}; headers at row {hrow}: {cols}")
    mm = merge_map(ws)

    def val(r, key):
        c = cols.get(key)
        if not c:
            return None
        v = ws.cell(r, c).value
        return v if v not in (None, '') else mm.get((r, c))

    rows = []
    for r in range(hrow + 1, ws.max_row + 1):
        if val(r, 'deliverable') in (None, ''):
            if not any(val(r, k) not in (None, '') for k in ('project', 'planned', 'actual')):
                break
            continue
        rows.append({
            'row': r,
            'project': str(val(r, 'project') or '').strip(),
            'deliverable': re.sub(r'\s+', ' ', str(val(r, 'deliverable'))).strip(),
            'due_raw': val(r, 'due'),
            'planned': num(val(r, 'planned')),
            'actual': num(val(r, 'actual')),
            'owners': [o.strip() for o in re.split(r'[\n,/]', str(val(r, 'owner') or '')) if o.strip()],
            'remark': re.sub(r'\s+', ' ', str(val(r, 'remark') or '')).strip(),
        })
    dates, day_first = parse_dates([x['due_raw'] for x in rows])
    for x, d in zip(rows, dates):
        x['due'] = d
    return rows, day_first, ws.title


def key(x):
    return (x['project'].lower(), x['deliverable'].lower())


def report(rows, day_first, sheet, path):
    n = len(rows)
    if not n:
        sys.exit("no deliverable rows found")
    sp, sa = sum(x['planned'] for x in rows), sum(x['actual'] for x in rows)
    done = [x for x in rows if x['actual'] >= 1]
    prog = [x for x in rows if 0 < x['actual'] < 1]
    ns   = [x for x in rows if x['actual'] == 0]

    print(f"\n{'='*66}\n{path}   sheet {sheet!r}   dates read {'day' if day_first else 'month'}-first\n{'='*66}")
    print(f"deliverables {n}   projects {len(set(x['project'] for x in rows))}")
    print(f"delivered {len(done)} ({len(done)/n*100:.1f}%)   "
          f"in progress {len(prog)} ({len(prog)/n*100:.1f}%)   "
          f"not started {len(ns)} ({len(ns)/n*100:.1f}%)")
    print(f"actual {sa:g}/{n} = {sa/n*100:.2f}%   planned {sp:g}/{n} = {sp/n*100:.2f}%")
    print(f"variance {(sa-sp)/n*100:+.2f} points = {sa-sp:+g} deliverables")

    today = datetime.date.today()
    bad = [x for x in rows if x['due'] and abs((x['due'] - today).days) > 300]
    if bad:
        print("\n!! dates far from today — check for a typo in the source")
        for x in bad:
            print(f"   {x['project']} / {x['deliverable']}: {x['due']:%d %b %Y}")

    if prog or ns:
        print("\nOUTSTANDING (ordered by exposure)")
        for x in sorted(prog + ns, key=lambda t: t['actual']):
            d = f"{x['due']:%d %b %Y}" if x['due'] else '-'
            print(f"  {x['project'][:26]:26s} {x['deliverable'][:30]:30s} {d:12s} "
                  f"P{x['planned']*100:4.0f}% A{x['actual']*100:4.0f}%  gap {x['planned']-x['actual']:+.2f}  "
                  f"{'/'.join(x['owners'])}")

    byp = OrderedDict()
    for x in rows:
        d = byp.setdefault(x['project'], {'n': 0, 'p': 0.0, 'a': 0.0})
        d['n'] += 1; d['p'] += x['planned']; d['a'] += x['actual']
    full = [k for k, v in byp.items() if v['a'] == v['n']]
    print(f"\nBY PROJECT — {len(full)} of {len(byp)} fully delivered")
    for k, v in byp.items():
        mark = ' ' if v['a'] == v['n'] else '*'
        print(f" {mark}{k[:30]:30s} n={v['n']}  planned {v['p']/v['n']*100:5.1f}%  actual {v['a']/v['n']*100:5.1f}%")

    byo = {}
    for x in rows:
        for o in x['owners']:
            d = byo.setdefault(o, {'n': 0, 'd': 0})
            d['n'] += 1
            if x['actual'] >= 1:
                d['d'] += 1
    if byo:
        print("\nBY OWNER (shared items count once per named owner)")
        for k, v in sorted(byo.items(), key=lambda t: -t[1]['n']):
            print(f"  {k[:14]:14s} total {v['n']:2d}  delivered {v['d']:2d}  open {v['n']-v['d']:2d}")
        print(f"  sum of owner totals = {sum(v['n'] for v in byo.values())} (vs {n} deliverables)")

    flags = {}
    for x in rows:
        if x['remark']:
            flags.setdefault(x['remark'][:48], []).append(x)
    if flags:
        print("\nREMARK FLAGS — a repeated flag is usually the real story")
        for f, items in sorted(flags.items(), key=lambda t: -len(t[1])):
            print(f"  [{len(items)}] {f}")
            for x in items:
                print(f"        {x['project'][:26]:26s} {x['deliverable'][:34]}")
    return rows


def compare(new, old):
    kn, ko = {key(x): x for x in new}, {key(x): x for x in old}
    print(f"\n{'='*66}\nWEEK ON WEEK\n{'='*66}")
    shrink = len(old) - len(new)
    if shrink > max(3, 0.3 * len(old)):
        print(f"!! the register shrank by {shrink} rows ({len(old)} -> {len(new)}).")
        print("   It is a live snapshot, so portfolio percentages are NOT comparable")
        print("   between periods. Compare deliverables individually and say so on the slide.\n")
    for k, x in kn.items():
        m = ko.get(k)
        if m:
            tag = 'CARRIED ' if x['actual'] != m['actual'] else 'NO MOVE '
            print(f"  {tag} {x['project'][:26]:26s} {x['deliverable'][:30]:30s} "
                  f"{m['actual']*100:5.0f}% -> {x['actual']*100:5.0f}%  ({(x['actual']-m['actual'])*100:+.0f})")
        else:
            print(f"  NEW      {x['project'][:26]:26s} {x['deliverable'][:30]:30s}   -> {x['actual']*100:5.0f}%")
    gone = [x for k, x in ko.items() if k not in kn]
    print(f"\n  {len(gone)} row(s) dropped since the previous register")
    for x in gone:
        print(f"     {x['project'][:26]:26s} {x['deliverable'][:34]:34s} was {x['actual']*100:.0f}%")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('register')
    ap.add_argument('--compare', metavar='PREVIOUS')
    a = ap.parse_args()
    rows, df, sheet = load(a.register)
    report(rows, df, sheet, a.register)
    if a.compare:
        old, odf, osheet = load(a.compare)
        report(old, odf, osheet, a.compare)
        compare(rows, old)
