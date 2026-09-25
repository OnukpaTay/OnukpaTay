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

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'Commercial Department';
pres.title  = 'Commercial Department — Outstanding Projects & Deliverables';

/* ---------------- helpers ---------------- */
function footer(s, n){
  s.addText('Commercial Department   ·   Outstanding Projects & Deliverables   ·   25 September 2026',
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

  chip(s, M, 4.52, 2.25, 0.42, '25 SEPTEMBER 2026', AMBER, '1B2A41');

  const stats = [['8','Live deliverables'],['6','Active projects'],['75%','Delivered'],['5','Awaiting review']];
  const bw = 2.72, gap = 0.30;
  stats.forEach((st, i) => {
    const x = M + i * (bw + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y:5.42, w:bw, h:1.10, rectRadius:0.10,
      fill:{ color:'FFFFFF', transparency:90 }, line:{ color:'FFFFFF', width:0.75, transparency:72 } });
    s.addText(st[0], T({ x:x+0.20, y:5.54, w:bw-0.40, h:0.50, fontSize:27, bold:true, fontFace:HF, color:WHITE, valign:'middle' }));
    s.addText(st[1], T({ x:x+0.20, y:6.03, w:bw-0.40, h:0.30, fontSize:10, color:ICE, valign:'middle' }));
  });

  s.addText('Presented by the Commercial Manager', T({ x:M, y:6.88, w:7.5, h:0.30, fontSize:10.5, color:ICE, valign:'middle' }));
  s.addNotes('Good morning. This is the weekly commercial status as at 25 September. The register now carries eight live deliverables across six projects. Six are finished. The headline this week is good news on the tenders and a growing queue in review.');
}

/* ================= SLIDE 2 — EXECUTIVE SUMMARY ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'AT A GLANCE', 'Executive Summary',
    'Position of the commercial deliverables register as at 25 September 2026.');

  const tiles = [
    ['8',  'Live deliverables', 'Across 6 active projects', NAVY],
    ['6',  'Delivered', '75% of the register', GOOD],
    ['5',  'Awaiting review', 'Finished but not signed off', WARN],
    ['2',  'Still open', 'Both on Priority Insurance', CRIT]
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
    [GOOD, 'Both tenders that were at risk last week have landed',
     'The Kinbu priced BoQ moved from 10% to finished and the Stanbic submission from 50% to two completed documents. Neither missed its 25 September deadline.'],
    [WARN, 'Five of the six finished deliverables are sitting in review',
     'Nothing can be closed out until a reviewer signs it off. The Advans final account has been waiting fourteen days, the oldest item in the queue.'],
    [CRIT, 'Priority Insurance has not moved in seven days',
     'Still at 40% against a 50% plan. The floor finishes schedule and structural drawings raised last week have not arrived, so the budget behind it still cannot start.']
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
  s.addNotes('Three things this week. First, the two tenders we flagged as critical last Friday both went in on time, which clears the largest gap on the register. Second, the problem has moved rather than gone away: five finished deliverables are now stuck waiting for a reviewer. Third, Priority Insurance is exactly where it was seven days ago, because the information we asked for has not come.');
}

/* ================= SLIDE 3 — WHERE THEY STAND ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'PORTFOLIO HEALTH', 'Where the 8 Deliverables Stand');

  s.addChart(pres.ChartType.doughnut,
    [{ name:'Delivery status', labels:['Delivered','In progress','Not started'], values:[6, 1, 1] }],
    { x:M, y:y0+0.10, w:5.30, h:4.50, holeSize:62, showTitle:false, showLegend:false, showValue:false,
      chartColors:[GOOD, WARN, MUTED], dataBorder:{ pct:2, color:WHITE } });

  s.addText('8', T({ x:2.27, y:3.34, w:2.0, h:0.62, fontSize:40, bold:true, fontFace:HF, color:NAVY, align:'center', valign:'middle' }));
  s.addText('deliverables', T({ x:2.27, y:3.94, w:2.0, h:0.28, fontSize:11, color:MUTED, align:'center', valign:'middle' }));

  const rx = 6.30, rw = W - M - rx;
  const legend = [
    [GOOD,  'Delivered',   'Finished; 5 of these await review', 6, '75%'],
    [WARN,  'In progress', 'Priority Insurance BoQ, at 40%',    1, '12.5%'],
    [MUTED, 'Not started', 'Priority Insurance budget, on plan',1, '12.5%']
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

  const py = y0 + 0.16 + 3 * (lh + lg) + 0.22;
  card(s, rx, py, rw, 1.66);
  s.addText('Progress against plan', T({ x:rx+0.22, y:py+0.16, w:rw-0.44, h:0.28, fontSize:12.5, bold:true, color:NAVY, valign:'middle' }));
  const bars = [['Planned', 0.8125, '81.3%', ORANGE], ['Actual', 0.800, '80.0%', BLUE]];
  bars.forEach((b, i) => {
    const by = py + 0.56 + i * 0.40;
    s.addText(b[0], T({ x:rx+0.22, y:by-0.04, w:1.05, h:0.26, fontSize:10.5, color:INK2, valign:'middle' }));
    progress(s, rx+1.34, by, 3.10, b[1], null, b[3], 0.17);
    s.addText(b[2], T({ x:rx+4.56, y:by-0.05, w:1.60, h:0.28, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
  });
  s.addText('1.3 points behind plan — the register is effectively on schedule',
    T({ x:rx+0.22, y:py+1.32, w:rw-0.44, h:0.26, fontSize:10.5, bold:true, color:GOOD, valign:'middle' }));

  footer(s, 3);
  s.addNotes('Six of the eight live deliverables are finished. One is in progress and one has not started, and both of those are Priority Insurance. On progress rather than headcount we are at 80.0% against a planned 81.3%, so about one tenth of a deliverable behind. On the numbers the register is on schedule. The issue is not delivery this week, it is sign-off.');
}

/* ================= SLIDE 4 — WEEK ON WEEK ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'MOVEMENT', 'What Changed Since 18 September',
    'Actual completion of every deliverable carried over from last week’s register.');

  // data[0] plots at the BOTTOM; biggest movement ends up at the top
  const mv = [
    ['Priority Ins. — Complete Budget',  0,   0],
    ['Priority Ins. — Complete BoQ',    40,  40],
    ['Stanbic — tender submission',     50, 100],
    ['Kinbu — Priced BoQ',              10, 100]
  ];

  const cw2 = 8.35;
  s.addChart(pres.ChartType.bar, [
    { name:'18 September', labels: mv.map(p=>p[0]), values: mv.map(p=>p[1]) },
    { name:'25 September', labels: mv.map(p=>p[0]), values: mv.map(p=>p[2]) }
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

  s.addText([
    { text:'The register carries live work only. Seventeen deliverables closed last week were removed from it, so the portfolio percentages on slide 3 are not comparable week to week — the comparison above is per deliverable.', options:{ breakLine:true } },
    { text:'Stanbic was recorded last week as a single “Preliminary Estimate” and this week as two documents, “Cost Proposal” and “Relevant Experience and CV”. It is shown here as one submission.', options:{} }
  ], T({ x:M, y:y0+4.18, w:cw2, h:0.62, fontSize:9, color:MUTED, paraSpaceAfter:3, valign:'top' }));

  const rx = M + cw2 + 0.32, rw = W - M - rx;
  const panels = [
    [GOOD, '2', 'tenders closed on time', 'Kinbu and Stanbic both went in by 25 September, clearing the two largest gaps on last week’s register.'],
    [CRIT, '0', 'points of movement', 'Priority Insurance is unchanged at 40% seven days on, still waiting on the same two documents.']
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
  s.addNotes('This is the week on week picture. Kinbu went from ten per cent to finished, Stanbic from half to two completed documents. Those were the two items I flagged as critical last Friday, and both landed. Priority Insurance is the flat line: forty per cent last week, forty per cent today. One caution on the numbers, the register only lists live work, so the overall percentages are not comparable between weeks. That is why this chart compares individual deliverables.');
}

/* ================= SLIDE 5 — DELIVERED ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'COMPLETED WORK', '6 Deliverables Finished Across 5 Projects');

  const done = [
    ['Stanbic Bank', 2, ['Cost Proposal', 'Relevant Experience and CV'], 'Team', true],
    ['Kinbu School Canteen Tender', 1, ['Priced BoQ'], 'Team', true],
    ['Ecole International School', 1, ['BoQ and Budget'], 'Tracy, Obed, Eunice', true],
    ['Advans Savings & Loans', 1, ['Final Account'], 'Tracy', true],
    ['Thoroughbred Place', 1, ['Financial Report (external)'], 'Sedem', false]
  ];

  const COLS = 3, GX = 0.28, GY = 0.22;
  const cw = (CW - (COLS - 1) * GX) / COLS;
  const chh = (CONTENT_BOTTOM - y0 - GY) / 2;
  done.forEach((d, i) => {
    const x = M + (i % COLS) * (cw + GX);
    const y = y0 + Math.floor(i / COLS) * (chh + GY);
    card(s, x, y, cw, chh);
    dot(s, x + cw - 0.40, y + 0.40, 0.44, GOOD, String(d[1]));
    s.addText(d[0], T({ x:x+0.26, y:y+0.18, w:cw-1.02, h:0.52, fontSize:14, bold:true, fontFace:HF, color:NAVY, valign:'top' }));
    s.addText(d[2].map((t, j) => ({ text:t, options:{ bullet:{ indent:13 }, breakLine: j < d[2].length - 1 } })),
      T({ x:x+0.34, y:y+0.78, w:cw-0.62, h:0.66, fontSize:10, color:INK2, paraSpaceAfter:3, valign:'top' }));
    chip(s, x+0.26, y+1.58, 1.92, 0.32, d[4] ? 'AWAITING REVIEW' : 'COMPLETE', d[4] ? WARN : GOOD, d[4] ? '1B2A41' : WHITE);
    s.addText(d[3], T({ x:x+0.26, y:y+1.98, w:cw-0.52, h:0.26, fontSize:9.5, bold:true, color:MUTED, valign:'middle' }));
  });

  footer(s, 5);
  s.addNotes('Six deliverables finished across five projects. The tender team carried three of them. Note the amber chips: five of these six are complete but have not been signed off. Only the Thoroughbred financial report is clear of the review queue.');
}

/* ================= SLIDE 6 — AWAITING REVIEW ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'THE BOTTLENECK', '5 Deliverables Waiting on Review',
    'Finished work that cannot be closed out. Waiting time is measured from the expected finish date.');

  const MAXW = 14;
  const rev = [
    ['Advans Savings & Loans',      'Final Account',              'Tracy',               '11 Sep 2026', 14, CRIT],
    ['Ecole International School',  'BoQ and Budget',             'Tracy, Obed, Eunice', '18 Sep 2026',  7, WARN],
    ['Stanbic Bank',                'Cost Proposal',              'Team',                '25 Sep 2026',  0, MUTED],
    ['Stanbic Bank',                'Relevant Experience and CV', 'Team',                '25 Sep 2026',  0, MUTED],
    ['Kinbu School Canteen Tender', 'Priced BoQ',                 'Team',                '25 Sep 2026',  0, MUTED]
  ];

  const rh = 0.85, rg = (CONTENT_BOTTOM - y0 - rev.length * rh) / (rev.length - 1);
  rev.forEach((r, i) => {
    const y = y0 + i * (rh + rg);
    card(s, M, y, CW, rh);
    dot(s, M + 0.30, y + rh/2, 0.24, r[5]);
    s.addText(r[0], T({ x:M+0.56, y:y+0.13, w:3.40, h:0.26, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(r[1], T({ x:M+0.56, y:y+0.40, w:3.40, h:0.26, fontSize:10, color:INK2, valign:'middle' }));

    s.addText('OWNER',           T({ x:M+4.10, y:y+0.15, w:1.80, h:0.22, fontSize:8, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(r[2],              T({ x:M+4.10, y:y+0.38, w:1.80, h:0.28, fontSize:9.5, color:INK2, valign:'middle' }));
    s.addText('EXPECTED FINISH', T({ x:M+6.05, y:y+0.15, w:1.55, h:0.22, fontSize:8, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(r[3],              T({ x:M+6.05, y:y+0.38, w:1.55, h:0.28, fontSize:10.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText('WAITING',         T({ x:M+7.75, y:y+0.15, w:1.30, h:0.22, fontSize:8, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(r[4] === 0 ? 'Submitted today' : `${r[4]} days`,
                                 T({ x:M+7.75, y:y+0.38, w:1.30, h:0.28, fontSize: r[4] === 0 ? 9.5 : 12, bold:true, color: r[4] === 0 ? INK2 : r[5], valign:'middle' }));

    // queue-age bar, scaled against the oldest item
    const bx = M + 9.20, bw = 2.70;
    s.addShape(pres.ShapeType.roundRect, { x:bx, y:y+(rh-0.17)/2, w:bw, h:0.17, rectRadius:0.085, fill:{color:TRACK}, line:{type:'none'} });
    if (r[4] > 0){
      s.addShape(pres.ShapeType.roundRect, { x:bx, y:y+(rh-0.17)/2, w:Math.max(0.10, bw * r[4]/MAXW), h:0.17,
        rectRadius:0.085, fill:{color:r[5]}, line:{type:'none'} });
    }
  });

  footer(s, 6);
  s.addNotes('This is the slide I most want a decision on. Five finished deliverables are waiting for a reviewer. The Advans final account has been waiting a fortnight, Ecole a week, and the three tender documents went in today so they are not yet late. None of this work can be closed out, and the two oldest are holding up projects we would otherwise report as finished.');
}

/* ================= SLIDE 7 — STILL OUTSTANDING ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'THE WATCH LIST', '2 Deliverables Still Open',
    'Both sit on Priority Insurance. The dark marker shows where each was planned to be today.');

  const out = [
    ['Priority Insurance', 'Complete BoQ',    0.40, 0.50, '30 Sep 2026', 'Obed, Sedem, Gilbert', WARN,  'BLOCKED'],
    ['Priority Insurance', 'Complete Budget', 0.00, 0.00, '09 Oct 2026', 'Obed, Sedem, Gilbert', MUTED, 'ON PLAN']
  ];

  const rh = 1.30, rg = 0.24;
  out.forEach((o, i) => {
    const y = y0 + i * (rh + rg);
    card(s, M, y, CW, rh);
    dot(s, M + 0.34, y + rh/2, 0.28, o[6]);
    s.addText(o[0], T({ x:M+0.70, y:y+0.36, w:2.75, h:0.30, fontSize:13, bold:true, color:NAVY, valign:'middle' }));
    s.addText(o[1], T({ x:M+0.70, y:y+0.68, w:2.75, h:0.28, fontSize:11, color:INK2, valign:'middle' }));

    const bx = M + 3.62, bw = 2.60;
    s.addText(`Actual ${Math.round(o[2]*100)}%`,  T({ x:bx, y:y+0.42, w:1.20, h:0.24, fontSize:10, bold:true, color:NAVY, valign:'middle' }));
    s.addText(`Planned ${Math.round(o[3]*100)}%`, T({ x:bx+bw-1.40, y:y+0.42, w:1.40, h:0.24, fontSize:10, color:MUTED, align:'right', valign:'middle' }));
    progress(s, bx, y + 0.76, bw, o[2], o[3], o[6], 0.18);

    s.addText('DUE',   T({ x:M+6.75, y:y+0.44, w:1.45, h:0.22, fontSize:8, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(o[4],    T({ x:M+6.75, y:y+0.67, w:1.45, h:0.28, fontSize:11, bold:true, color:NAVY, valign:'middle' }));
    s.addText('OWNER', T({ x:M+8.42, y:y+0.44, w:1.85, h:0.22, fontSize:8, bold:true, color:MUTED, charSpacing:1.1, valign:'middle' }));
    s.addText(o[5],    T({ x:M+8.42, y:y+0.67, w:1.85, h:0.28, fontSize:10, color:INK2, valign:'middle' }));

    chip(s, M + 10.52, y + (rh - 0.34)/2, 1.28, 0.34, o[7], o[6], o[6] === WARN ? '1B2A41' : WHITE);
  });

  const cy = y0 + 2 * rh + rg + 0.26;
  card(s, M, cy, CW, 1.48, { fill: PANEL, lineWidth: 0, flat: true });
  s.addText('Why it has not moved', T({ x:M+0.30, y:cy+0.16, w:4.0, h:0.28, fontSize:12, bold:true, color:CRIT, valign:'middle' }));
  s.addText('The architectural take-off has been 90% complete for two weeks. The floor finishes schedule and the structural drawings have still not been issued, so the BoQ cannot be closed. The budget is sequenced behind the BoQ, which is why it correctly shows no progress against a zero plan rather than a slippage.',
    T({ x:M+0.30, y:cy+0.46, w:CW-0.60, h:0.56, fontSize:10.5, color:INK2, valign:'top' }));
  s.addText('Ask: a firm issue date for both documents from the design team and the client.',
    T({ x:M+0.30, y:cy+1.08, w:CW-0.60, h:0.26, fontSize:10.5, bold:true, color:NAVY, valign:'middle' }));

  footer(s, 7);
  s.addNotes('Only two deliverables are still open and both belong to Priority Insurance. The BoQ is ten points behind plan, which is small, but it has not moved at all in seven days because we are waiting on the same two drawings I raised last week. The budget sits behind it and is correctly showing nothing against a zero plan, so it is not late yet, but it will be if the drawings do not come.');
}

/* ================= SLIDE 8 — BLOCKERS ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'ESCALATION', 'Blockers and Decisions Required',
    'Two items cannot be cleared by the commercial department alone.');

  const blockers = [
    [WARN, 'Review bottleneck', 'Stanbic · Kinbu · Ecole · Advans',
     'Five finished deliverables across four projects are waiting to be signed off. The Advans final account has been in the queue fourteen days and Ecole seven. Three more went in today, so the queue will grow again next week unless it is cleared. Until each is reviewed the work cannot be closed out or reported as complete.',
     'Nominate a reviewer for each of the five, and set a clearance date for the two that are already overdue.'],
    [CRIT, 'Missing design information', 'Priority Insurance',
     'The same two documents raised last week, the floor finishes schedule and the structural drawings, have still not been issued. The architectural take-off has been stuck at 90% for a fortnight. The BoQ is now the only deliverable on the register making no progress, and the budget behind it cannot start.',
     'Escalate to the design team and client for a firm issue date. Agree a revised BoQ date if they slip past 30 September.']
  ];

  const bw = (CW - 0.30) / 2, bh = 3.42;
  blockers.forEach((b, i) => {
    const x = M + i * (bw + 0.30);
    card(s, x, y0, bw, bh);
    dot(s, x + 0.54, y0 + 0.50, 0.48, b[0], String(i+1), b[0] === WARN ? '1B2A41' : WHITE);
    s.addText(b[1], T({ x:x+0.94, y:y0+0.22, w:bw-1.18, h:0.56, fontSize:15, bold:true, fontFace:HF, color:NAVY, valign:'middle' }));
    s.addText(b[2], T({ x:x+0.30, y:y0+0.86, w:bw-0.60, h:0.24, fontSize:10, bold:true, color:MUTED, valign:'middle' }));
    s.addText(b[3], T({ x:x+0.30, y:y0+1.20, w:bw-0.60, h:1.14, fontSize:11, color:INK2, valign:'top' }));
    s.addShape(pres.ShapeType.roundRect, { x:x+0.30, y:y0+2.44, w:bw-0.60, h:0.86, rectRadius:0.08,
      fill:{ color:PANEL }, line:{ type:'none' } });
    s.addText('DECISION REQUIRED', T({ x:x+0.46, y:y0+2.54, w:bw-0.92, h:0.20, fontSize:8, bold:true, color:b[0] === WARN ? '9A6B00' : b[0], charSpacing:1.1, valign:'middle' }));
    s.addText(b[4], T({ x:x+0.46, y:y0+2.76, w:bw-0.92, h:0.50, fontSize:10, bold:true, color:NAVY, valign:'top' }));
  });

  card(s, M, y0 + bh + 0.28, CW, 1.00, { fill: NAVY, lineWidth: 0 });
  s.addText('What we need from this meeting', T({ x:M+0.32, y:y0+bh+0.42, w:4.6, h:0.28, fontSize:12, bold:true, color:AMBER, valign:'middle' }));
  s.addText('A named reviewer against each of the five items in the queue, and a firm issue date for the two Priority Insurance drawings.',
    T({ x:M+0.32, y:y0+bh+0.70, w:CW-0.64, h:0.28, fontSize:11.5, color:WHITE, valign:'middle' }));

  footer(s, 8);
  s.addNotes('Two asks. First, the review queue: I need a named reviewer against each of the five items, and a date for the Advans and Ecole ones that are already overdue. Second, the Priority Insurance drawings, which is the same ask as last week and has not been actioned. If those drawings will not arrive before the thirtieth I would rather agree a revised BoQ date now than report a slippage next Friday.');
}

/* ================= SLIDE 9 — WORKLOAD ================= */
{
  const s = pres.addSlide();
  const y0 = header(s, 'RESOURCING', 'Workload Across the Team',
    'Live deliverables held by each team member, split between finished and still open.');

  const people = [['Eunice', 1, 0], ['Gilbert', 0, 2], ['Tracy', 2, 0], ['Obed', 1, 2], ['Sedem', 1, 2], ['Team', 3, 0]];
  s.addChart(pres.ChartType.bar, [
    { name:'Finished',  labels: people.map(p=>p[0]), values: people.map(p=>p[1]) },
    { name:'Still open', labels: people.map(p=>p[0]), values: people.map(p=>p[2]) }
  ], {
    x:M, y:y0, w:7.95, h:4.35, barDir:'bar', barGrouping:'stacked', barGapWidthPct:52,
    chartColors:[GOOD, WARN], showTitle:false,
    showLegend:true, legendPos:'t', legendFontSize:11, legendColor:INK2,
    showValue:true, dataLabelPosition:'ctr', dataLabelFontSize:10, dataLabelColor:NAVY, dataLabelFontBold:true,
    dataLabelFormatCode:'0;;;', dataLabelFontFace:BF,
    valAxisMinVal:0, valAxisMaxVal:4, valAxisMajorUnit:1,
    valAxisLabelFontSize:9, valAxisLabelColor:MUTED,
    catAxisLabelFontSize:11, catAxisLabelColor:INK2,
    valGridLine:{ color:LINE, size:1 }, catGridLine:{ style:'none' },
    valAxisLineColor:LINE, catAxisLineColor:LINE,
    catAxisLabelFontFace:BF, valAxisLabelFontFace:BF, legendFontFace:BF
  });

  const nx = M + 8.25, nw = W - M - nx;
  const notes = [
    ['The tender team cleared everything', 'All three items held against "Team", both Stanbic documents and the Kinbu priced BoQ, were finished this week.'],
    ['Gilbert has nothing finished', 'Both of his items are the Priority Insurance BoQ and budget. That is a blockage on drawings, not a delivery problem.'],
    ['One project holds every open item', 'Priority Insurance accounts for all four open entries shown here, across Obed, Sedem and Gilbert.']
  ];
  const nh = 1.28;
  notes.forEach((n, i) => {
    const y = y0 + i * (nh + 0.18);
    card(s, nx, y, nw, nh, { fill: PANEL, lineWidth: 0, flat: true });
    s.addText(n[0], T({ x:nx+0.24, y:y+0.16, w:nw-0.48, h:0.30, fontSize:11.5, bold:true, color:NAVY, valign:'middle' }));
    s.addText(n[1], T({ x:nx+0.24, y:y+0.48, w:nw-0.48, h:0.66, fontSize:10, color:INK2, valign:'top' }));
  });

  s.addText([
    { text:'Shared deliverables count once for each named owner, so the totals here (14) exceed the 8 items on the register. "Team" means no individual was named.', options:{ breakLine:true } },
    { text:'Source: Commercial Department deliverables register, 25 September 2026. Dates read as day/month/year. The register gives the Stanbic "Relevant Experience and CV" finish date as 25 September 2027; it is read here as 2026.', options:{} }
  ], T({ x:M, y:y0+4.42, w:CW, h:0.62, fontSize:8.5, color:MUTED, paraSpaceAfter:3, valign:'top' }));

  footer(s, 9);
  s.addNotes('On resourcing: the tender team cleared all three of its items this week. Tracy and Eunice are clear. Gilbert, Obed and Sedem carry the four open entries between them, and every one of those is Priority Insurance. So the department has capacity once the review queue clears. One data note, the register gives a 2027 finish date against one of the Stanbic documents; I have read that as this year.');
}

pres.writeFile({ fileName: 'Commercial_Department_Deliverables_2026-09-25.pptx' })
  .then(f => console.log('WROTE', f));
