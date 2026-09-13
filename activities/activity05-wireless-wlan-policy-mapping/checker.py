#!/usr/bin/env python3
"""Independent offline fixture checker. Does not connect to/configure network devices."""
import json, sys, ipaddress, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evaluate(d):
    checks={}; detail={}
    wl={x['ssid']:x for x in d['wlans']}
    checks['staff enterprise and VLAN20']=wl['Staff']['vlan']==20 and wl['Staff']['auth']=='WPA2-Enterprise'
    checks['clients match WLAN subnet']=bool(d['clients']) and all(ipaddress.ip_interface(c['ip']).network==ipaddress.ip_network(f"10.10.{wl[c['ssid']]['vlan']}.0/24") and ipaddress.ip_address(c['gateway']) in ipaddress.ip_interface(c['ip']).network and ipaddress.ip_address(c['gateway']) not in [ipaddress.ip_interface(c['ip']).network.network_address,ipaddress.ip_interface(c['ip']).network.broadcast_address] and ipaddress.ip_interface(c['ip']).ip not in [ipaddress.ip_interface(c['ip']).network.network_address,ipaddress.ip_interface(c['ip']).network.broadcast_address] for c in d['clients'])
    checks['2.4GHz plan 1 6 11']=set(d['ap_channels'])=={1,6,11}
    checks['CAPWAP control and local data']=d['capwap_control_udp']==5246 and d['ap_mode']=='FlexConnect' and d['local_switching'] is True
    checks['guest isolation']=d['guest_to_staff_permitted'] is False
    detail={'staff_vlan':wl['Staff']['vlan'],'radio_channels':d['ap_channels'],'data_path':'local site switching'}
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
        mutated['capwap_control_udp']=5247
        assert not accepted(mutated), 'corrupted control must fail'
        mutated=copy.deepcopy(good)
        mutated['clients'][0]['gateway']='10.10.20.255'
        assert not accepted(mutated), 'invalid scope/address must fail'
        mutated=copy.deepcopy(good)
        mutated['clients']=[]
        assert not accepted(mutated), 'invalid scope/address must fail'
        print('PASS | corrected, faulty and independent corrupted-control cases tested'); sys.exit(0)
    sys.exit(run(sys.argv[1] if len(sys.argv)>1 else ROOT/'case.json'))
