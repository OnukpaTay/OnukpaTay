import json, os
exec(open('fixes.py').read())

FLOORS=[('F00','Substructure','Raft foundation & starters (Foundation to Ground)'),
('F01','Ground Floor','Ground floor (+300) - elements rising to next level'),
('F02','M1 Level','M1 Level 1B Parking (+2500)'),
('F03','First Floor','First Floor Level 2A Parking (+4150)'),
('F04','M2 Level','M2 Level 2B Parking (+5200)'),
('F05','Second Floor','Second Floor Level 3A Parking (+6850)'),
('F06','Mezzanine Floor','Mezzanine Floor 3B Parking (+7900)'),
('F07','Third Floor','Third Floor (+10900)'),
('F08','Fourth Floor','Fourth Floor (+14200) - typical 4th-8th'),
('F09','Fifth Floor','Fifth Floor (+17500) - typical 4th-8th'),
('F10','Sixth Floor','Sixth Floor (+20800) - typical 4th-8th'),
('F11','Seventh Floor','Seventh Floor (+24100) - typical 4th-8th'),
('F12','Eighth Floor','Eighth Floor (+27400) - typical 4th-8th'),
('F13','Ninth Floor','Ninth Floor (+30700)'),
('F14','Tenth Floor','Tenth Floor (+34000)'),
('F15','Roof Top Terrace','Roof Top Terrace (+37300)'),
('F16','Roof Level','Roof Level (+40450)'),
('F17','Top of Lift Core','Top of Lift Core (+44650)')]
STOREY={'FOUNDATION':'F00','GROUND':'F01','M1':'F02','FIRST':'F03','M2':'F04','SECOND':'F05','MEZZ':'F06','THIRD':'F07',
'FOURTH':'F08','FIFTH':'F09','SIXTH':'F10','SEVENTH':'F11','EIGHT':'F12','NINTH':'F13','TENTH':'F14','ROOF TOP':'F15','ROOF':'F16'}

# drawing number = page-1 (SHC-KANESHIE-STR-xxx)
def dwg(p): return 'STR-%03d'%(p-1)

def sched(page):
    rows={}
    fn='rows_%d.json'%page
    if os.path.exists(fn) and not FIX.get(page,{}).get('__replace__'):
        for r in json.load(open(fn)):
            mk=r['mark']
            if mk in rows: continue
            v=(int(r['nums'][0]),int(r['nums'][1]),int(r['nums'][2]))
            if v[1]>1500 or not (100<=v[2]<=12500): continue
            rows[mk]=v
    for mk,v in FIX.get(page,{}).items():
        if mk=='__replace__': continue
        if v is None: rows.pop(mk,None)
        else: rows[mk]=v
    return dict(sorted(rows.items()))
