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

const REPORT_DATE = '6 November 2026';
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
  chip(s, M, 4.52, 2.25, 0.42, '6 NOVEMBER 2026', AMBER, '1B2A41');

  const stats = [['20','Deliverables tracked'],['11','Active projects'],['80%','Delivered'],['2','Behind plan']];
  const bw = 2.72, gap = 0.30;
  stats.forEach((st, i) => {
    const x = M + i * (bw + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y:5.42, w:bw, h:1.10, rectRadius:0.10,
      fill:{ color:'FFFFFF', transparency:90 }, line:{ color:'FFFFFF', width:0.75, transparency:72 } });
    s.addText(st[0], T({ x:x+0.20, y:5.54, w:bw-0.40, h:0.50, fontSize:27, bold:true, fontFace:HF, color:WHITE, valign:'middle' }));
    s.addText(st[1], T({ x:x+0.20, y:6.03, w:bw-0.40, h:0.30, fontSize:10, color:ICE, valign:'middle' }));
  });
  s.addText('Presented by the Commercial Manager', T({ x:M, y:6.88, w:7.5, h:0.30, fontSize:10.5, color:ICE, valign:'middle' }));
  s.addNotes('Good morning. The register as at 6 November carries twenty deliverables across eleven projects. Sixteen are finished. Only two are behind plan and the gap between them is six tenths of one deliverable, so on the numbers this is a strong week. The one thing I want a decision on is Priority Insurance.');
}

/* ================= SLIDE 2 — EXECUTIVE SUMMARY ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'AT A GLANCE', 'Executive Summary',
    'Position of the commercial deliverables register as at 6 November 2026.');

  const tiles = [
    ['20', 'Deliverables tracked', 'Across 11 active projects', NAVY],
    ['16', 'Delivered', '80% of the register', GOOD],
    ['2',  'Behind plan', 'Together 0.6 of a deliverable', WARN],
    ['7',  'Weeks on one blocker', 'Priority Insurance drawings', CRIT]
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
    [GOOD, 'The September book is closed and most of a new one with it',
     'Only two deliverables carried over from September. Eighteen new items came onto the register since, across six projects that were not on it before, and sixteen of the twenty are already finished.'],
    [WARN, 'Just two deliverables are behind plan, and not by much',
     'The Priority Insurance preliminaries budget sits at 50% against a 100% plan, and the Barry Callebaut Factory valuation at 90%. Together that is six tenths of one deliverable.'],
    [CRIT, 'Priority Insurance has been waiting on structural drawings for seven weeks',
     'The architectural take-off has read 90% complete since 18 September. The BoQ deadline has moved from 30 September to 13 November and the budget behind it stands at 10%.']
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
  s.addNotes('Three points. First, we have turned the register over almost completely since September and still closed eighty per cent of it. Second, the variance is genuinely small, two items and six tenths of a deliverable between them. Third, and this is the one that needs you: Priority Insurance has not been able to move for seven weeks because we are waiting on drawings from outside the department.');
}

/* ================= SLIDE 3 — WHERE THEY STAND ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'PORTFOLIO HEALTH', 'Where the 20 Deliverables Stand');

  s.addChart(pres.ChartType.doughnut,
    [{ name:'Status', labels:['Delivered','On plan, incomplete','Behind plan'], values:[16, 2, 2] }],
    { x:M, y:y0+0.10, w:5.30, h:4.50, holeSize:62, showTitle:false, showLegend:false, showValue:false,
      chartColors:[GOOD, MUTED, WARN], dataBorder:{ pct:2, color:WHITE } });
  s.addText('20', T({ x:2.27, y:3.34, w:2.0, h:0.62, fontSize:40, bold:true, fontFace:HF, color:NAVY, align:'center', valign:'middle' }));
  s.addText('deliverables', T({ x:2.27, y:3.94, w:2.0, h:0.28, fontSize:11, color:MUTED, align:'center', valign:'middle' }));

  const rx = 6.30, rw = W - M - rx;
  const legend = [
    [GOOD,  'Delivered',           'Finished; 2 of these await review',  16, '80%'],
    [MUTED, 'On plan, incomplete', 'Both Priority Insurance, due 13 Nov', 2, '10%'],
    [WARN,  'Behind plan',         'Preliminaries budget and a valuation', 2, '10%']
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
  [['Planned', 0.930, '93.0%', ORANGE], ['Actual', 0.900, '90.0%', BLUE]].forEach((b, i) => {
    const by = py + 0.56 + i * 0.40;
    s.addText(b[0], T({ x:rx+0.22, y:by-0.04, w:1.05, h:0.26, fontSize:10.5, color:INK2, valign:'middle' }));
    progress(s, rx+1.34, by, 3.10, b[1], null, b[3], 0.17);
    s.addText(b[2], T({ x:rx+4.56, y:by-0.05, w:1.60, h:0.28, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
  });
  s.addText('3.0 points behind plan — six tenths of one deliverable',
    T({ x:rx+0.22, y:py+1.32, w:rw-0.44, h:0.26, fontSize:10.5, bold:true, color:GOOD, valign:'middle' }));

  footer(s, 3);
  s.addNotes('Sixteen of twenty finished. Two are incomplete but exactly where the plan says they should be, and both are Priority Insurance items due next Friday. Two are genuinely behind. On progress rather than headcount we are at ninety per cent against a planned ninety-three, so three points, or six tenths of a single deliverable.');
}

/* ================= SLIDE 4 — DELIVERED ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'COMPLETED WORK', '16 Deliverables Finished Across 11 Projects');

  // [project, count, items, owner, awaitingReview]
  const done = [
    ['Vanguard Assurance',     2, ['Valuation', 'Budgetary report'], 'Gilbert', false],
    ['Thoroughbred Place',     2, ['Valuation', 'Budgetary report'], 'Sedem', false],
    ['RE Villa',               2, ['Budgetary Report', 'Valuation'], 'Eunice', false],
    ['Enterprise COO Office',  2, ['Valuation', 'Budgetary Report'], 'Eunice', false],
    ['Priority Insurance',     2, ['Cash Flow', 'Extraction of Labour Rates'], 'Sedem, Gilbert', false],
    ['Tullow Oil',             1, ['Tender'], 'Sedem, Gilbert, Tracy, Eunice', false],
    ['Goldfied',               1, ['Report on Omitted Items'], 'Sedem, Gilbert', false],
    ['Barry Callebaut Factory',1, ['Budgetary report'], 'Gilbert', false],
    ['Barry Callebaut Fitout', 1, ['BoQ'], 'Tracy', true],
    ["Ecole Int'l School",     1, ['Cash Flow'], 'Tracy, Obed, Eunice', true],
    ['Advans Savings & Loans', 1, ['Budgetary Report'], 'Tracy', false]
  ];

  const COLS = 4, GX = 0.24, GY = 0.20, GRID_BOTTOM = 6.40;
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
      T({ x:x+0.30, y:y+0.60, w:cw-0.56, h:0.50, fontSize:8.5, color:INK2, paraSpaceAfter:2, valign:'top' }));
    s.addText(d[3], T({ x:x+0.22, y:y+chh-0.32, w:cw-0.44, h:0.24, fontSize:8.5, bold:true, color:MUTED, valign:'middle' }));
  });

  s.addText('An amber dot marks a deliverable that is finished but still awaiting review: the Barry Callebaut Fitout BoQ and the Ecole cash flow.',
    T({ x:M, y:6.48, w:CW, h:0.26, fontSize:9, color:MUTED, valign:'middle' }));

  footer(s, 4);
  s.addNotes('Sixteen deliverables closed across all eleven projects on the register, so every project has shipped something this period. Vanguard, Thoroughbred, RE Villa, Enterprise and Priority each carried two. Two of the sixteen are finished but still waiting on a reviewer, and those are marked with the amber dot.');
}

/* ================= SLIDE 5 — STILL OPEN ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'THE WATCH LIST', '4 Deliverables Still Open',
    'Ordered by exposure. The dark marker shows where each was planned to be today.');

  const out = [
    ['Priority Insurance', 'Budget for preliminaries and general items', 0.50, 1.00, '13 Nov 2026', 'Obed',           WARN,  'BEHIND'],
    ['Barry Callebaut Factory Extension', 'Valuation',                   0.90, 1.00, '06 Nov 2026', 'Gilbert',        SERIOUS,'DUE TODAY'],
    ['Priority Insurance', 'Complete BoQ',                               0.50, 0.50, '13 Nov 2026', 'Sedem, Gilbert', MUTED, 'ON PLAN'],
    ['Priority Insurance', 'Complete Budget',                            0.10, 0.10, '13 Nov 2026', 'Sedem, Gilbert', MUTED, 'ON PLAN']
  ];

  const rh = 1.02, rg = (CONTENT_BOTTOM - y0 - out.length * rh) / (out.length - 1), o0 = (rh - 0.54) / 2 - 0.12;
  out.forEach((o, i) => {
    const y = y0 + i * (rh + rg) + o0;
    card(s, M, y - o0, CW, rh);
    dot(s, M + 0.30, y - o0 + rh/2, 0.24, o[6]);
    s.addText(o[0], T({ x:M+0.58, y:y+0.13, w:2.80, h:0.26, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(o[1], T({ x:M+0.58, y:y+0.40, w:2.95, h:0.26, fontSize:9.5, color:INK2, valign:'middle' }));

    const bx = M + 3.62, bw = 2.60;
    s.addText(`Actual ${Math.round(o[2]*100)}%`,  T({ x:bx, y:y+0.12, w:1.20, h:0.24, fontSize:9.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(`Planned ${Math.round(o[3]*100)}%`, T({ x:bx+bw-1.40, y:y+0.12, w:1.40, h:0.24, fontSize:9.5, color:MUTED, align:'right', valign:'middle' }));
    progress(s, bx, y + 0.45, bw, o[2], o[3], o[6], 0.17);

    s.addText('DUE',   T({ x:M+6.75, y:y+0.15, w:1.45, h:0.22, fontSize:8, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(o[4],    T({ x:M+6.75, y:y+0.38, w:1.45, h:0.28, fontSize:11, bold:true, color:NAVY, valign:'middle' }));
    s.addText('OWNER', T({ x:M+8.42, y:y+0.15, w:1.85, h:0.22, fontSize:8, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(o[5],    T({ x:M+8.42, y:y+0.38, w:1.85, h:0.28, fontSize:10, color:INK2, valign:'middle' }));

    chip(s, M + 10.52, y - o0 + (rh - 0.34)/2, 1.28, 0.34, o[7], o[6], (o[6] === WARN || o[6] === SERIOUS) ? '1B2A41' : WHITE);
  });

  footer(s, 5);
  s.addNotes('Four items still open. The preliminaries budget is the one genuinely behind, at half of a hundred per cent plan with a week to run, and it sits with Obed alone. The Barry Callebaut valuation is due today at ninety per cent, so it is ten points from done. The two Priority items read as on plan, but I want to be straight about what that means, and the next slide covers it.');
}

/* ================= SLIDE 6 — PRIORITY INSURANCE ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'DEEP DIVE', 'Priority Insurance: Seven Weeks on One Blocker',
    'Five deliverables. The two that matter are held by information the department does not control.');

  const LW = 6.10;
  const items = [
    ['Complete BoQ',                             0.50, 0.50, '13 Nov', MUTED],
    ['Complete Budget',                          0.10, 0.10, '13 Nov', MUTED],
    ['Budget for preliminaries and general items',0.50, 1.00, '13 Nov', WARN],
    ['Cash Flow',                                1.00, 1.00, '06 Nov', GOOD],
    ['Extraction of Labour Rates',               1.00, 1.00, '06 Nov', GOOD]
  ];
  const rh = 0.84, rg = (CONTENT_BOTTOM - y0 - items.length * rh) / (items.length - 1);
  items.forEach((it, i) => {
    const y = y0 + i * (rh + rg);
    card(s, M, y, LW, rh);
    s.addText(it[0], T({ x:M+0.20, y:y+0.10, w:3.60, h:0.26, fontSize:10.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(`due ${it[3]}`, T({ x:M+3.85, y:y+0.10, w:1.15, h:0.26, fontSize:9, color:MUTED, align:'right', valign:'middle' }));
    progress(s, M+0.20, y + 0.46, 4.25, it[1], it[2], it[4], 0.16);
    s.addText(`${Math.round(it[1]*100)}%`, T({ x:M+4.58, y:y+0.40, w:1.30, h:0.26, fontSize:10.5, bold:true, color:NAVY, valign:'middle' }));
  });

  const rx = M + LW + 0.32, rw = W - M - rx;
  card(s, rx, y0, rw, 2.72);
  s.addText('The same blocker, three reports running', T({ x:rx+0.24, y:y0+0.16, w:rw-0.48, h:0.28, fontSize:12.5, bold:true, color:NAVY, valign:'middle' }));
  const hist = [
    ['18 Sep', CRIT,  'BoQ at 40%, due 30 Sep. Awaiting the floor finishes schedule and the structural drawings.'],
    ['25 Sep', CRIT,  'BoQ still at 40%, due 30 Sep. No movement in seven days.'],
    ['06 Nov', WARN,  'BoQ at 50%, due 13 Nov. The structural drawings are still listed as outstanding.']
  ];
  hist.forEach((h, i) => {
    const hy = y0 + 0.58 + i * 0.68;
    dot(s, rx + 0.40, hy + 0.17, 0.20, h[1]);
    s.addText(h[0], T({ x:rx+0.60, y:hy+0.02, w:0.95, h:0.28, fontSize:11, bold:true, fontFace:HF, color:NAVY, valign:'middle' }));
    s.addText(h[2], T({ x:rx+1.60, y:hy, w:rw-1.84, h:0.56, fontSize:9.5, color:INK2, valign:'top' }));
  });

  card(s, rx, y0 + 2.94, rw, 1.78, { fill: PANEL, lineWidth: 0, flat: true });
  s.addText('The take-off has read 90% since 18 September',
    T({ x:rx+0.24, y:y0+3.10, w:rw-0.48, h:0.28, fontSize:11.5, bold:true, color:CRIT, valign:'middle' }));
  s.addText('In seven weeks the BoQ has gained ten points and its deadline has moved out six, from 30 September to 13 November. It reads as on plan today only because the plan moved with it. The budget behind it is at 10% and shares the same deadline.',
    T({ x:rx+0.24, y:y0+3.42, w:rw-0.48, h:0.74, fontSize:10, color:INK2, valign:'top' }));
  s.addText('Ask: a firm issue date for the structural drawings, or approval to price the structural element provisionally and close the BoQ without them.',
    T({ x:rx+0.24, y:y0+4.18, w:rw-0.48, h:0.46, fontSize:10, bold:true, color:NAVY, valign:'top' }));

  footer(s, 6);
  s.addNotes('I want to be straight about Priority Insurance. Three of its five deliverables are fine. The BoQ shows as on plan today, but that is because the plan has moved, not because the work has. Seven weeks ago the take-off was ninety per cent complete and we were waiting on structural drawings. Today the take-off is still ninety per cent complete and we are still waiting on structural drawings. The deadline has moved out six weeks in that time. So I need either a date for those drawings, or your agreement that we price the structural element provisionally and close the BoQ without them.');
}

/* ================= SLIDE 7 — BLOCKERS ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'ESCALATION', 'Blockers and Decisions Required',
    'Three items the commercial department cannot clear on its own.');

  const blockers = [
    [CRIT, 'Structural drawings', 'Priority Insurance',
     'Outstanding since 18 September. The architectural take-off has been stuck at 90% for seven weeks, the BoQ deadline has moved out six, and the budget behind it cannot progress past 10%.',
     'Give us a firm issue date, or approve pricing the structural element provisionally so the BoQ can close.'],
    [WARN, 'Preliminaries budget', 'Priority Insurance',
     'At 50% against a 100% plan with a week to the 13 November deadline. It is the only deliverable on the register held by a single person with nothing else finished behind them.',
     'Confirm Obed has what he needs, or put a second pair of hands on it this week.'],
    [BLUE, 'Two items awaiting review', 'Barry Callebaut Fitout · Ecole',
     'The Fitout BoQ and the Ecole cash flow are both finished and both waiting on a reviewer. The queue is far shorter than it was in September, which is why clearing it now is cheap.',
     'Nominate a reviewer for each and set a clearance date before the next report.']
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
  s.addText('A date for the Priority Insurance structural drawings or approval to proceed without them, support for the preliminaries budget, and two named reviewers.',
    T({ x:M+0.32, y:y0+bh+0.70, w:CW-0.64, h:0.28, fontSize:11.5, color:WHITE, valign:'middle' }));

  footer(s, 7);
  s.addNotes('Three asks, in order of cost. The drawings are the expensive one and I would rather have a decision to proceed without them than another week of waiting. The preliminaries budget just needs a second person on it. And two reviewers, which is a five minute decision that closes two deliverables.');
}

/* ================= SLIDE 8 — WORKLOAD ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'RESOURCING', 'Workload Across the Team',
    'Deliverables naming each team member, split between finished and still open.');

  const people = [['Obed', 1, 1], ['Tracy', 4, 0], ['Eunice', 6, 0], ['Sedem', 5, 2], ['Gilbert', 7, 3]];
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
    ['Gilbert is named on half the register', 'Ten of the twenty deliverables, across six projects. He has finished seven and holds three of the four open items.'],
    ['Tracy and Eunice are fully closed out', 'Ten deliverables between them this period, all finished, nothing carried forward.'],
    ['Every open item is one of two projects', 'Three sit on Priority Insurance and one on the Barry Callebaut Factory valuation. No other project has work outstanding.']
  ];
  const nh = 1.28;
  notes.forEach((n, i) => {
    const y = y0 + i * (nh + 0.18);
    card(s, nx, y, nw, nh, { fill: PANEL, lineWidth: 0, flat: true });
    s.addText(n[0], T({ x:nx+0.24, y:y+0.16, w:nw-0.48, h:0.30, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(n[1], T({ x:nx+0.24, y:y+0.48, w:nw-0.48, h:0.66, fontSize:10, color:INK2, valign:'top' }));
  });

  s.addText([
    { text:'Shared deliverables count once for each named owner, so the totals here (29) exceed the 20 items on the register.', options:{ breakLine:true } },
    { text:'Source: Commercial Department deliverables register, 6 November 2026, read from the issued PDF. Dates read as day/month/year. Project and client names are reproduced as spelled in the register.', options:{} }
  ], T({ x:M, y:y0+4.42, w:CW, h:0.62, fontSize:8.5, color:MUTED, paraSpaceAfter:3, valign:'top' }));

  footer(s, 8);
  s.addNotes('On resourcing: Gilbert is named on ten of the twenty deliverables and holds three of the four still open, so he is the constraint if anything else arrives. Tracy and Eunice are completely clear. Obed has one open item, the preliminaries budget, which is the one I asked for support on. Every open item belongs to Priority Insurance or the Barry Callebaut valuation.');
}

pres.writeFile({ fileName: 'Commercial_Department_Deliverables_2026-11-06.pptx' })
  .then(f => console.log('WROTE', f));
