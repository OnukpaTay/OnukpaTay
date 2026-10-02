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

const REPORT_DATE = '25 September 2026';          // shown in the footer
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



/* ---- using the helpers ----------------------------------------------------
 *   const s  = pres.addSlide();
 *   const y0 = header(s, 'EYEBROW', 'Slide title', 'Optional subtitle');
 *   card(s, M, y0, CW, 0.9);                       // white card with shadow
 *   card(s, M, y0, CW, 0.9, { fill: PANEL, lineWidth: 0, flat: true });
 *   dot(s, M + 0.5, y0 + 0.45, 0.46, GOOD, '1');   // badge with a numeral
 *   progress(s, x, y, 3.0, 0.4, 0.5, WARN);        // actual 40%, planned tick at 50%
 *   chip(s, x, y, 1.3, 0.34, 'BLOCKED', WARN, NAVY);
 *   footer(s, 3);
 *   s.addNotes('What the presenter actually says.');
 *
 * Finish with:
 *   pres.writeFile({ fileName: 'deck.pptx' }).then(f => console.log('WROTE', f));
 * ------------------------------------------------------------------------- */
