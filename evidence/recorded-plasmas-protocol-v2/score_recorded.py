"""Score two hash-bound recorded boundaries once; no optimization or new gates."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import math
import re
from pathlib import Path
import subprocess
import sys
import time
import traceback

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'c18-recovered-radial'))
import run_pair as shared

guard = shared.guard
from utc_supervisor import supervise


def claim_check(manifest,digest):
    root=Path(manifest['coordination'])
    note=root/'notes/codex.md';text=note.read_text()
    pattern=rf'^C18-RECORDED-V2 CLAIM manifest={digest} start=(\S+) end=(\S+)$'
    matches=re.findall(pattern,text,re.MULTILINE)
    guard.need(len(matches)==1,'one explicit current root claim required')
    start,end=map(guard.timestamp,matches[0]);now=datetime.now(timezone.utc)
    guard.need(start<=now and (end-now).total_seconds()>=900,'resource claim expired or too short')
    snapshot=root/'automation/process-check.json';record=guard.load(snapshot)
    age=(now-guard.timestamp(record['checked_at'])).total_seconds()
    guard.need(0<=age<300 and record['native_compute_pids']==[], 'stale or occupied inventory')
    guard.need(record['controller_lock_held'] is True and record['other_codex_exec_worker'] is False,
               'controller ownership mismatch')
    guard.need(not (root/'automation/STOP').exists(),'STOP present')
    guard.need(manifest['execution_authority']=='User25October2026continue; existing112lane',
               'task authority mismatch')
    return dict(claim_start=start.isoformat(),claim_end=end.isoformat(),
                peer_checkpoint_sha256=guard.sha(root/'notes/claude.md'),
                own_note_sha256=guard.sha(note),controller=record)


def validate(report, item):
    guard.need(tuple(report['targets']) == (item['id'],), 'custom target mismatch')
    record = report['targets'][item['id']]
    guard.need(record['completed'] is True and record['input_sha256'] == item['sha256'],
               'incomplete score or input mismatch')
    guard.need(record['conversion_validation']['passed'] is True, 'conversion failed')
    vmec = record['vmec']
    guard.need((vmec['ns'],vmec['mpol'],vmec['ntor'],vmec['ier_flag']) == (99,10,10,0),
               'unexpected grid or convergence flag')
    guard.need(len(record['metrics']) == 12 and all(type(x) in (float,int) and math.isfinite(x)
               for x in record['metrics'].values()), 'nonfinite or missing metrics')
    guard.need(report['physical_admission'] is False, 'unexpected physical admission')
    return record


def child(manifest, digest):
    guard.verify_runtime(manifest)
    for path, expected in manifest['files_sha256'].items():
        guard.need(guard.sha(path) == expected, f'child identity mismatch: {path}')
    claim_check(manifest,digest)
    output=Path(manifest['output'])
    with (output/'child-started.json').open('x') as stream:
        json.dump({'manifest_sha256':digest,'started_at':datetime.now(timezone.utc).isoformat()},stream)
    from constellaration.mhd import vmec_settings
    spec=importlib.util.spec_from_file_location('recorded_scorer',manifest['scorer'])
    scorer=importlib.util.module_from_spec(spec);spec.loader.exec_module(scorer)
    rows=[]
    with shared.capture_defaults(vmec_settings,output) as settings:
        for item in manifest['inputs']:
            sys.argv=[manifest['scorer'],'--input',item['path'],'--sha256',item['sha256'],
                      '--target-id',item['id'],'--output',str(output/item['id'])]
            code=scorer.main()
            report_path=output/item['id']/'report.json'
            guard.need(code==0, f'scorer failed: {item["id"]}')
            report=guard.load(report_path)
            row=validate(report,item)
            rows.append({'id':item['id'],'report_sha256':guard.sha(report_path),
                         'input_sha256':item['sha256'],'record':row})
            guard.write(output/f'{item["id"]}-completed.json',rows[-1])
    guard.need(len(settings)==2,'one effective default per boundary required')
    guard.write(output/'scores.json',{'completed':True,'physical_admission':False,'rows':rows,
        'interpretation':'Same frozen near-vacuum forward model; no old Step3 verdict is changed.'})


def main():
    started=time.monotonic();started_utc=time.time()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',required=True,type=Path)
    parser.add_argument('--manifest-sha256',required=True)
    mode=parser.add_mutually_exclusive_group();mode.add_argument('--execute',action='store_true');mode.add_argument('--child',action='store_true')
    args=parser.parse_args();guard.need(guard.sha(args.manifest)==args.manifest_sha256,'manifest mismatch')
    manifest=guard.load(args.manifest)
    if args.child:
        child(manifest,args.manifest_sha256);return 0
    source=manifest['source']
    head=subprocess.check_output(['git','-C',source,'rev-parse','HEAD'],text=True).strip()
    dirty=subprocess.check_output(['git','-C',source,'status','--porcelain'],text=True).strip()
    guard.verify_files(manifest,head,dirty)
    preflight=claim_check(manifest,args.manifest_sha256)
    if not args.execute:
        print(json.dumps({'preflight':preflight,'native_started':False}));return 0
    output=Path(manifest['output']);output.mkdir(exist_ok=False)
    for name in ['cache','tmp']:(output/name).mkdir()
    guard.write(output/'preflight.json',preflight)
    command=[manifest['native_python'],'-B',str(Path(__file__).resolve()),'--manifest',str(args.manifest.resolve()),'--manifest-sha256',args.manifest_sha256,'--child']
    outcome={'completed':False,'physical_admission':False,'manifest_sha256':args.manifest_sha256}
    try:
        run=supervise(command,output,guard.clean_environment(output),Path(manifest['coordination'])/'automation/STOP',limits={**guard.LIMITS,'wall_seconds':min(840,870-max(time.monotonic()-started,time.time()-started_utc))},reservation_end=guard.timestamp(preflight['claim_end']).timestamp())
        outcome['execution']=run
        guard.need(run['exit_code']==0 and run['stop_reason'] is None,'native child incomplete')
        for path,expected in manifest['files_sha256'].items():
            guard.need(guard.sha(path)==expected,f'postflight identity mismatch:{path}')
        scores=guard.load(output/'scores.json');guard.need(scores['completed'],'scores incomplete')
        outcome['scores_sha256']=guard.sha(output/'scores.json')
        guard.need(max(time.monotonic()-started,time.time()-started_utc)<900,'900second task limit exceeded')
        outcome['completed']=True
    except Exception:outcome['error']=traceback.format_exc()
    finally:
        outcome['monotonic_seconds']=time.monotonic()-started;outcome['utc_elapsed_seconds']=time.time()-started_utc;guard.write(output/'launch-result.json',outcome)
    return 0 if outcome['completed'] else 1


if __name__=='__main__':sys.exit(main())
