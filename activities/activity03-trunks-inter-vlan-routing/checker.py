#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    a,b=d['left'],d['right']; common=set(a['allowed'])&set(b['allowed'])
    checks['both interfaces trunks']=a['mode']==b['mode']=='trunk'
    checks['native VLAN agreement']=a['native']==b['native']==99
    checks['end-to-end VLAN allowance']={10,20,99}<=common
    checks['layer3 enabled']=d['ip_routing'] is True
    checks['SVI gateways']=all(s['up'] and str(ipaddress.ip_interface(s['prefix']).ip)==f"10.10.{s['vlan']}.1" for s in d['svIs']) and {s['vlan'] for s in d['svIs']}=={10,20}
    detail={'common_allowed_vlans':sorted(common),'gateways':[s['prefix'] for s in d['svIs']]}
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
        mutated['ip_routing']=False
        assert not accepted(mutated), 'corrupted control must fail'

        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
