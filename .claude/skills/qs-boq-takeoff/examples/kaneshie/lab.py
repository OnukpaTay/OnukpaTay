# capture Q terms with labels from qty.py
import sys,re,collections
src=open('qty.py').read()
old="def add(sheet,key,term):\n    if term not in (None,'','0'): Q[sheet][key].append(term)"
assert old in src
src=src.replace(old,"def add(sheet,key,term):\n    if term not in (None,'','0'):\n        Q[sheet][key].append(term); _CAP(sheet,key,term,sys._getframe(1).f_locals)")
LV={'F00':'Substructure (raft to GF)','F01':'Ground floor (+300)','F02':'M1 level 1B (+2500)','F03':'First floor 2A (+4150)','F04':'M2 level 2B (+5200)',
'F05':'Second floor 3A (+6850)','F06':'Mezzanine 3B (+7900)','F07':'Third floor (+10900)','F08':'Fourth floor (+14200)','F09':'Fifth floor (+17500)',
'F10':'Sixth floor (+20800)','F11':'Seventh floor (+24100)','F12':'Eighth floor (+27400)','F13':'Ninth floor (+30700)','F14':'Tenth floor (+34000)',
'F15':'Roof top terrace (+37300)','F16':'Roof level (+40450)','F17':'Top of lift core (+44650)'}
AL={'GF':'Ground floor','1F':'First floor (2A)','2F':'Second floor (3A)','MEZZ':'Mezzanine (3B)','3F':'Third floor','4F':'Fourth floor','5F':'Fifth floor',
'6F':'Sixth floor','7F':'Seventh floor','8F':'Eighth floor','9F':'Ninth floor','10F':'Tenth floor','RT':'Roof top terrace','ROOF':'Roof level'}
STN={'FOUNDATION':'raft to GF','GROUND':'GF to M1','M1':'M1 to 1st','FIRST':'1st to M2','M2':'M2 to 2nd','SECOND':'2nd to Mezz','MEZZ':'Mezz to 3rd',
'THIRD':'3rd to 4th','FOURTH':'4th to 5th','FIFTH':'5th to 6th','SIXTH':'6th to 7th','SEVENTH':'7th to 8th','EIGHT':'8th to 9th','NINTH':'9th to 10th','TENTH':'10th to roof terrace','ROOF TOP':'roof terrace to roof'}
KD={'slab':'Suspended slab: measured area x 250 thk','fs':'Slab soffit: measured area','fe':'Slab edge: measured perimeter','slab150':'Roof slab 150 thk: area x thk',
'beam':'Downstand beams: length x width x depth','fb':'Beam sides & soffit: length x (2 x depth + width)','coping':'Parapet coping: length x 300 x 150',
'lintel':'Lintels: openings','fl':'Lintel / coping formwork','blk150':'150 blockwork: wall length x storey ht','blk200':'200 blockwork: wall length x storey ht',
'rint':'Internal render: wall faces','rwet':'Washroom walls: approx. nr x 8.0m girth x ht less door','wtile':'Washroom wall tiling to 2.4m high','pwet':'Washroom walls above tiling',
'rext':'External walls: perimeter x storey ht less windows','burglar':'Window areas (burglar proofing)','screed':'Tiled floor areas (measured)','bed':'Tiled floor areas (measured)',
'ceil':'Ceiling areas (measured)','ceilwet':'Washroom ceiling areas (measured)','pwood':'Timber doors both faces + frames','frame':'Door frames: nr x (2 x ht + width)',
'stop':'Door stops: nr x (2 x ht + width)','hinge':'Timber door leaves x 1.5 pairs','lock':'D3/D4 doors','ilock':'D6 doors','wp':'Waterproofing area','wps':'Waterproofing screed area',
'flash':'Flashing length','gutter':'Gutter length','t_wet':'Wet areas (measured)','t_lob':'Lobbies (measured)','t_ns':'Corridors/terraces/service (measured)',
't_semi':'Habitable rooms (measured)','t_int':'External/unlabelled paved areas (measured)','t_pu':'Parking & ramps (measured)'}
WL={'22.05':'main stair core walls (22.05 m run)','21.825':'lift core walls (21.825 m run)','25.57':'emergency stair core walls (25.57 m run)'}
CAP=collections.defaultdict(list)   # sheet -> [(key,term,label)]
def _CAP(sheet,key,term,L):
    f=L.get('f'); lab=None
    lvl=LV.get(f) if isinstance(f,str) else None
    alv=AL.get(f) if isinstance(f,str) else None
    if key in ('slab','fs','fe','beam','fb'):
        lab='%s - %s'%(lvl,KD[key]) if key not in('beam','fb') else '%s - %s wide beams: length x width x depth'%(lvl,'300' if '0.3' in term.split('*')[1:2] or '+0.3)' in term else '200')
        if key=='fb': lab='%s - beam sides & soffit (%s wide): length x girth'%(lvl,'300' if '0.3)' in term else '200')
        if sheet=='12TH' and term.startswith(('31.4','34.0','176.3','16.3','159.3','17.3')): lab='Roof level / lift core roof - '+KD[key]
    elif key in ('col','fc','colpaint'):
        lab='%s x%d - %s (%s), ht %s'%(L['t'],L['nos'],{'col':'column','fc':'column sides','colpaint':'column faces'}[key],STN[L['st']],'%g'%(L['h'] if L['st']=='FOUNDATION' else round(L['h']-0.25,3)))
    elif key in ('wsh','wlift','fw') and sheet=='12TH' and '*4.05' in term:
        lab='Lift overrun (roof to top of lift core, 4.05 high) - lift core walls'+(' (both faces)' if key=='fw' else ': run x ht x 250 thk')
    elif key in ('wsh','wlift','fw'):
        ln=term.split('*')[1] if term.startswith('2*') else term.split('*')[0]
        lab='%s - %s%s'%(lvl or 'Roof level / lift overrun',WL.get(ln,ln),' (both faces)' if key=='fw' else ': run x ht x 250 thk')
    elif key in ('stair','fst','t_stair'):
        D=L.get('D'); kind='Main stair' if D is L.get('SMAIN') else 'Emergency stair'
        lab='%s - %s flight (storey ht %g)'%(lvl,kind,L['h'])
    elif key.startswith('r_'):
        lab='%s - %s, Y%s (from reinforcement take-off / BBS)'%(LV.get(f,f),L['e'],L['dd'])
    elif key.startswith('n_'):
        lab='%s - %s'%(alv,L['n'])
    elif key=='bed' and term.startswith('(2*1.8'):
        lab='Stair finishes (treads, risers, landings)'
    elif key in KD and alv and key not in ('coping','wp','wps','flash','gutter','slab150'):
        lab='%s - %s'%(alv,KD[key])
    else:
        lab=KD.get(key,key)
    CAP[sheet].append((key,term,lab,f if isinstance(f,str) and f in AL else None))
ns={'__name__':'qtylab','_CAP':_CAP,'sys':sys}
exec(compile(src,'qty.py','exec'),ns)
OPEN=ns['OPEN']; DIM=ns['DIM']; ASH=ns['ASH']; Q=ns['Q']
