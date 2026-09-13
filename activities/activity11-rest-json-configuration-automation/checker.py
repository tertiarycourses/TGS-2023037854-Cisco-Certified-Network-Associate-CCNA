#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    r=d['response']; checks['REST success and JSON media']=r['status']==200 and r['content_type']=='application/json'
    entries=r['body']['interfaces']; checks['JSON interface schema']=all(type(x['enabled']) is bool and isinstance(x['name'],str) and isinstance(x['description'],str) for x in entries)
    live=next(x for x in entries if x['name']==d['desired']['name']); plan={k:v for k,v in d['desired'].items() if live.get(k)!=v}
    checks['desired state idempotent']=plan=={}
    q=d['request']; checks['read request secure']=q['method']=='GET' and q['tls_verify'] and not q['token_in_file']
    a=d['agent']; prompt=a['prompt'].lower(); checks['bounded agentic proposal']=not a['allow_writes'] and a['sanitized'] and all(s in prompt for s in ['sanitized','rollback','do not execute','human approval'])
    detail={'change_plan':plan,'second_run_plan':{} if plan=={} else 'Apply candidate only after review; not executed','request_method':q['method']}
    return checks,detail
def run(path):
    try:
        d=json.loads(Path(path).read_text()); checks,detail=evaluate(d)
        for name,ok in checks.items(): print(('PASS' if ok else 'FAIL')+' | '+name)
        print('OFFLINE FIXTURE ANALYSIS; no hardware/API execution')
        print(json.dumps(detail,indent=2))
        return 0 if checks and all(checks.values()) else 1
    except (ValueError,KeyError,TypeError,StopIteration,OSError) as e:
        print('INVALID EVIDENCE: '+str(e)); return 2
def accepted(d):
    try:
        c,_=evaluate(d); return bool(c) and all(c.values())
    except (ValueError,KeyError,TypeError,StopIteration,OSError): return False
if __name__=='__main__':
    if '--self-test' in sys.argv:
        import copy
        good=json.loads((ROOT/'reference.json').read_text()); bad=json.loads((ROOT/'faulty.json').read_text())
        assert accepted(good), 'reference must pass'
        assert not accepted(bad), 'faulty case must fail'
        mutated=copy.deepcopy(good)
        mutated['request']['method']='PATCH'
        assert not accepted(mutated), 'corrupted control must fail'

        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
