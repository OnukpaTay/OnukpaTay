#!/usr/bin/env python3
"""Recalculate every formula in an .xlsx without Excel/LibreOffice and report errors.

usage: recalc_check.py BOOK.xlsx ["SHEET!A1" ...]
  - prints the number of #REF!/#VALUE!/#DIV/0!/#NAME? results per sheet (must be 0)
  - prints the value of each requested cell (e.g. the General Summary total)
  - writes vals.pkl ({"'[BOOK.XLSX]SHEET'!A1": value}) for inject_cached_values.py
Needs: pip install formulas.  ~1 min for a 20-sheet, 40k-cell BOQ.
Delete external links / stale defined names first ("[31]!Name" refs break the parser).
"""
import formulas, sys, time, collections, pickle, os
src = sys.argv[1]; t = time.time()
sol = formulas.ExcelModel().loads(src).finish().calculate()
book = os.path.basename(src).upper()
errs = collections.Counter(); vals = {}
for k, v in sol.items():
    try: x = v.value[0][0]
    except Exception: x = v
    if str(x).startswith('#'): errs[k.split('!')[0]] += 1
    vals[k.upper()] = float(x) if isinstance(x, (int, float)) else str(x)
print('recalc %.0fs | formula errors: %d %s' % (time.time() - t, sum(errs.values()), dict(errs)))
for c in sys.argv[2:]:
    sh, ref = c.rsplit('!', 1)
    print(c, '=', vals.get("'[%s]%s'!%s" % (book, sh.strip("'").upper(), ref.upper())))
pickle.dump(vals, open('vals.pkl', 'wb'))
