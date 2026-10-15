import sys,json,math,bisect,hashlib,argparse
from pathlib import Path
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
parser=argparse.ArgumentParser(description='Independent aspect/NFP arithmetic comparison')
parser.add_argument('--cache',type=Path,default=Path(__file__).resolve().parent.parent)
parser.add_argument('--expected',type=Path,default=Path(__file__).resolve().with_name('result.json'))
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
cache=args.cache.resolve()
sys.path.insert(0,str(cache))
from calibrate import VerifiedRanges
import pyarrow as pa,pyarrow.parquet as pq
pa.set_cpu_count(1);pa.set_io_thread_count(1)
plan=json.loads((cache/'range-plan.json').read_text());manifest=json.loads((cache/'ranges.json').read_text());expected=json.loads(args.expected.read_text(encoding='utf-8'))
labels=['[0,4)','[4,6)','[6,8)','[8,10)','[10,12)','[12,16)','[16,infinity)']
names=['vacuum_well','flux_compression_in_regions_of_bad_curvature','qi','edge_rotational_transform_over_n_field_periods','edge_magnetic_mirror_ratio']
flags=[s for s in plan[0]['columns'] if s.startswith('misc.has_')]
cs=defaultdict(Counter);ms=defaultdict(lambda:defaultdict(Counter));ex=defaultdict(Counter);globalc=Counter();qbins=Counter()
def valid(x): return type(x) in (int,float) and math.isfinite(x)
for item in plan:
 rows=pq.ParquetFile(VerifiedRanges(item['entry'],manifest),pre_buffer=False).read(columns=item['columns'],use_threads=False).to_pylist()
 for r in rows:
  globalc['rows']+=1;q=r['metrics.qi']
  if valid(q) and q>=0:globalc['qi_valid']+=1;globalc['qi_pass']+=q<=.0001
  n=r['boundary.n_field_periods'];a=r['metrics.aspect_ratio']
  if n is None:globalc['missing_nfp']+=1;continue
  if not valid(n) or n<=0 or n!=int(n):globalc['invalid_nfp']+=1;continue
  if n not in [1,2,3,4,5]:globalc['other_nfp_'+str(n)]+=1;continue
  groups=[f'nfp_{int(n)}','nfp_1_to_5']
  for g in groups:ex[g]['all_rows']+=1
  if a is None:
   for g in groups:ex[g]['excluded_aspect_missing']+=1
   continue
  if not valid(a) or a<=0:
   for g in groups:ex[g]['excluded_aspect_invalid']+=1
   continue
  bi=bisect.bisect_right([4,6,8,10,12,16],a);label=labels[bi]
  vals=[r['metrics.'+name] for name in names]
  vs=[valid(v) and (i!=2 or v>=0) for i,v in enumerate(vals)]
  ps=[vs[0] and vals[0]>=0,vs[1] and vals[1]<=.9,vs[2] and vals[2]<=1e-4,vs[3] and abs(vals[3])>=.25,vs[4] and vals[4]<=.25]
  keys=[(g,b) for g in groups for b in ['total',label]]
  if n==2 and 9<=a<=11:keys.append(('primary','total'))
  if ps[2]:qbins[f'nfp_{int(n)}:{label}']+=1
  for key in keys:
   c=cs[key];c['rows']+=1;c['complete_metrics']+=all(vs);c['metric_joint']+=all(ps)
   f=r.get('misc.has_neurips_2025_forward_model_error')
   c['forward_error_true' if f is True else 'forward_error_false' if f is False else 'forward_error_unknown']+=1
   c['all_five_historical_flags_known']+=all(type(r.get(z)) is bool for z in flags)
   c['metric_joint_forward_false']+=all(ps) and f is False
   c['original_strict_flag_joint']+=all(ps) and all(r.get(z) is False for z in flags)
   for i,name in enumerate(names):ms[key][name]['valid']+=vs[i];ms[key][name]['passes']+=ps[i]
errors=[]
def compare(key,e):
 c=cs[key]
 for field in ['rows','complete_metrics','metric_joint','metric_joint_forward_false','original_strict_flag_joint','all_five_historical_flags_known','forward_error_true','forward_error_false','forward_error_unknown']:
  if c[field]!=e[field]:errors.append([key,field,c[field],e[field]])
 for name in names:
  for f in ['valid','passes']:
   if ms[key][name][f]!=e['marginals'][name][f]:errors.append([key,name,f])
  for field,den in [('fraction_population',c['rows']),('fraction_valid',ms[key][name]['valid'])]:
   v=ms[key][name]['passes']/den if den else None
   if v!=e['marginals'][name][field]:errors.append([key,name,field])
 for field,den in [('metric_joint_fraction_population',c['rows']),('metric_joint_fraction_complete',c['complete_metrics'])]:
  v=c['metric_joint']/den if den else None
  if v!=e[field]:errors.append([key,field])
for g,e in expected['cohorts'].items():
 for field in ['all_rows','excluded_aspect_missing','excluded_aspect_invalid']:
  if ex[g][field]!=e[field]:errors.append([g,field])
 compare((g,'total'),e['positive_aspect_total'])
 for label in labels:compare((g,label),e['bins'][label])
compare(('primary','total'),expected['primary_closed_slice'])
result={'errors':errors,'global':dict(globalc),'qi_pass_bins':dict(qbins),'pooled_positive':dict(cs[('nfp_1_to_5','total')]),'primary':dict(cs[('primary','total')]),'bin_populations':{g:{l:cs[(g,l)]['rows'] for l in labels} for g in expected['cohorts']},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2));assert not errors
