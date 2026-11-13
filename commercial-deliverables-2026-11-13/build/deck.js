/* Deck kit: tokens and helpers for a management status deck.
 * Copy this to the top of your generator, change REPORT_DATE and the title,
 * then add slides. See references/design-system.md for the why behind the
 * colours, and for the pptxgenjs traps these helpers already work around.
 */
const pptxgen = require('pptxgenjs');

/* ---------------- design tokens ---------------- */
const W = 13.333, H = 7.5, M = 0.62, CW = W - 2 * M;   // content width 12.093
const NAVY='1B2A41', NAVY2='2A3E58', INK='0B0B0B', INK2='52514E', MUTED='898781';
const PANEL='F2F5F8', TRACK='E3E9F0', LINE='E1E0D9', WHITE='FFFFFF';
const BLUE='2A78D6', ORANGE='EB6834';                   // validated categorical pair
const GOOD='0CA30C', WARN='FAB219', CRIT='D03B3B', SERIOUS='EC835A';   // reserved status palette
const AMBER='E08A3C', ICE='AFC1D6';
const HF='Cambria', BF='Calibri';
const CONTENT_BOTTOM = 6.58;

const sh = (o) => Object.assign({ type:'outer', color:'1B2A41', blur:12, offset:2, angle:90, opacity:0.10 }, o||{});
const T  = (o) => Object.assign({ isTextBox:true, margin:0, fontFace:BF, color:INK2 }, o);

const REPORT_DATE = '13 November 2026';
const DEPARTMENT  = 'Commercial Department';
const DECK_TITLE  = 'Outstanding Projects & Deliverables';

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'Commercial Department';   // <- your department
pres.title  = 'Commercial Department — Outstanding Projects & Deliverables';

/* ---------------- helpers ---------------- */
function footer(s, n){
  s.addText(`${DEPARTMENT}   ·   ${DECK_TITLE}   ·   ${REPORT_DATE}`,
    T({ x:M, y:6.95, w:9.8, h:0.30, fontSize:9, color:MUTED, valign:'middle' }));
  s.addText(String(n), T({ x:W-M-0.7, y:6.95, w:0.7, h:0.30, fontSize:9, color:MUTED, align:'right', valign:'middle' }));
}

function header(s, eyebrow, title, subtitle){
  s.addText(eyebrow, T({ x:M, y:0.46, w:CW, h:0.24, fontSize:10.5, bold:true, color:BLUE, charSpacing:1.6, valign:'middle' }));
  s.addText(title,   T({ x:M, y:0.74, w:CW, h:0.62, fontSize:31, bold:true, fontFace:HF, color:NAVY, valign:'middle' }));
  if (subtitle){
    s.addText(subtitle, T({ x:M, y:1.38, w:CW, h:0.32, fontSize:12.5, color:INK2, valign:'middle' }));
    return 1.86;
  }
  return 1.54;
}

function card(s, x, y, w, h, opt){
  opt = opt || {};
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: opt.r || 0.10,
    fill: { color: opt.fill || WHITE },
    line: { color: opt.lineColor || LINE, width: opt.lineWidth === undefined ? 1 : opt.lineWidth },
    shadow: opt.flat ? { type:'outer', color:'FFFFFF', blur:0, offset:0, angle:90, opacity:0 } : sh()
  });
}

function dot(s, cx, cy, d, color, label, labelColor){
  s.addShape(pres.ShapeType.ellipse, { x:cx-d/2, y:cy-d/2, w:d, h:d, fill:{color}, line:{ type:'none' } });
  if (label !== undefined){
    s.addText(label, T({ x:cx-d/2, y:cy-d/2, w:d, h:d, fontSize: d>=0.44 ? 13 : 10, bold:true,
      color: labelColor || WHITE, align:'center', valign:'middle' }));
  }
}

/* progress track with an "actual" fill and a "planned" tick marker */
function progress(s, x, y, w, actual, planned, fillColor, h){
  h = h || 0.17;
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius:h/2, fill:{color:TRACK}, line:{type:'none'} });
  const aw = Math.max(0.055, w * actual);
  if (actual > 0){
    s.addShape(pres.ShapeType.roundRect, { x, y, w:aw, h, rectRadius:h/2, fill:{color:fillColor}, line:{type:'none'} });
  }
  if (planned !== null && planned !== undefined && planned > 0){
    const px = x + w * planned;
    s.addShape(pres.ShapeType.rect, { x: Math.min(px, x+w-0.035), y:y-0.075, w:0.035, h:h+0.15,
      fill:{color:NAVY}, line:{type:'none'} });
  }
}

function chip(s, x, y, w, h, text, bg, fg){
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius:h/2, fill:{color:bg}, line:{type:'none'} });
  s.addText(text, T({ x, y, w, h, fontSize:9, bold:true, color:fg||WHITE, align:'center', valign:'middle', charSpacing:0.4 }));
}




/* ================= SLIDE 1 — TITLE ================= */
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.ShapeType.ellipse, { x:10.35, y:-1.45, w:4.6, h:4.6, fill:{color:'FFFFFF', transparency:94}, line:{type:'none'} });
  s.addShape(pres.ShapeType.ellipse, { x:11.55, y:0.55,  w:2.5, h:2.5, fill:{color:AMBER,   transparency:86}, line:{type:'none'} });
  s.addShape(pres.ShapeType.ellipse, { x:-1.60, y:6.05,  w:3.3, h:3.3, fill:{color:'FFFFFF', transparency:96}, line:{type:'none'} });

  s.addText('COMMERCIAL DEPARTMENT   ·   PRE & POST CONTRACT',
    T({ x:M, y:1.52, w:10.5, h:0.3, fontSize:12, bold:true, color:AMBER, charSpacing:2.2, valign:'middle' }));
  s.addText('Outstanding Projects\n& Deliverables',
    T({ x:M, y:1.95, w:9.4, h:1.85, fontSize:46, bold:true, fontFace:HF, color:WHITE, lineSpacingMultiple:1.02, valign:'top' }));
  s.addText('Weekly status report to Management',
    T({ x:M, y:3.92, w:9.4, h:0.38, fontSize:19, color:ICE, valign:'middle' }));
  chip(s, M, 4.52, 2.25, 0.42, '13 NOVEMBER 2026', AMBER, '1B2A41');

  const stats = [['23','Deliverables tracked'],['10','Active projects'],['74%','Delivered'],['5','Due today, unfinished']];
  const bw = 2.72, gap = 0.30;
  stats.forEach((st, i) => {
    const x = M + i * (bw + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y:5.42, w:bw, h:1.10, rectRadius:0.10,
      fill:{ color:'FFFFFF', transparency:90 }, line:{ color:'FFFFFF', width:0.75, transparency:72 } });
    s.addText(st[0], T({ x:x+0.20, y:5.54, w:bw-0.40, h:0.50, fontSize:27, bold:true, fontFace:HF, color:WHITE, valign:'middle' }));
    s.addText(st[1], T({ x:x+0.20, y:6.03, w:bw-0.40, h:0.30, fontSize:10, color:ICE, valign:'middle' }));
  });
  s.addText('Presented by the Commercial Manager', T({ x:M, y:6.88, w:7.5, h:0.30, fontSize:10.5, color:ICE, valign:'middle' }));
  s.addNotes('Good morning. Twenty-three deliverables on the register this week across ten projects, seventeen of them finished. I have to be blunt about the rest: six are still open and five of those fall due today. Very little moved in the last seven days and I need decisions on two of them before we leave.');
}

/* ================= SLIDE 2 — EXECUTIVE SUMMARY ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'AT A GLANCE', 'Executive Summary',
    'Position of the commercial deliverables register as at 13 November 2026.');

  const tiles = [
    ['23', 'Deliverables tracked', 'Across 10 active projects', NAVY],
    ['17', 'Delivered', '74% of the register', GOOD],
    ['6',  'Still open', '5 of them fall due today', WARN],
    ['8',  'Weeks on one blocker', 'Priority Insurance drawings', CRIT]
  ];
  const tw = (CW - 3 * 0.28) / 4, th = 1.52;
  tiles.forEach((t, i) => {
    const x = M + i * (tw + 0.28);
    card(s, x, y0, tw, th, { fill: PANEL, lineWidth: 0, flat: true });
    dot(s, x + tw - 0.34, y0 + 0.32, 0.18, t[3]);
    s.addText(t[0], T({ x:x+0.26, y:y0+0.16, w:tw-0.75, h:0.62, fontSize:40, bold:true, fontFace:HF, color:NAVY, valign:'middle' }));
    s.addText(t[1], T({ x:x+0.26, y:y0+0.80, w:tw-0.50, h:0.30, fontSize:12.5, bold:true, color:INK, valign:'middle' }));
    s.addText(t[2], T({ x:x+0.26, y:y0+1.10, w:tw-0.50, h:0.28, fontSize:9.5, color:MUTED, valign:'middle' }));
  });

  const rows = [
    [CRIT, 'Five of the six open deliverables fall due today',
     'Three Priority Insurance items, the Barry Callebaut Factory valuation and its new variation BoQ. Only the RE Villa variation, due Monday, has any time left on it.'],
    [CRIT, 'Three of the four items open a week ago have not moved at all',
     'The Priority Insurance BoQ is still at 50%, its budget still at 10% and the Barry Callebaut valuation still at 90%. Only the preliminaries budget advanced, from 50% to 70%.'],
    [WARN, 'Four new deliverables came on and two closed',
     'Variation work on Barry Callebaut, Thoroughbred and RE Villa, plus the GIA revised MEP valuation. Separately, two finished items have now been awaiting review for a week.']
  ];
  const ry = y0 + th + 0.26, rh = 0.94, rg = 0.12;
  rows.forEach((r, i) => {
    const y = ry + i * (rh + rg);
    card(s, M, y, CW, rh);
    dot(s, M + 0.52, y + rh/2, 0.46, r[0], String(i+1), r[0] === WARN ? NAVY : WHITE);
    s.addText(r[1], T({ x:M+0.98, y:y+0.13, w:CW-1.30, h:0.28, fontSize:13, bold:true, color:NAVY, valign:'middle' }));
    s.addText(r[2], T({ x:M+0.98, y:y+0.43, w:CW-1.30, h:0.36, fontSize:10.5, color:INK2, valign:'top' }));
  });

  footer(s, 2);
  s.addNotes('Three things. First, five of the six open items are due today and will not all be met. Second, and this is the one that concerns me, three of the four items that were open last Friday are in exactly the same place this Friday. Third, the register grew by four while two closed, so the volume is healthy, it is the movement that is not.');
}

/* ================= SLIDE 3 — WHERE THEY STAND ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'PORTFOLIO HEALTH', 'Where the 23 Deliverables Stand');

  s.addChart(pres.ChartType.doughnut,
    [{ name:'Status', labels:['Delivered','On plan, incomplete','Behind plan'], values:[17, 2, 4] }],
    { x:M, y:y0+0.10, w:5.30, h:4.50, holeSize:62, showTitle:false, showLegend:false, showValue:false,
      chartColors:[GOOD, MUTED, WARN], dataBorder:{ pct:2, color:WHITE } });
  s.addText('23', T({ x:2.27, y:3.34, w:2.0, h:0.62, fontSize:40, bold:true, fontFace:HF, color:NAVY, align:'center', valign:'middle' }));
  s.addText('deliverables', T({ x:2.27, y:3.94, w:2.0, h:0.28, fontSize:11, color:MUTED, align:'center', valign:'middle' }));

  const rx = 6.30, rw = W - M - rx;
  const legend = [
    [GOOD,  'Delivered',           'Finished; 2 have awaited review a week', 17, '74%'],
    [MUTED, 'On plan, incomplete', 'Both Priority Insurance, both due today', 2, '9%'],
    [WARN,  'Behind plan',         'Two Barry Callebaut, one each elsewhere', 4, '17%']
  ];
  const lh = 0.80, lg = 0.13;
  legend.forEach((l, i) => {
    const y = y0 + 0.16 + i * (lh + lg);
    card(s, rx, y, rw, lh, { fill: PANEL, lineWidth: 0, flat: true });
    dot(s, rx + 0.36, y + lh/2, 0.26, l[0]);
    s.addText(l[1], T({ x:rx+0.68, y:y+0.13, w:3.00, h:0.28, fontSize:13, bold:true, color:NAVY, valign:'middle' }));
    s.addText(l[2], T({ x:rx+0.68, y:y+0.41, w:3.20, h:0.26, fontSize:9.5, color:MUTED, valign:'middle' }));
    s.addText(String(l[3]), T({ x:rx+3.95, y:y+0.17, w:1.05, h:0.46, fontSize:24, bold:true, fontFace:HF, color:NAVY, align:'right', valign:'middle' }));
    s.addText(l[4], T({ x:rx+5.06, y:y+0.26, w:1.05, h:0.30, fontSize:12, color:INK2, align:'right', valign:'middle' }));
  });

  const py = y0 + 0.16 + 3 * (lh + lg) + 0.22;
  card(s, rx, py, rw, 1.66);
  s.addText('Progress against plan', T({ x:rx+0.22, y:py+0.16, w:rw-0.44, h:0.28, fontSize:12.5, bold:true, color:NAVY, valign:'middle' }));
  [['Planned', 0.939, '93.9%', ORANGE], ['Actual', 0.906, '90.6%', BLUE]].forEach((b, i) => {
    const by = py + 0.56 + i * 0.40;
    s.addText(b[0], T({ x:rx+0.22, y:by-0.04, w:1.05, h:0.26, fontSize:10.5, color:INK2, valign:'middle' }));
    progress(s, rx+1.34, by, 3.10, b[1], null, b[3], 0.17);
    s.addText(b[2], T({ x:rx+4.56, y:by-0.05, w:1.60, h:0.28, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
  });
  s.addText('3.3 points behind plan — three quarters of one deliverable',
    T({ x:rx+0.22, y:py+1.32, w:rw-0.44, h:0.26, fontSize:10.5, bold:true, color:WARN === WARN ? '9A6B00' : NAVY, valign:'middle' }));

  footer(s, 3);
  s.addNotes('Seventeen of twenty-three finished. Two are incomplete but sitting exactly where the plan says, though I would note the plan says fifty per cent on the day the item is due. Four are genuinely behind. On progress we are at ninety point six against a planned ninety-three point nine, so three points, about three quarters of a deliverable.');
}

/* ================= SLIDE 4 — WHAT MOVED ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'MOVEMENT', 'What Moved Since 6 November',
    'Every deliverable that was open a week ago, then and now.');

  // data[0] plots at the BOTTOM, so the only item that moved ends up on top
  const mv = [
    ['Barry Callebaut — Valuation',        90,  90],
    ['Priority Ins. — Complete Budget',    10,  10],
    ['Priority Ins. — Complete BoQ',       50,  50],
    ['Priority Ins. — Preliminaries budget',50, 70]
  ];
  const cw2 = 8.35;
  s.addChart(pres.ChartType.bar, [
    { name:'6 November',  labels: mv.map(p=>p[0]), values: mv.map(p=>p[1]) },
    { name:'13 November', labels: mv.map(p=>p[0]), values: mv.map(p=>p[2]) }
  ], {
    x:M, y:y0, w:cw2, h:4.10, barDir:'bar', barGrouping:'clustered', barGapWidthPct:38,
    chartColors:[ORANGE, BLUE], showTitle:false,
    showLegend:true, legendPos:'t', legendFontSize:11, legendColor:INK2,
    showValue:true, dataLabelPosition:'outEnd', dataLabelFontSize:10, dataLabelColor:INK2,
    dataLabelFormatCode:'0"%"',
    valAxisMinVal:0, valAxisMaxVal:112, valAxisMajorUnit:25,
    valAxisLabelFontSize:9.5, valAxisLabelColor:MUTED, valAxisLabelFormatCode:'0"%"',
    catAxisLabelFontSize:10, catAxisLabelColor:INK2,
    valGridLine:{ color:LINE, size:1 }, catGridLine:{ style:'none' },
    valAxisLineColor:LINE, catAxisLineColor:LINE,
    catAxisLabelFontFace:BF, valAxisLabelFontFace:BF, dataLabelFontFace:BF, legendFontFace:BF
  });

  s.addText('The register carries live work only, so the overall percentages on slide 3 are not comparable between weeks. This chart compares individual deliverables, which is.',
    T({ x:M, y:y0+4.18, w:cw2, h:0.40, fontSize:9, color:MUTED, valign:'top' }));

  const rx = M + cw2 + 0.32, rw = W - M - rx;
  const panels = [
    [CRIT, '1', 'of 4 open items moved', 'The preliminaries budget went from 50% to 70%. The other three sit exactly where they were seven days ago.'],
    [BLUE, '4', 'new deliverables added', 'Variation work on Barry Callebaut, Thoroughbred and RE Villa, plus the GIA revised MEP valuation. Two of the four are already finished.']
  ];
  panels.forEach((p, i) => {
    const y = y0 + i * 2.28;
    card(s, rx, y, rw, 2.08, { fill: PANEL, lineWidth: 0, flat: true });
    dot(s, rx + rw - 0.38, y + 0.36, 0.20, p[0]);
    s.addText(p[1], T({ x:rx+0.26, y:y+0.18, w:rw-0.80, h:0.72, fontSize:46, bold:true, fontFace:HF, color:NAVY, valign:'middle' }));
    s.addText(p[2], T({ x:rx+0.26, y:y+0.92, w:rw-0.52, h:0.30, fontSize:12.5, bold:true, color:INK, valign:'middle' }));
    s.addText(p[3], T({ x:rx+0.26, y:y+1.26, w:rw-0.52, h:0.68, fontSize:10, color:INK2, valign:'top' }));
  });

  footer(s, 4);
  s.addNotes('This is the slide I would look at hardest. Four deliverables were open last Friday. One of them moved. The Priority Insurance BoQ, its budget and the Barry Callebaut valuation are flat lines across seven days. The register did grow by four new items and two of those are already closed, so the team is producing; it is these four that are stuck.');
}

/* ================= SLIDE 5 — DELIVERED ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'COMPLETED WORK', '17 Deliverables Finished Across 10 Projects');

  const done = [
    ['Thoroughbred Place', 3, ['Valuation', 'Budgetary report', 'Variation — relaxation room'], 'Sedem', false],
    ['RE Villa', 3, ['Budgetary Report', 'Budgetary Report', 'Valuation'], 'Eunice', false],
    ['Vanguard Assurance', 2, ['Valuation', 'Budgetary report'], 'Gilbert', false],
    ['Enterprise COO Office', 2, ['Valuation', 'Budgetary Report'], 'Eunice', false],
    ['Priority Insurance', 2, ['Cash Flow', 'Extraction of Labour Rates'], 'Sedem, Gilbert', false],
    ['Goldfied', 1, ['Report on Omitted Items'], 'Sedem, Gilbert', false],
    ['Barry Callebaut Factory', 1, ['Budgetary report'], 'Gilbert', false],
    ['Barry Callebaut Fitout', 1, ['BoQ'], 'Tracy', true],
    ["Ecole Int'l School", 1, ['Cash Flow'], 'Tracy, Obed, Eunice', true],
    ['GIA', 1, ['Revised MEP Valuation and Payment'], 'Eunice, Sedem', false]
  ];

  const COLS = 4, GX = 0.24, GY = 0.20, GRID_BOTTOM = 6.34;
  const cw = (CW - (COLS - 1) * GX) / COLS;
  const chh = (GRID_BOTTOM - y0 - 2 * GY) / 3;
  done.forEach((d, i) => {
    const x = M + (i % COLS) * (cw + GX);
    const y = y0 + Math.floor(i / COLS) * (chh + GY);
    card(s, x, y, cw, chh);
    dot(s, x + cw - 0.34, y + 0.32, 0.40, GOOD, String(d[1]));
    if (d[4]) dot(s, x + cw - 0.66, y + 0.32, 0.16, WARN);
    s.addText(d[0], T({ x:x+0.22, y:y+0.14, w:cw-1.12, h:0.44, fontSize:11, bold:true, fontFace:HF, color:NAVY, valign:'top' }));
    s.addText(d[2].map((t, j) => ({ text:t, options:{ bullet:{ indent:13 }, breakLine: j < d[2].length - 1 } })),
      T({ x:x+0.30, y:y+0.60, w:cw-0.56, h:0.58, fontSize:8.5, color:INK2, paraSpaceAfter:2, valign:'top' }));
    s.addText(d[3], T({ x:x+0.22, y:y+chh-0.32, w:cw-0.44, h:0.24, fontSize:8.5, bold:true, color:MUTED, valign:'middle' }));
  });

  s.addText([
    { text:'An amber dot marks a finished deliverable still awaiting review. Both have now been in the queue a week.', options:{ breakLine:true } },
    { text:'The register lists the RE Villa budgetary report twice, in rows 21 and 22. Counts follow the register as issued; the distinct totals are 22 deliverables and 16 delivered.', options:{} }
  ], T({ x:M, y:6.42, w:CW, h:0.46, fontSize:8.5, color:MUTED, paraSpaceAfter:2, valign:'top' }));

  footer(s, 5);
  s.addNotes('Seventeen finished across ten projects. Thoroughbred and RE Villa carried three each. Two are marked with an amber dot because they are done but still waiting on a reviewer, and they are the same two I flagged last week. One housekeeping point: the register lists the RE Villa budgetary report twice, so the true distinct count is twenty-two and sixteen, and that is worth tidying at source.');
}

/* ================= SLIDE 6 — STILL OPEN ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'THE WATCH LIST', '6 Open Deliverables, 5 of Them Due Today');

  const out = [
    ['Priority Insurance', 'Complete Budget',                            0.10, 0.10, '13 Nov', 'Sedem, Gilbert', CRIT,    'DUE TODAY'],
    ['Priority Insurance', 'Complete BoQ',                               0.50, 0.50, '13 Nov', 'Sedem, Gilbert', CRIT,    'DUE TODAY'],
    ['Priority Insurance', 'Budget for preliminaries and general items', 0.70, 1.00, '13 Nov', 'Obed',           WARN,    'BEHIND'],
    ['Barry Callebaut Factory', 'Variation BoQ',                         0.80, 1.00, '13 Nov', 'Gilbert',        WARN,    'BEHIND'],
    ['Barry Callebaut Factory', 'Valuation',                             0.90, 1.00, '13 Nov', 'Gilbert',        SERIOUS, 'BEHIND'],
    ['RE Villa',          'Variation 4 BOQ',                             0.85, 1.00, '16 Nov', 'Eunice',         MUTED,   'MONDAY']
  ];

  const rh = 0.76, rg = (CONTENT_BOTTOM - y0 - out.length * rh) / (out.length - 1);
  out.forEach((o, i) => {
    const y = y0 + i * (rh + rg);
    card(s, M, y, CW, rh);
    dot(s, M + 0.30, y + rh/2, 0.22, o[6]);
    s.addText(o[0], T({ x:M+0.56, y:y+0.12, w:2.85, h:0.24, fontSize:11, bold:true, color:NAVY, valign:'middle' }));
    s.addText(o[1], T({ x:M+0.56, y:y+0.37, w:3.00, h:0.22, fontSize:9, color:INK2, valign:'middle' }));

    const bx = M + 3.70, bw = 2.55;
    s.addText(`Actual ${Math.round(o[2]*100)}%`,  T({ x:bx, y:y+0.09, w:1.20, h:0.22, fontSize:9, bold:true, color:NAVY, valign:'middle' }));
    s.addText(`Planned ${Math.round(o[3]*100)}%`, T({ x:bx+bw-1.40, y:y+0.09, w:1.40, h:0.22, fontSize:9, color:MUTED, align:'right', valign:'middle' }));
    progress(s, bx, y + 0.38, bw, o[2], o[3], o[6], 0.16);

    s.addText('DUE',   T({ x:M+6.70, y:y+0.11, w:1.20, h:0.18, fontSize:7.5, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(o[4],    T({ x:M+6.70, y:y+0.31, w:1.20, h:0.26, fontSize:10.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText('OWNER', T({ x:M+8.12, y:y+0.11, w:2.10, h:0.18, fontSize:7.5, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(o[5],    T({ x:M+8.12, y:y+0.31, w:2.10, h:0.26, fontSize:9.5, color:INK2, valign:'middle' }));

    chip(s, M + 10.52, y + (rh - 0.32)/2, 1.28, 0.32, o[7], o[6], (o[6] === WARN || o[6] === SERIOUS) ? '1B2A41' : WHITE);
  });

  footer(s, 6);
  s.addNotes('Six open, and the top five are all due today. The two Priority Insurance items at the top are marked on plan in the register, but the plan says fifty per cent and ten per cent on the day they are due, which is not a plan that can be met. Barry Callebaut has two items behind. Only the RE Villa variation, due Monday, has time on it.');
}

/* ================= SLIDE 7 — PRIORITY INSURANCE ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'DEEP DIVE', 'Priority Insurance: Eight Weeks, and the Deadline Is Today',
    'The deadline this project was re-based to on 6 November has now arrived.');

  const LW = 6.10;
  const items = [
    ['Complete BoQ',                              0.50, 0.50, CRIT],
    ['Complete Budget',                           0.10, 0.10, CRIT],
    ['Budget for preliminaries and general items',0.70, 1.00, WARN],
    ['Cash Flow',                                 1.00, 1.00, GOOD],
    ['Extraction of Labour Rates',                1.00, 1.00, GOOD]
  ];
  const rh = 0.84, rg = (CONTENT_BOTTOM - y0 - items.length * rh) / (items.length - 1);
  items.forEach((it, i) => {
    const y = y0 + i * (rh + rg);
    card(s, M, y, LW, rh);
    s.addText(it[0], T({ x:M+0.20, y:y+0.10, w:3.60, h:0.26, fontSize:10.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText('due 13 Nov', T({ x:M+3.85, y:y+0.10, w:1.15, h:0.26, fontSize:9, color:MUTED, align:'right', valign:'middle' }));
    progress(s, M+0.20, y + 0.46, 4.25, it[1], it[2], it[3], 0.16);
    s.addText(`${Math.round(it[1]*100)}%`, T({ x:M+4.58, y:y+0.40, w:1.30, h:0.26, fontSize:10.5, bold:true, color:NAVY, valign:'middle' }));
  });

  const rx = M + LW + 0.32, rw = W - M - rx;
  card(s, rx, y0, rw, 2.92);
  s.addText('The same blocker, four reports running', T({ x:rx+0.24, y:y0+0.14, w:rw-0.48, h:0.28, fontSize:12.5, bold:true, color:NAVY, valign:'middle' }));
  const hist = [
    ['18 Sep', CRIT, 'BoQ 40%, due 30 Sep. Awaiting the floor finishes schedule and the structural drawings.'],
    ['25 Sep', CRIT, 'BoQ 40%, due 30 Sep. No movement in seven days.'],
    ['06 Nov', WARN, 'BoQ 50%, deadline re-based to 13 Nov. Structural drawings still outstanding.'],
    ['13 Nov', CRIT, 'BoQ still 50%. The re-based deadline is today and the drawings have not come.']
  ];
  hist.forEach((h, i) => {
    const hy = y0 + 0.54 + i * 0.58;
    dot(s, rx + 0.40, hy + 0.15, 0.18, h[1]);
    s.addText(h[0], T({ x:rx+0.58, y:y0+0.54+i*0.58, w:0.95, h:0.26, fontSize:10.5, bold:true, fontFace:HF, color:NAVY, valign:'middle' }));
    s.addText(h[2], T({ x:rx+1.58, y:hy-0.02, w:rw-1.82, h:0.52, fontSize:9, color:INK2, valign:'top' }));
  });

  card(s, rx, y0 + 3.14, rw, 1.58, { fill: PANEL, lineWidth: 0, flat: true });
  s.addText('Eight weeks, ten points of progress', T({ x:rx+0.24, y:y0+3.28, w:rw-0.48, h:0.28, fontSize:11.5, bold:true, color:CRIT, valign:'middle' }));
  s.addText('The take-off has read 90% complete at every report since 18 September. Waiting has not worked, and the deadline we moved it to has arrived with the BoQ at half.',
    T({ x:rx+0.24, y:y0+3.58, w:rw-0.48, h:0.56, fontSize:10, color:INK2, valign:'top' }));
  s.addText('Ask: approve pricing the structural element provisionally so the BoQ can close, and set a new date today.',
    T({ x:rx+0.24, y:y0+4.16, w:rw-0.48, h:0.46, fontSize:10, bold:true, color:NAVY, valign:'top' }));

  footer(s, 7);
  s.addNotes('I raised this on 18 September, on 25 September and again last Friday. The architectural take-off has read ninety per cent complete at every one of those reports. Last week the deadline was re-based to today, and today the BoQ is still at fifty per cent because the structural drawings still have not arrived. I am no longer asking for a date. I am asking for approval to price the structural element provisionally and close the BoQ without them, because another week of waiting will produce the same slide.');
}

/* ================= SLIDE 8 — BLOCKERS ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'ESCALATION', 'Blockers and Decisions Required',
    'Three items the commercial department cannot clear on its own. The first is the third time of asking.');

  const blockers = [
    [CRIT, 'Structural drawings', 'Priority Insurance · raised 18 Sep',
     'Eight weeks outstanding. The take-off has read 90% at four consecutive reports, and the deadline re-based to today has arrived with the BoQ at 50% and the budget at 10%. Waiting has been tried and has not worked.',
     'Approve pricing the structural element provisionally so the BoQ can close, and set a replacement date today.'],
    [WARN, 'Two items, one project', 'Barry Callebaut Factory Extension',
     'The valuation has sat at 90% for two weeks and the new variation BoQ is at 80%. Both were due today and both sit with Gilbert, who is named on ten of the twenty-three deliverables on the register.',
     'Confirm what is holding the valuation, and whether Gilbert needs the variation BoQ taken off him.'],
    [BLUE, 'Review queue', 'Barry Callebaut Fitout · Ecole',
     'The Fitout BoQ and the Ecole cash flow have both been finished and waiting on a reviewer for a week. They were on last week’s slide for the same reason. Neither can be closed out until signed off.',
     'Nominate a reviewer for each today, rather than carrying them into a third report.']
  ];

  const bw = (CW - 2 * 0.30) / 3, bh = 3.42;
  blockers.forEach((b, i) => {
    const x = M + i * (bw + 0.30);
    card(s, x, y0, bw, bh);
    dot(s, x + 0.54, y0 + 0.50, 0.48, b[0], String(i+1), b[0] === WARN ? NAVY : WHITE);
    s.addText(b[1], T({ x:x+0.94, y:y0+0.22, w:bw-1.18, h:0.56, fontSize:14, bold:true, fontFace:HF, color:NAVY, valign:'middle' }));
    s.addText(b[2], T({ x:x+0.30, y:y0+0.86, w:bw-0.60, h:0.24, fontSize:9.5, bold:true, color:MUTED, valign:'middle' }));
    s.addText(b[3], T({ x:x+0.30, y:y0+1.20, w:bw-0.60, h:1.14, fontSize:10.5, color:INK2, valign:'top' }));
    s.addShape(pres.ShapeType.roundRect, { x:x+0.30, y:y0+2.44, w:bw-0.60, h:0.86, rectRadius:0.08,
      fill:{ color:PANEL }, line:{ type:'none' } });
    s.addText('DECISION REQUIRED', T({ x:x+0.46, y:y0+2.54, w:bw-0.92, h:0.20, fontSize:8, bold:true, color: b[0] === WARN ? '9A6B00' : b[0], charSpacing:1.1, valign:'middle' }));
    s.addText(b[4], T({ x:x+0.46, y:y0+2.76, w:bw-0.92, h:0.50, fontSize:9.5, bold:true, color:NAVY, valign:'top' }));
  });

  card(s, M, y0 + bh + 0.28, CW, 1.00, { fill: NAVY, lineWidth: 0 });
  s.addText('What we need from this meeting', T({ x:M+0.32, y:y0+bh+0.42, w:4.6, h:0.28, fontSize:12, bold:true, color:AMBER, valign:'middle' }));
  s.addText('Approval to close the Priority Insurance BoQ on provisional structural pricing, a view on the Barry Callebaut valuation, and two named reviewers.',
    T({ x:M+0.32, y:y0+bh+0.70, w:CW-0.64, h:0.28, fontSize:11.5, color:WHITE, valign:'middle' }));

  footer(s, 8);
  s.addNotes('Three asks. The first is the third time I have brought it to you and I would rather have a decision to proceed than another date. The second is about load as much as anything, because Gilbert is named on ten of the twenty-three items. The third takes five minutes and closes two deliverables.');
}

/* ================= SLIDE 9 — WORKLOAD ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'RESOURCING', 'Workload Across the Team',
    'Deliverables naming each team member, split between finished and still open.');

  const people = [['Tracy', 2, 0], ['Obed', 1, 1], ['Sedem', 6, 2], ['Eunice', 7, 1], ['Gilbert', 6, 4]];
  s.addChart(pres.ChartType.bar, [
    { name:'Finished',   labels: people.map(p=>p[0]), values: people.map(p=>p[1]) },
    { name:'Still open', labels: people.map(p=>p[0]), values: people.map(p=>p[2]) }
  ], {
    x:M, y:y0, w:7.95, h:4.35, barDir:'bar', barGrouping:'stacked', barGapWidthPct:52,
    chartColors:[GOOD, WARN], showTitle:false,
    showLegend:true, legendPos:'t', legendFontSize:11, legendColor:INK2,
    showValue:true, dataLabelPosition:'ctr', dataLabelFontSize:10, dataLabelColor:NAVY, dataLabelFontBold:true,
    dataLabelFormatCode:'0;;;', dataLabelFontFace:BF,
    valAxisMinVal:0, valAxisMaxVal:11, valAxisMajorUnit:2,
    valAxisLabelFontSize:9, valAxisLabelColor:MUTED,
    catAxisLabelFontSize:11, catAxisLabelColor:INK2,
    valGridLine:{ color:LINE, size:1 }, catGridLine:{ style:'none' },
    valAxisLineColor:LINE, catAxisLineColor:LINE,
    catAxisLabelFontFace:BF, valAxisLabelFontFace:BF, legendFontFace:BF
  });

  const nx = M + 8.25, nw = W - M - nx;
  const notes = [
    ['Gilbert holds four of the six open items', 'He is named on ten of the twenty-three deliverables. Both stuck Barry Callebaut items and both stuck Priority Insurance items are his.'],
    ['Tracy has the shortest list and both are done', 'The Fitout BoQ and the Ecole cash flow, which are the two sitting in the review queue rather than with her.'],
    ['The open work sits on three projects', 'Priority Insurance has three, Barry Callebaut Factory two and RE Villa one. Seven of the ten projects are fully closed out.']
  ];
  const nh = 1.28;
  notes.forEach((n, i) => {
    const y = y0 + i * (nh + 0.18);
    card(s, nx, y, nw, nh, { fill: PANEL, lineWidth: 0, flat: true });
    s.addText(n[0], T({ x:nx+0.24, y:y+0.16, w:nw-0.48, h:0.30, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(n[1], T({ x:nx+0.24, y:y+0.48, w:nw-0.48, h:0.66, fontSize:10, color:INK2, valign:'top' }));
  });

  s.addText([
    { text:'Shared deliverables count once for each named owner, so the totals here (30) exceed the 23 items on the register.', options:{ breakLine:true } },
    { text:'Source: Commercial Department deliverables register, sheet 13-11-2026, read from the issued workbook. Two older sheets in the same file, dated 2 and 9 October, were not used. Dates read as day/month/year. Names reproduced as spelled in the register.', options:{} }
  ], T({ x:M, y:y0+4.42, w:CW, h:0.62, fontSize:8.5, color:MUTED, paraSpaceAfter:3, valign:'top' }));

  footer(s, 9);
  s.addNotes('On resourcing: Gilbert is named on ten of the twenty-three deliverables and holds four of the six still open, including everything that has not moved this week. That is the pattern I would watch. Tracy has only two items and both are finished. Seven of the ten projects are completely closed out, so the open work is concentrated in three.');
}

pres.writeFile({ fileName: 'Commercial_Department_Deliverables_2026-11-13.pptx' })
  .then(f => console.log('WROTE', f));
