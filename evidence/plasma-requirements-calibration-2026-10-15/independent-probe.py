import sys,json,math,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
base=Path('/Users/patrickkoch/projects/nuclear-fusion-at-home-workforce-alignment/worktrees/codex-calibration/results')
sys.path.insert(0,str(base))
from calibrate import VerifiedRanges
import pyarrow as pa
import pyarrow.parquet as pq
pa.set_cpu_count(1); pa.set_io_thread_count(1)
plan=json.loads((base/'range-plan.json').read_text()); manifest=json.loads((base/'ranges.json').read_text())
rows=[]
for item in plan:
 rows.extend(pq.ParquetFile(VerifiedRanges(item['entry'],manifest),pre_buffer=False).read(columns=item['columns'],use_threads=False).to_pylist())
def numeric(x):
 return type(x) in (int,float) and math.isfinite(x)
sel=[r for r in rows if numeric(r.get('boundary.n_field_periods')) and r['boundary.n_field_periods']==2 and numeric(r.get('metrics.aspect_ratio')) and r['metrics.aspect_ratio']>=9 and r['metrics.aspect_ratio']<=11]
checks=[('vacuum_well',lambda x:x>=0),('flux_compression_in_regions_of_bad_curvature',lambda x:x<=.9),('qi',lambda x:0<=x<=.0001),('edge_rotational_transform_over_n_field_periods',lambda x:abs(x)>=.25),('edge_magnetic_mirror_ratio',lambda x:x<=.25)]
counts={}
for k,func in checks:
 vals=[r.get('metrics.'+k) for r in sel]
 valid=[v for v in vals if numeric(v) and (k!='qi' or v>=0)]
 counts[k]={'valid':len(valid),'pass':sum(func(v) for v in valid)}
flags=[c for c in plan[0]['columns'] if c.startswith('misc.has_')]
metricjoint=[r for r in sel if all(numeric(r.get('metrics.'+k)) and f(r['metrics.'+k]) for k,f in checks)]
joint=[r for r in metricjoint if all(type(r.get(k)) is bool and r[k]==False for k in flags)]
def qmin(rs):
 vals=[(r['metrics.qi'],r.get('plasma_config_id')) for r in rs if numeric(r.get('metrics.qi')) and r['metrics.qi']>=0]
 return {'valid':len(vals),'minimum':min(vals) if vals else None,'pass_le_1e_4':sum(v<=1e-4 for v,i in vals)}
result={'total':len(rows),'selected':len(sel),'marginals':counts,'metric_only_joint':len(metricjoint),'joint':len(joint),'selected_qi':qmin(sel),'global_qi':qmin(rows),'negative_signed_transform':sum(r['metrics.edge_rotational_transform_over_n_field_periods']<0 for r in sel),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path('/tmp/calibration113-review/result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
