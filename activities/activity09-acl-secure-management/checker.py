#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    def verdict(f):
        for r in d['rules']:
            if ipaddress.ip_address(f['source']) in ipaddress.ip_network(r['source']) and ipaddress.ip_address(f['destination']) in ipaddress.ip_network(r['destination']) and r['protocol'] in ['ip',f['protocol']] and (r['port'] is None or r['port']==f['port']): return r['action']
        return 'deny'
    decisions=[verdict(f) for f in d['flows']]
    checks['ACL first-match flow matrix']=len(d['flows'])>=3 and {f['expected'] for f in d['flows']}=={'permit','deny'} and all(v==f['expected'] for v,f in zip(decisions,d['flows']))
    v=d['vty']; checks['SSH only and bounded session']=v['transport']==['ssh'] and 0<v['timeout_minutes']<=5 and v['local_secret']
    a=d['aaa']; checks['AAA client and server roles']=a['client']=='router' and a['protocol']=='RADIUS' and a['auth_port']==1812 and a['server']=='192.0.2.181'
    checks['tested local fallback']=a['fallback']=='local' and a['console_tested']
    detail={'flow_verdicts':decisions,'AAA_client':a['client'],'AAA_server':a['server']}
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
        mutated['aaa']['client']='server'
        assert not accepted(mutated), 'corrupted control must fail'
        mutated=copy.deepcopy(good)
        mutated['flows']=[]
        assert not accepted(mutated), 'invalid scope/address must fail'
        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
