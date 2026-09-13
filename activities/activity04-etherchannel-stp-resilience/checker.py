#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    m=d['members']; root=min(d['switches'],key=lambda x:(x['priority'],int(x['mac'],16)))['name']
    checks['LACP initiation']=all('active' in (x['mode'],x['peer_mode']) for x in m)
    checks['channel member consistency']=len({(x['speed'],x['vlan_signature']) for x in m})==1 and all(x['bundled'] for x in m)
    checks['intended STP root']=root==d['observed_root']=='DIST1'
    checks['one redundant alternate']=sorted(x['state'] for x in d['paths'])==['alternate','forwarding']
    alternate=[x['name'] for x in d['paths'] if x['state']=='alternate']; f=d['failure']
    checks['alternate takes over within budget']=f['new_forwarding'] in alternate and f['failed']!=f['new_forwarding'] and f['seconds']<=f['budget']
    detail={'calculated_root':root,'convergence_seconds':f['seconds']}
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
        mutated['observed_root']='DIST2'
        assert not accepted(mutated), 'corrupted control must fail'

        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
