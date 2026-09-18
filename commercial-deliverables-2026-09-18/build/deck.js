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

// The Commercial Manager removed the closing 'Next Steps' slide from the reviewed copy.
// Set this to true to bring it back (its content is refreshed for the new figures).
const INCLUDE_NEXT_STEPS = false;

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'Commercial Department';
pres.title  = 'Commercial Department — Outstanding Projects & Deliverables';

/* ---------------- helpers ---------------- */
function footer(s, n){
  s.addText('Commercial Department   ·   Outstanding Projects & Deliverables   ·   18 September 2026',
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
  // motif: soft translucent discs
  s.addShape(pres.ShapeType.ellipse, { x:10.35, y:-1.45, w:4.6, h:4.6, fill:{color:'FFFFFF', transparency:94}, line:{type:'none'} });
  s.addShape(pres.ShapeType.ellipse, { x:11.55, y:0.55,  w:2.5, h:2.5, fill:{color:AMBER,   transparency:86}, line:{type:'none'} });
  s.addShape(pres.ShapeType.ellipse, { x:-1.60, y:6.05,  w:3.3, h:3.3, fill:{color:'FFFFFF', transparency:96}, line:{type:'none'} });

  s.addText('COMMERCIAL DEPARTMENT   ·   PRE & POST CONTRACT',
    T({ x:M, y:1.52, w:10.5, h:0.3, fontSize:12, bold:true, color:AMBER, charSpacing:2.2, valign:'middle' }));
  s.addText('Outstanding Projects\n& Deliverables',
    T({ x:M, y:1.95, w:9.4, h:1.85, fontSize:46, bold:true, fontFace:HF, color:WHITE, lineSpacingMultiple:1.02, valign:'top' }));
  s.addText('Status report to Management',
    T({ x:M, y:3.92, w:9.4, h:0.38, fontSize:19, color:ICE, valign:'middle' }));

  // date pill
  chip(s, M, 4.52, 2.25, 0.42, '18 SEPTEMBER 2026', AMBER, '1B2A41');

  // headline mini-stats
  const stats = [['22','Deliverables tracked'],['13','Active projects'],['82%','Delivered to date'],['4','Still outstanding']];
  const bw = 2.72, gap = 0.30;
  stats.forEach((st, i) => {
    const x = M + i * (bw + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y:5.42, w:bw, h:1.10, rectRadius:0.10,
      fill:{ color:'FFFFFF', transparency:90 }, line:{ color:'FFFFFF', width:0.75, transparency:72 } });
    s.addText(st[0], T({ x:x+0.20, y:5.54, w:bw-0.40, h:0.50, fontSize:27, bold:true, fontFace:HF, color:WHITE, valign:'middle' }));
    s.addText(st[1], T({ x:x+0.20, y:6.03, w:bw-0.40, h:0.30, fontSize:10, color:ICE, valign:'middle' }));
  });

  s.addText('Presented by the Commercial Manager', T({ x:M, y:6.88, w:7.5, h:0.30, fontSize:10.5, color:ICE, valign:'middle' }));
  s.addNotes('Good morning. This is the commercial department status report as at 18 September 2026, covering pre and post contract deliverables across 13 active projects. Twenty-two deliverables are being tracked. Eighteen are complete. Four remain outstanding, and three items on this register need a decision from this meeting.');
}

/* ================= SLIDE 2 — EXECUTIVE SUMMARY ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'AT A GLANCE', 'Executive Summary',
    'Position of the commercial deliverables register as at 18 September 2026.');

  const tiles = [
    ['22', 'Deliverables tracked', 'Across 13 active projects', NAVY],
    ['18', 'Delivered', '82% of the register', GOOD],
    ['4',  'Outstanding', '3 in progress, 1 not started', WARN],
    ['3',  'Need a decision today', 'Blocked or at risk of slipping', CRIT]
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
    [BLUE, 'The register is 86% complete against a 93% plan',
     'A shortfall of 6.8 percentage points, equal to one and a half deliverables. All of it sits in three items: Kinbu, Stanbic and the Priority Insurance BoQ.'],
    [CRIT, 'Two tender submissions fall due on 24 September',
     'The Kinbu School Canteen priced BoQ stands at 10% against a 100% plan, and the Stanbic Bank preliminary estimate at 50%. Both are held by the wider team rather than a named owner.'],
    [WARN, 'Priority Insurance is held up by missing design information',
     'The architectural take-off is 90% done, but the floor finishes schedule and structural drawings are still outstanding. The budget that follows it cannot start.']
  ];
  const ry = y0 + th + 0.26, rh = 0.94, rg = 0.12;
  rows.forEach((r, i) => {
    const y = ry + i * (rh + rg);
    card(s, M, y, CW, rh);
    dot(s, M + 0.52, y + rh/2, 0.46, r[0], String(i+1));
    s.addText(r[1], T({ x:M+0.98, y:y+0.13, w:CW-1.30, h:0.28, fontSize:13, bold:true, color:NAVY, valign:'middle' }));
    s.addText(r[2], T({ x:M+0.98, y:y+0.43, w:CW-1.30, h:0.36, fontSize:10.5, color:INK2, valign:'top' }));
  });

  footer(s, 2);
  s.addNotes('Three things to take away. First, we are 86% complete against a 93% plan — a gap of just under seven points, and it is concentrated, not spread. Ecole closed out since the last review. Second, two tenders close on 24 September and one of them, Kinbu, is only 10% priced. Third, Priority Insurance is blocked on information we do not control.');
}

/* ================= SLIDE 3 — DELIVERY STATUS ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'PORTFOLIO HEALTH', 'Where the 22 Deliverables Stand');

  s.addChart(pres.ChartType.doughnut,
    [{ name:'Delivery status', labels:['Delivered','In progress','Not started'], values:[18, 3, 1] }],
    { x:M, y:y0+0.10, w:5.30, h:4.50, holeSize:62, showTitle:false, showLegend:false, showValue:false,
      chartColors:[GOOD, WARN, MUTED], dataBorder:{ pct:2, color:WHITE } });

  // hole label
  s.addText('22', T({ x:2.27, y:3.34, w:2.0, h:0.62, fontSize:40, bold:true, fontFace:HF, color:NAVY, align:'center', valign:'middle' }));
  s.addText('deliverables', T({ x:2.27, y:3.94, w:2.0, h:0.28, fontSize:11, color:MUTED, align:'center', valign:'middle' }));

  const rx = 6.30, rw = W - M - rx;   // 6.413
  const legend = [
    [GOOD,  'Delivered',   'Signed off and issued',            18, '82%'],
    [WARN,  'In progress', 'Started but short of the plan',      3, '14%'],
    [MUTED, 'Not started', 'Zero progress, still within plan',   1,  '5%']
  ];
  const lh = 0.80, lg = 0.13;
  legend.forEach((l, i) => {
    const y = y0 + 0.16 + i * (lh + lg);
    card(s, rx, y, rw, lh, { fill: PANEL, lineWidth: 0, flat: true });
    dot(s, rx + 0.36, y + lh/2, 0.26, l[0]);
    s.addText(l[1], T({ x:rx+0.68, y:y+0.13, w:2.70, h:0.28, fontSize:13, bold:true, color:NAVY, valign:'middle' }));
    s.addText(l[2], T({ x:rx+0.68, y:y+0.41, w:3.10, h:0.26, fontSize:9.5, color:MUTED, valign:'middle' }));
    s.addText(String(l[3]), T({ x:rx+3.95, y:y+0.17, w:1.05, h:0.46, fontSize:24, bold:true, fontFace:HF, color:NAVY, align:'right', valign:'middle' }));
    s.addText(l[4], T({ x:rx+5.06, y:y+0.26, w:1.05, h:0.30, fontSize:12, color:INK2, align:'right', valign:'middle' }));
  });

  // progress against plan
  const py = y0 + 0.16 + 3 * (lh + lg) + 0.22;
  card(s, rx, py, rw, 1.66);
  s.addText('Progress against plan', T({ x:rx+0.22, y:py+0.16, w:rw-0.44, h:0.28, fontSize:12.5, bold:true, color:NAVY, valign:'middle' }));
  const bars = [['Planned', 0.932, '93.2%', ORANGE], ['Actual', 0.864, '86.4%', BLUE]];
  bars.forEach((b, i) => {
    const by = py + 0.56 + i * 0.40;
    s.addText(b[0], T({ x:rx+0.22, y:by-0.04, w:1.05, h:0.26, fontSize:10.5, color:INK2, valign:'middle' }));
    progress(s, rx+1.34, by, 3.10, b[1], null, b[3], 0.17);
    s.addText(b[2], T({ x:rx+4.56, y:by-0.05, w:1.60, h:0.28, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
  });
  s.addText('6.8 points behind plan — a shortfall of 1.5 deliverables',
    T({ x:rx+0.22, y:py+1.32, w:rw-0.44, h:0.26, fontSize:10.5, bold:true, color:CRIT, valign:'middle' }));

  footer(s, 3);
  s.addNotes('Eighteen of twenty-two deliverables are complete — over four fifths of the register. Three are in progress and one has not started, though that one is still inside its plan. Measured on progress rather than headcount, we are at 86.4% against a planned 93.2% — a gap of one and a half deliverables.');
}

/* ================= SLIDE 4 — BY PROJECT ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'DELIVERY PERFORMANCE', 'Where the Portfolio Is Behind',
    'The three projects still carrying variance. Planned versus actual completion, averaged across each project\u2019s deliverables.');

  // ordered worst-variance first; data[0] plots at the BOTTOM of a horizontal bar chart
  const proj = [
    ['Priority Insurance',     25,  20],
    ['Stanbic Bank',          100,  50],
    ['Kinbu Canteen Tender',  100,  10]
  ];

  const cw2 = 8.35;
  s.addChart(pres.ChartType.bar, [
    { name:'Planned', labels: proj.map(p=>p[0]), values: proj.map(p=>p[1]) },
    { name:'Actual',  labels: proj.map(p=>p[0]), values: proj.map(p=>p[2]) }
  ], {
    x:M, y:y0, w:cw2, h:4.30, barDir:'bar', barGrouping:'clustered', barGapWidthPct:38,
    chartColors:[ORANGE, BLUE], showTitle:false,
    showLegend:true, legendPos:'t', legendFontSize:11, legendColor:INK2,
    showValue:true, dataLabelPosition:'outEnd', dataLabelFontSize:10, dataLabelColor:INK2,
    dataLabelFormatCode:'0"%"',
    valAxisMinVal:0, valAxisMaxVal:112, valAxisMajorUnit:25,
    valAxisLabelFontSize:9.5, valAxisLabelColor:MUTED, valAxisLabelFormatCode:'0"%"',
    catAxisLabelFontSize:11, catAxisLabelColor:INK2,
    valGridLine:{ color:LINE, size:1 }, catGridLine:{ style:'none' },
    valAxisLineColor:LINE, catAxisLineColor:LINE,
    catAxisLabelFontFace:BF, valAxisLabelFontFace:BF, dataLabelFontFace:BF, legendFontFace:BF
  });

  s.addText('Priority Insurance shows a small gap because only part of its work was scheduled to be complete by today.',
    T({ x:M, y:y0+4.38, w:cw2, h:0.30, fontSize:10, color:MUTED, valign:'middle' }));

  const rx = M + cw2 + 0.32, rw = W - M - rx;
  const panels = [
    [GOOD, '10', 'projects fully delivered', 'Eighteen deliverables closed, every one of them at 100% of plan. The detail follows on the next slide.'],
    [CRIT, '3',  'projects behind plan',     'Between them they account for the whole shortfall of one and a half deliverables against the September plan.']
  ];
  panels.forEach((p, i) => {
    const y = y0 + i * 2.28;
    card(s, rx, y, rw, 2.08, { fill: PANEL, lineWidth: 0, flat: true });
    dot(s, rx + rw - 0.38, y + 0.36, 0.20, p[0]);
    s.addText(p[1], T({ x:rx+0.26, y:y+0.18, w:rw-0.80, h:0.72, fontSize:46, bold:true, fontFace:HF, color:NAVY, valign:'middle' }));
    s.addText(p[2], T({ x:rx+0.26, y:y+0.92, w:rw-0.52, h:0.30, fontSize:13, bold:true, color:INK, valign:'middle' }));
    s.addText(p[3], T({ x:rx+0.26, y:y+1.26, w:rw-0.52, h:0.68, fontSize:10, color:INK2, valign:'top' }));
  });

  footer(s, 4);
  s.addNotes('This is where the variance actually sits, and it is now three projects rather than four. Kinbu is the outlier at 10% against a 100% plan. Stanbic is at half of what was planned. Priority Insurance looks small at 20 against 25, and it is small, because only half of its BoQ was ever scheduled to be done by today. Every other project in the portfolio, ten of them, is complete.');
}

/* ================= SLIDE 5 — DELIVERED ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'COMPLETED WORK', '18 Deliverables Signed Off Across 10 Projects');

  const done = [
    ['Anglogold Ashanti', 3, ['Budget', 'Revised BoQ', 'Valuation report'], 'Gilbert, Sedem'],
    ['Warehouse', 3, ['Cost analysis — electrical works', 'Cashflow forecast', 'Roller shutter subcontractor'], 'Eunice'],
    ['RE Villa', 3, ['Budgetary report', 'Remeasurement of hardcore filling', 'Cashflow forecast'], 'Eunice'],
    ['Vanguard Assurance Spintex', 2, ['Monthly valuation', 'Budgetary report'], 'Gilbert'],
    ['Advans Savings & Loans', 2, ['Final account', 'Budgetary report'], 'Tracy'],
    ['Ecole International School', 1, ['BoQ and Budget'], 'Tracy, Obed, Eunice'],
    ['Thoroughbred Place', 1, ['Financial report (internal)'], 'Sedem'],
    ['Barry Callebaut', 1, ['Budgetary report'], 'Gilbert'],
    ['Brimmo Gardens Tender', 1, ['RFP submission'], 'Eunice'],
    ["Enterprise COO's Office", 1, ['Cashflow forecast'], 'Eunice']
  ];

  const COLS = 4, GX = 0.24, GY = 0.20;
  const cw = (CW - (COLS - 1) * GX) / COLS;
  const chh = (CONTENT_BOTTOM - y0 - 2 * GY) / 3;
  done.forEach((d, i) => {
    const x = M + (i % COLS) * (cw + GX);
    const y = y0 + Math.floor(i / COLS) * (chh + GY);
    card(s, x, y, cw, chh);
    dot(s, x + cw - 0.36, y + 0.34, 0.40, GOOD, String(d[1]));
    s.addText(d[0], T({ x:x+0.22, y:y+0.15, w:cw-0.76, h:0.46, fontSize:11.5, bold:true, fontFace:HF, color:NAVY, valign:'top' }));
    s.addText(d[2].map((t, j) => ({ text:t, options:{ bullet:{ indent:13 }, breakLine: j < d[2].length - 1 } })),
      T({ x:x+0.30, y:y+0.64, w:cw-0.56, h:chh-1.06, fontSize:8.5, color:INK2, paraSpaceAfter:2, valign:'top' }));
    s.addText(d[3], T({ x:x+0.22, y:y+chh-0.34, w:cw-0.44, h:0.26, fontSize:8.5, bold:true, color:MUTED, valign:'middle' }));
  });

  footer(s, 5);
  s.addNotes('This is the delivered column, and Ecole has now joined it. Ten projects are fully closed out for the period — eighteen deliverables in total. Anglogold, the Warehouse and RE Villa each carried three. Worth noting that the Anglogold budget is finished but is sitting with a reviewer; I will come back to that on the blockers slide.');
}

/* ================= SLIDE 6 — OUTSTANDING ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'THE WATCH LIST', '4 Outstanding Deliverables',
    'Ordered by exposure. The dark marker on each bar shows where the deliverable was planned to be today.');

  const out = [
    ['Kinbu School Canteen Tender', 'Priced BoQ',           0.10, 1.00, '24 Sep 2026', 'Team',                 CRIT, 'CRITICAL'],
    ['Stanbic Bank',                'Preliminary Estimate', 0.50, 1.00, '24 Sep 2026', 'Team',              SERIOUS, 'AT RISK'],
    ['Priority Insurance',          'Complete BoQ',         0.40, 0.50, '30 Sep 2026', 'Obed, Sedem, Gilbert', WARN, 'BLOCKED'],
    ['Priority Insurance',          'Complete Budget',      0.00, 0.00, '09 Oct 2026', 'Obed, Sedem, Gilbert', MUTED,'ON PLAN']
  ];

  const rh = 1.02, rg = (CONTENT_BOTTOM - y0 - out.length * rh) / (out.length - 1), o0 = (rh - 0.54) / 2 - 0.12;
  out.forEach((o, i) => {
    const y = y0 + i * (rh + rg) + o0;
    card(s, M, y - o0, CW, rh);
    dot(s, M + 0.30, y - o0 + rh/2, 0.24, o[6]);
    s.addText(o[0], T({ x:M+0.58, y:y+0.13, w:2.80, h:0.26, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(o[1], T({ x:M+0.58, y:y+0.40, w:2.80, h:0.26, fontSize:10,   color:INK2, valign:'middle' }));

    const bx = M + 3.62, bw = 2.60;
    s.addText(`Actual ${Math.round(o[2]*100)}%`, T({ x:bx, y:y+0.12, w:1.20, h:0.24, fontSize:9.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(`Planned ${Math.round(o[3]*100)}%`, T({ x:bx+bw-1.40, y:y+0.12, w:1.40, h:0.24, fontSize:9.5, color:MUTED, align:'right', valign:'middle' }));
    progress(s, bx, y + 0.45, bw, o[2], o[3], o[6] === MUTED ? MUTED : o[6], 0.17);

    s.addText('DUE',   T({ x:M+6.75, y:y+0.15, w:1.45, h:0.22, fontSize:8, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(o[4],    T({ x:M+6.75, y:y+0.38, w:1.45, h:0.28, fontSize:11, bold:true, color:NAVY, valign:'middle' }));
    s.addText('OWNER', T({ x:M+8.42, y:y+0.15, w:1.85, h:0.22, fontSize:8, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(o[5],    T({ x:M+8.42, y:y+0.38, w:1.85, h:0.28, fontSize:10, color:INK2, valign:'middle' }));

    chip(s, M + 10.52, y - o0 + (rh - 0.34)/2, 1.28, 0.34, o[7], o[6], (o[6] === WARN || o[6] === SERIOUS) ? '1B2A41' : WHITE);
  });

  footer(s, 6);
  s.addNotes('Four items now that Ecole has closed. Kinbu is the one that should worry us — 10% priced with six days to submission. Stanbic is at half. The Priority Insurance BoQ is only ten points behind plan, but it is blocked rather than late. The Priority budget has not started and does not need to have — it follows the BoQ.');
}

/* ================= SLIDE 7 — DEADLINE RUNWAY ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'WHAT FALLS DUE NEXT', 'The Next Three Weeks',
    'With Ecole closed, the remaining work falls due between 24 September and 9 October.');

  const x0 = 1.95, x1 = 11.30, span = x1 - x0, lineY = 3.86;
  const ms = [
    { d:0,  date:'18 Sep',  when:'Today',     color:MUTED, items:[] },
    { d:6,  date:'24 Sep',  when:'In 6 days', color:CRIT,  items:[['Kinbu Canteen Tender','Priced BoQ','10% complete'], ['Stanbic Bank','Preliminary Estimate','50% complete']] },
    { d:12, date:'30 Sep',  when:'In 12 days',color:WARN,  items:[['Priority Insurance','Complete BoQ','40% complete']] },
    { d:21, date:'09 Oct',  when:'In 21 days',color:MUTED, items:[['Priority Insurance','Complete Budget','Not started']] }
  ];

  // the runway
  const BASE = 3.54;                       // every card sits on this baseline
  s.addShape(pres.ShapeType.rect, { x:x0-0.40, y:lineY-0.02, w:span+0.80, h:0.04, fill:{color:LINE}, line:{type:'none'} });

  ms.forEach(m => {
    const px = x0 + (m.d / 21) * span;
    const cw = 2.32, cx = px - cw/2;
    const chh = 0.34 + m.items.length * 0.66;
    const cy = BASE - chh;
    if (m.items.length) card(s, cx, cy, cw, chh);
    m.items.forEach((it, j) => {
      const iy = cy + 0.16 + j * 0.66;
      s.addText(it[0], T({ x:cx+0.20, y:iy,      w:cw-0.40, h:0.24, fontSize:10.5, bold:true, color:NAVY, valign:'middle' }));
      s.addText(it[1], T({ x:cx+0.20, y:iy+0.23, w:cw-0.40, h:0.22, fontSize:9.5,  color:INK2, valign:'middle' }));
      s.addText(it[2], T({ x:cx+0.20, y:iy+0.44, w:cw-0.40, h:0.20, fontSize:8.5, bold:true, color:m.color, valign:'middle' }));
    });
    if (m.items.length) s.addShape(pres.ShapeType.rect, { x:px-0.015, y:BASE, w:0.03, h:lineY-0.15-BASE, fill:{color:LINE}, line:{type:'none'} });
    const md = m.items.length ? 0.30 : 0.20;
    s.addShape(pres.ShapeType.ellipse, { x:px-md/2, y:lineY-md/2, w:md, h:md, fill:{color:m.color}, line:{color:WHITE, width:2.5} });
    s.addText(m.date, T({ x:px-1.20, y:lineY+0.26, w:2.40, h:0.32, fontSize:15, bold:true, fontFace:HF, color: m.items.length ? NAVY : MUTED, align:'center', valign:'middle' }));
    s.addText(m.when, T({ x:px-1.20, y:lineY+0.58, w:2.40, h:0.26, fontSize:10, color:MUTED, align:'center', valign:'middle' }));
  });

  card(s, M, 5.08, CW, 1.18, { fill: PANEL, lineWidth: 0, flat: true });
  s.addText('Pinch point', T({ x:M+0.30, y:5.24, w:2.0, h:0.26, fontSize:11, bold:true, color:CRIT, valign:'middle' }));
  s.addText('Two tender submissions close on the same day, 24 September, and both sit with the team rather than a named owner. Between them they account for 1.4 of the 1.5 deliverables we are behind. Naming an owner for each is the single highest-value action available this week.',
    T({ x:M+0.30, y:5.52, w:CW-0.60, h:0.60, fontSize:10.5, color:INK2, valign:'top' }));

  footer(s, 7);
  s.addNotes('Laid out on a calendar, the exposure is obvious. Nothing falls due today now that Ecole has closed. Six days from now two tenders close on the same day. The Priority BoQ follows on the thirtieth and its budget on the ninth of October. The twenty-fourth is the pinch point, and neither of those two tenders has a named owner.');
}

/* ================= SLIDE 8 — BLOCKERS ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'ESCALATION', 'Blockers and Decisions Required',
    'Three items cannot be cleared by the commercial department alone.');

  const blockers = [
    [CRIT, 'Tender capacity', 'Kinbu School Canteen · Stanbic Bank',
     'Both submissions close on 24 September. The Kinbu priced BoQ is at 10% and the Stanbic estimate at 50%. Neither has a named owner — both are logged against "Team".',
     'Assign a named lead to each tender today, or authorise a request for an extension on Kinbu.'],
    [WARN, 'Missing design information', 'Priority Insurance',
     'The architectural take-off is 90% done. The floor finishes schedule and the structural drawings have not been received, so the BoQ cannot be closed and the budget behind it cannot start.',
     'Escalate to the design team and the client for a firm issue date for both documents.'],
    [BLUE, 'Review bottleneck', 'Anglogold Ashanti',
     'The budget is complete and has been sitting in "awaiting review" since 11 September. It is the only finished deliverable not yet signed off.',
     'Nominate the reviewer and set a clearance date so the deliverable can be closed.']
  ];

  const bw = (CW - 2 * 0.30) / 3, bh = 3.38;
  blockers.forEach((b, i) => {
    const x = M + i * (bw + 0.30);
    card(s, x, y0, bw, bh);
    dot(s, x + 0.54, y0 + 0.50, 0.48, b[0], String(i+1));
    // title gets two full lines; the project sits on its own line beneath
    s.addText(b[1], T({ x:x+0.92, y:y0+0.22, w:bw-1.16, h:0.56, fontSize:13.5, bold:true, fontFace:HF, color:NAVY, valign:'middle' }));
    s.addText(b[2], T({ x:x+0.30, y:y0+0.84, w:bw-0.60, h:0.24, fontSize:9.5, bold:true, color:MUTED, valign:'middle' }));
    s.addText(b[3], T({ x:x+0.30, y:y0+1.18, w:bw-0.60, h:1.10, fontSize:10.5, color:INK2, valign:'top' }));
    s.addShape(pres.ShapeType.roundRect, { x:x+0.30, y:y0+2.40, w:bw-0.60, h:0.80, rectRadius:0.08,
      fill:{ color:PANEL }, line:{ type:'none' } });
    s.addText('DECISION REQUIRED', T({ x:x+0.46, y:y0+2.50, w:bw-0.92, h:0.20, fontSize:8, bold:true, color:b[0], charSpacing:1.1, valign:'middle' }));
    s.addText(b[4], T({ x:x+0.46, y:y0+2.70, w:bw-0.92, h:0.46, fontSize:9.5, bold:true, color:NAVY, valign:'top' }));
  });

  card(s, M, y0 + bh + 0.28, CW, 1.00, { fill: NAVY, lineWidth: 0 });
  s.addText('What we need from this meeting', T({ x:M+0.32, y:y0+bh+0.42, w:4.6, h:0.28, fontSize:12, bold:true, color:AMBER, valign:'middle' }));
  s.addText('Two named tender leads, a firm issue date for the Priority Insurance drawings, and a nominated reviewer for the Anglogold budget.',
    T({ x:M+0.32, y:y0+bh+0.70, w:CW-0.64, h:0.28, fontSize:11.5, color:WHITE, valign:'middle' }));

  footer(s, 8);
  s.addNotes('These are the three asks. One: name a lead for each of the two tenders, or let us request an extension on Kinbu. Two: help us get a firm date for the Priority Insurance floor finishes schedule and structural drawings. Three: tell us who reviews the Anglogold budget and by when. All three are decisions, not work.');
}

/* ================= SLIDE 9 — WORKLOAD ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'RESOURCING', 'Workload Across the Team',
    'Deliverables held by each team member, split between delivered and outstanding.');

  const people = [['Team', 0, 2], ['Obed', 1, 2], ['Tracy', 3, 0], ['Sedem', 3, 2], ['Gilbert', 4, 2], ['Eunice', 9, 0]];
  s.addChart(pres.ChartType.bar, [
    { name:'Delivered',   labels: people.map(p=>p[0]), values: people.map(p=>p[1]) },
    { name:'Outstanding', labels: people.map(p=>p[0]), values: people.map(p=>p[2]) }
  ], {
    x:M, y:y0, w:7.95, h:4.35, barDir:'bar', barGrouping:'stacked', barGapWidthPct:52,
    chartColors:[GOOD, WARN], showTitle:false,
    showLegend:true, legendPos:'t', legendFontSize:11, legendColor:INK2,
    showValue:true, dataLabelPosition:'ctr', dataLabelFontSize:10, dataLabelColor:NAVY, dataLabelFontBold:true,
    dataLabelFormatCode:'0;;;', dataLabelFontFace:BF,
    valAxisMinVal:0, valAxisMaxVal:10, valAxisMajorUnit:2,
    valAxisLabelFontSize:9, valAxisLabelColor:MUTED,
    catAxisLabelFontSize:11, catAxisLabelColor:INK2,
    valGridLine:{ color:LINE, size:1 }, catGridLine:{ style:'none' },
    valAxisLineColor:LINE, catAxisLineColor:LINE,
    catAxisLabelFontFace:BF, valAxisLabelFontFace:BF, legendFontFace:BF
  });

  const nx = M + 8.25, nw = W - M - nx;
  const notes = [
    ['Eunice has closed every item', 'Nine deliverables, all of them delivered. The highest throughput in the department by some margin.'],
    ['Obed\u2019s open work is one project', 'Both of his remaining items sit on Priority Insurance, which is blocked on design information rather than running late.'],
    ['Two items have no named owner', 'Both Kinbu and Stanbic are logged against "Team". These are the two tenders closing on 24 September.']
  ];
  const nh = 1.28;
  notes.forEach((n, i) => {
    const y = y0 + i * (nh + 0.18);
    card(s, nx, y, nw, nh, { fill: PANEL, lineWidth: 0, flat: true });
    s.addText(n[0], T({ x:nx+0.24, y:y+0.16, w:nw-0.48, h:0.30, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(n[1], T({ x:nx+0.24, y:y+0.48, w:nw-0.48, h:0.66, fontSize:10, color:INK2, valign:'top' }));
  });

  s.addText('Shared deliverables count once for each named owner, so the totals here (28) exceed the 22 items on the register. "Team" means no individual was named.',
    T({ x:M, y:y0+4.45, w:CW, h:0.34, fontSize:9.5, color:MUTED, valign:'top' }));

  footer(s, 9);
  s.addNotes('On resourcing: Eunice is carrying nine deliverables and has now closed all nine. Gilbert six, Sedem five. Tracy is also fully closed out. Obed has two items left, both on Priority Insurance, so that is a blockage rather than a performance question. The two unowned items are the same two tenders we keep coming back to.');
}

if (INCLUDE_NEXT_STEPS)
/* ================= SLIDE 10 — NEXT STEPS ================= */
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.ShapeType.ellipse, { x:11.60, y:-2.05, w:3.6, h:3.6, fill:{color:'FFFFFF', transparency:96}, line:{type:'none'} });
  s.addShape(pres.ShapeType.ellipse, { x:-1.70, y:6.15, w:3.0, h:3.0, fill:{color:AMBER, transparency:92}, line:{type:'none'} });

  s.addText('NEXT STEPS', T({ x:M, y:0.62, w:CW, h:0.26, fontSize:10.5, bold:true, color:AMBER, charSpacing:1.6, valign:'middle' }));
  s.addText('Closing the Seven-Point Gap', T({ x:M, y:0.90, w:CW, h:0.62, fontSize:33, bold:true, fontFace:HF, color:WHITE, valign:'middle' }));

  const acts = [
    ['Name a lead for each open tender', 'Kinbu priced BoQ and Stanbic preliminary estimate', 'Commercial Manager', 'Today'],
    ['Obtain the Priority Insurance drawings', 'Floor finishes schedule and structural drawings', 'Design team / client', '23 Sep'],
    ['Clear the Anglogold budget review', 'Complete since 11 September, awaiting a reviewer', 'Nominated reviewer', '22 Sep'],
    ['Start the Priority Insurance budget', 'Follows the BoQ, cannot begin until the drawings arrive', 'Obed, Sedem, Gilbert', '09 Oct']
  ];
  const ah = 0.94, ag = 0.17, ay0 = 1.82;
  acts.forEach((a, i) => {
    const y = ay0 + i * (ah + ag);
    s.addShape(pres.ShapeType.roundRect, { x:M, y, w:CW, h:ah, rectRadius:0.10,
      fill:{ color:'FFFFFF', transparency:91 }, line:{ color:'FFFFFF', width:0.75, transparency:76 } });
    s.addText(String(i+1), T({ x:M+0.26, y:y+0.22, w:0.5, h:0.5, fontSize:22, bold:true, fontFace:HF, color:AMBER, align:'center', valign:'middle' }));
    s.addText(a[0], T({ x:M+0.92, y:y+0.16, w:6.1, h:0.30, fontSize:13.5, bold:true, color:WHITE, valign:'middle' }));
    s.addText(a[1], T({ x:M+0.92, y:y+0.48, w:6.1, h:0.28, fontSize:10, color:ICE, valign:'middle' }));
    s.addText('OWNER', T({ x:M+7.35, y:y+0.20, w:2.4, h:0.20, fontSize:8, bold:true, color:AMBER, charSpacing:1.1, valign:'middle' }));
    s.addText(a[2], T({ x:M+7.35, y:y+0.42, w:2.4, h:0.30, fontSize:11, color:WHITE, valign:'middle' }));
    s.addText('BY', T({ x:M+10.05, y:y+0.20, w:1.8, h:0.20, fontSize:8, bold:true, color:AMBER, charSpacing:1.1, valign:'middle' }));
    s.addText(a[3], T({ x:M+10.05, y:y+0.42, w:1.8, h:0.30, fontSize:12, bold:true, color:WHITE, valign:'middle' }));
  });

  s.addText('Naming the two tender leads alone closes 1.4 of the remaining 1.5-deliverable gap.',
    T({ x:M, y:6.32, w:8.2, h:0.32, fontSize:13, bold:true, fontFace:HF, color:AMBER, valign:'middle' }));
  s.addText('Source: Commercial Department deliverables register (22 rows), 18 September 2026. Dates read as day/month/year. Deliverable names lightly corrected for spelling.',
    T({ x:M, y:6.92, w:CW, h:0.28, fontSize:8.5, color:'7E8FA6', valign:'middle' }));

  s.addNotes('To close: four actions. Name the two tender leads today. Chase the Priority Insurance drawings by the twenty-third. Clear the Anglogold review by the twenty-second. The Priority budget then follows by the ninth of October. Naming the tender leads on its own recovers almost the whole remaining gap. I need decisions on the tender ownership and the drawings before we leave this room.');
}

pres.writeFile({ fileName: 'Commercial_Department_Deliverables_Sep2026.pptx' })
  .then(f => console.log('WROTE', f));
