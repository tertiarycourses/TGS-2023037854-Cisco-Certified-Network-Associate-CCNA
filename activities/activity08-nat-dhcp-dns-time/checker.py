#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    t=d['translations']; tuples=[(x['global'],x['global_port'],x['protocol']) for x in t]
    checks['PAT tuple disambiguation']=len(t)>=2 and len(set(tuples))==len(t) and len({x['inside'] for x in t})==len(t) and all(0<x['global_port']<65536 for x in t)
    l=d['lease']; net=ipaddress.ip_interface(l['ip']).network
    checks['DHCP scope and options']=ipaddress.ip_address(l['gateway']) in net and ipaddress.ip_interface(l['ip']).ip not in [net.network_address,net.broadcast_address] and ipaddress.ip_address(l['gateway']) not in [net.network_address,net.broadcast_address] and l['giaddr']==l['gateway'] and l['dns']=='192.0.2.53' and l['sequence']==['DISCOVER','OFFER','REQUEST','ACK']
    records={x['type']:x for x in d['dns']}; checks['DNS forward and refresh records']={'A','AAAA','MX','NS','PTR'}<=set(records) and records['PTR']['value']==records['A']['name'] and records['MX']['value'].startswith('10 ') and records['NS']['value']=='ns1.example.test' and ipaddress.ip_address(records['A']['value']).version==4 and ipaddress.ip_address(records['AAAA']['value']).version==6
    n=d['ntp']; checks['NTP selected synchronized source']=n['synchronized'] and abs(n['offset_ms'])<=n['budget_ms']
    x=d['transfer']; digest=hashlib.sha256((ROOT/'transfer-copy.cfg').read_bytes()).hexdigest(); checks['secure transfer integrity']=x['protocol'] in ['SFTP','SCP'] and x['hash_before']==x['hash_after']==digest
    detail={'PAT_global_tuples':tuples,'DHCP_network':str(net),'DNS_record_types':sorted(records),'offset_ms':n['offset_ms']}
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
        mutated['transfer']['hash_after']='modified'
        assert not accepted(mutated), 'corrupted control must fail'
        mutated=copy.deepcopy(good)
        mutated['dns'][1]['value']='not-an-ipv6-address'
        assert not accepted(mutated), 'invalid scope/address must fail'
        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
