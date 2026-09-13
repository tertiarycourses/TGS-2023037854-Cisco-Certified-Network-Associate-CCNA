#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    p=d['port']; delta={k:d['after'][k]-d['before'][k] for k in d['before']}
    checks['link administrative and operational up']=p['admin']==p['oper']=='up'
    checks['peer speed duplex agreement']=p['speed']==p['peer_speed'] and p['duplex']==p['peer_duplex']=='full'
    checks['endpoint VLAN membership']=p['access_vlan']==p['endpoint_vlan']==10
    checks['fresh counters stable']=all(v==0 for v in delta.values())
    demand=d['poe']['ap_count']*d['poe']['each_watts']; checks['PoE capacity']=demand<=d['poe']['available_watts']
    detail={'counter_delta':delta,'poe_demand_watts':round(demand,1),'poe_margin':round(d['poe']['available_watts']-demand,1)}
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
        mutated['poe']['available_watts']=100
        assert not accepted(mutated), 'corrupted control must fail'

        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
