#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    n=d['neighbors']; winner=min(d['paths'],key=lambda p:sum(p['costs']))
    checks['unique router IDs']=len({x['router_id'] for x in n})==len(n)
    checks['compatible adjacency']=len({(x['area'],x['hello'],x['dead'],x['mtu']) for x in n})==1 and all(x['state']=='FULL' for x in n)
    checks['lowest OSPF path cost']=winner['next']==d['installed_next']
    h=d['hsrp']; checks['single virtual gateway owner']=h['active_count']==h['standby_count']==1 and h['vip']==h['host_gateway'] and h['postfailure_owner']=='R2'
    r=d['refresh']; checks['refresh OSPFv3 IPv6 adjacency']=r['ospfv3']['ipv6_enabled'] and r['ospfv3']['state']=='FULL' and r['ospfv3']['area']==0
    checks['refresh VRRP unique master']=r['vrrp']['masters']==r['vrrp']['backup']==1 and r['vrrp']['vip']==h['vip']
    detail={'path_costs':{p['next']:sum(p['costs']) for p in d['paths']},'virtual_gateway':h['vip']}
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
        mutated['hsrp']['active_count']=2
        assert not accepted(mutated), 'corrupted control must fail'

        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
