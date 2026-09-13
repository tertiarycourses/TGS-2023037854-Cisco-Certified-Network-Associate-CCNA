#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    b,a=d['before'],d['after']; c=d['change']
    checks['isolated trunk hypothesis']=b['gateway_ping'] and b['remote_ip_ping'] and b['dns_ok'] and not b['https_ok'] and not b['vlan20_allowed']
    checks['repaired services and preserved ACL']=all(a[k] for k in ['gateway_ping','remote_ip_ping','dns_ok','https_ok','vlan20_allowed','acl_expected'])
    checks['narrow approved reversible change']=c['target']=='trunk allowed VLAN20' and c['scope']==['trunk VLAN20'] and bool(c['approval']) and bool(c['rollback']) and c['saved_before']
    checks['regressions include isolation']=all(x['pass'] for x in d['regression']) and {x['test'] for x in d['regression']}=={'staff HTTPS','guest-to-staff denied','management SSH'}
    t=d['timeline']; checks['ordered approved timeline']=[x['event'] for x in t]==['detect','approve','change','verify'] and all(t[i]['seconds']<t[i+1]['seconds'] for i in range(len(t)-1))
    detail={'restored_HTTPS':a['https_ok'],'change_scope':c['scope'],'verification_seconds':t[-1]['seconds']}
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
        mutated['timeline'][2]['seconds']=5
        assert not accepted(mutated), 'corrupted control must fail'

        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
