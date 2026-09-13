#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    edge=[p for p in d['ports'] if p['role']=='endpoint']; up=[p for p in d['ports'] if p['role']=='uplink']
    checks['untrusted endpoints']=bool(edge) and bool(up) and all(not p['dhcp_trust'] and not p['dai_trust'] and p['port_security_max']==2 for p in edge)
    checks['trusted infrastructure uplink']=all(p['dhcp_trust'] and p['dai_trust'] for p in up)
    checks['DAI binding matches ARP']=all(d['binding'][k]==d['arp'][k] for k in ['ip','mac','vlan','port'])
    checks['refresh RA guard at edge']=all(p['ra_guard'] for p in edge) and all(not p['ra_guard'] for p in up)
    checks['refresh storm threshold bounded']=all(0<p['storm_percent']<=1 for p in edge)
    w=d['wireless']; checks['enterprise AES no embedded PSK']=w['auth']=='WPA2-Enterprise' and w['cipher']=='AES' and not w['psk_in_files']
    detail={'edge_ports':[p['name'] for p in edge],'ARP_binding_match':checks['DAI binding matches ARP']}
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
        mutated['wireless']['cipher']='TKIP'
        assert not accepted(mutated), 'corrupted control must fail'
        mutated=copy.deepcopy(good)
        mutated['ports']=[]
        assert not accepted(mutated), 'invalid scope/address must fail'
        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
