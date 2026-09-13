#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    def lookup(target,routes):
        candidates=[r for r in routes if r['up'] and ipaddress.ip_address(target) in ipaddress.ip_network(r['prefix'])]
        return min(candidates,key=lambda r:(-ipaddress.ip_network(r['prefix']).prefixlen,r['distance']))
    selected=lookup(d['target'],d['routes']); specific=[r for r in d['routes'] if r['prefix']==d['failure_prefix']]
    checks['host route longest match']=selected['prefix']=='192.0.2.50/32' and selected['next']==d['expected_next']
    checks['floating distance greater']=next(r['distance'] for r in specific if r['next']=='10.0.0.6')>next(r['distance'] for r in specific if r['next']=='10.0.0.2')
    failed=[dict(r,up=False) if r['next']=='10.0.0.2' else r for r in d['routes']]
    backup=lookup('192.0.2.51',failed); checks['backup selected after withdrawal']=backup['next']=='10.0.0.6' and backup['distance']==200
    v=d['ipv6']; checks['IPv6 link-local scope']=ipaddress.ip_address(v['next']).is_link_local and v['interface']=='Gi0/0' and ipaddress.ip_network(v['prefix']).version==6
    detail={'selected':selected,'withdrawal_backup':backup}
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
        mutated['routes'][2]['prefix']='192.0.2.50/31'
        assert not accepted(mutated), 'corrupted control must fail'

        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
