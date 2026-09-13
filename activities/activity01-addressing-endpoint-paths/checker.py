#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    nets=[ipaddress.ip_network(x['prefix']) for x in d['allocations']]
    checks['VLSM capacity']=len(nets)==3 and all(n.num_addresses-2>=x['required'] for n,x in zip(nets,d['allocations']))
    checks['VLSM no overlap']=all(not a.overlaps(b) for i,a in enumerate(nets) for b in nets[i+1:])
    host=ipaddress.ip_interface(d['host']); gw=ipaddress.ip_address(d['gateway'])
    checks['usable local gateway']=gw in host.network and gw not in [host.network.network_address,host.network.broadcast_address,host.ip] and host.ip not in [host.network.network_address,host.network.broadcast_address]
    checks['remote destination is routed']=ipaddress.ip_address(d['remote']) not in host.network
    checks['ARP and frame target gateway']=d['arp_target']==d['gateway'] and d['frame_dst']==d['gateway_mac']
    detail={'usable_hosts':[n.num_addresses-2 for n in nets],'packet_destination':d['remote'],'next_hop':d['gateway']}
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
        mutated['allocations'][1]['prefix']='10.10.0.0/27'
        assert not accepted(mutated), 'corrupted control must fail'
        mutated=copy.deepcopy(good)
        mutated['host']='10.10.0.63/26'
        assert not accepted(mutated), 'invalid scope/address must fail'
        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
