# Activity 04: EtherChannel and STP resilience

Tertiary Infotech Academy Pte Ltd | TGS-2023037854 | v7.0 | 100 minutes

## Goal

Check LACP negotiation and spanning-tree redundancy without confusing blocked paths with failed links.

## Before you start

Cisco Packet Tracer for the compulsory core simulation, Python 3.9+, a text editor and this entire folder. Offline checkers need no pip installation, Internet access or real credentials. Use the exact device models, cabling and baseline configurations below. Separately labelled advanced extensions may require CML/IOS XE or remain evidence-only on unsupported PT models. Keep case.json as your working fixture; faulty.json resets it. reference.json is corrected synthetic evidence for self-study. The simulator uses the stated campus addresses; offline fixtures are independent documentation-address cases and do not connect to the simulator.

## Detailed procedure

### 1. Construct and save the mandatory simulator topology (13 minutes)

Start Cisco Packet Tracer 8.x or a current compatible version. File > New; use the bottom device palette, drag these models into the workspace and rename them via Config > Display Name: 2 x Switch 2960 (S1,S2), 2 x PC-PT (PC1,PC2). Choose Connections > Copper Straight-Through for the table unless otherwise stated. Switch-to-switch links use Copper Cross-Over or Automatically Choose Connection Type. Click the first device and select its named interface; click the peer and select its named interface. Wait for links to initialize. Save as activity-start.pkt.

| Device/port A | Device/port B | Cable |
|---|---|---|
| PC1 FastEthernet0 | S1 FastEthernet0/1 | Straight-through |
| PC2 FastEthernet0 | S2 FastEthernet0/1 | Straight-through |
| S1 FastEthernet0/23 | S2 FastEthernet0/23 | Cross-over/Auto |
| S1 FastEthernet0/24 | S2 FastEthernet0/24 | Cross-over/Auto |
| S1 GigabitEthernet0/1 | S2 GigabitEthernet0/1 | Cross-over/Auto |

```text
Save both activity-start.pkt and a working activity-working.pkt; use File > Save As.
```

### 2. Assign endpoint addresses and inspect interface identifiers (10 minutes)

Set Desktop > IP Configuration > Static on each endpoint.

| Endpoint | Address | Mask | Gateway | DNS |
|---|---|---|---|---|
| PC1 | 10.10.10.10 | 255.255.255.0 | none | none |
| PC2 | 10.10.10.20 | 255.255.255.0 | none | none |

For routers/switches open CLI. Answer no to the initial configuration dialog and press Enter. Use the exact interface names below; a 2911 uses GigabitEthernet0/0 through 0/2, a 2960/3560 uses FastEthernet0/1 through 0/24 and GigabitEthernet0/1 through 0/2.

```text
enable
show ip interface brief
```

### 3. Install all peer baseline configurations (26 minutes)

Paste the complete corrected per-device blocks below, including the Po1 STP cost3 to prefer the channel over Gi0/1.

Device S1
```text
enable
configure terminal
hostname S1
no ip domain-lookup
vlan 10
spanning-tree mode rapid-pvst
spanning-tree vlan 10 priority 4096
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
exit
interface range FastEthernet0/23-24
 switchport mode trunk
 switchport trunk allowed vlan 10
 channel-group 1 mode active
 no shutdown
exit
interface Port-channel1
 spanning-tree vlan 10 cost 3
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
exit
end
copy running-config startup-config
```

Device S2
```text
enable
configure terminal
hostname S2
no ip domain-lookup
vlan 10
spanning-tree mode rapid-pvst
spanning-tree vlan 10 priority 8192
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
exit
interface range FastEthernet0/23-24
 switchport mode trunk
 switchport trunk allowed vlan 10
 channel-group 1 mode passive
 no shutdown
exit
interface Port-channel1
 spanning-tree vlan 10 cost 3
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
exit
end
copy running-config startup-config
```

```text
show running-config
show ip interface brief
copy running-config startup-config
```

### 4. Prove the healthy baseline with actual packets (13 minutes)

Run every test below before introducing the fault. PC/Desktop > Command Prompt provides ping, ipconfig and arp. Use Simulation mode and Edit Filters to keep ARP, ICMP and the protocol under study; click Add Simple PDU for a ping and Capture/Forward to inspect hops. The first ping may lose one packet during ARP; repeat and record the second result. Do not mark a test passed until observed.

S1/S2 show etherchannel summary: Po1(SU), both Fa0/23 and Fa0/24 show (P). show spanning-tree vlan 10: S1 is root. The configured Po1 STP cost3 is lower than Gi0/1 cost4. Therefore S2 Po1 root forwarding, Gi0/1 alternate. PC1 ping PC2 succeeds. After Po1 shutdown Gi0/1 becomes forwarding. Measure actual simulated interruption; offline 2.1s is a synthetic example, not your measured result.

After all healthy tests pass, File > Save As > activity-start.pkt to preserve the CONFIGURED healthy baseline, then File > Save As > activity-working.pkt before introducing the fault. The initial empty construction is not the rollback baseline.

```text
Save baseline screenshots / CLI text with device names; File > Save.
```

### 5. Introduce and diagnose the controlled fault (13 minutes)

Save the baseline first. Apply only the following fault to the specified device. Repeat the same traffic tests, capture the first failing hop/control and compare show output with the healthy baseline.

After capturing baseline, shut S1 Port-channel1:
```text
enable
configure terminal
interface Port-channel1
 shutdown
end
```
Repeat ping while RSTP reconverges; inspect the Gi0/1 alternate becoming forwarding. Restore Port-channel1 before the next fault. For LACP initiation failure, remove channel-group 1 from S1 Fa0/23-24 and recreate it mode passive; with S2 passive, no bundled LACP channel should form.

```text
Retain activity-start.pkt and baseline running configurations; work in activity-working.pkt.
```

### 6. Apply the narrow repair and re-test the network (13 minutes)

S1: configure terminal; interface Port-channel1; no shutdown; exit; interface range FastEthernet0/23-24; no channel-group 1; channel-group 1 mode active; end. If old membership exists remove it before changing mode. Keep S2 passive.

Repeat the baseline test matrix. Check surrounding controls as well as the repaired flow. why LACP needs at least one active peer and STP treats a correctly bundled channel as one logical link

```text
Save actual show output and allowed/denied traffic results; copy running-config startup-config only after successful verification.
```

### 7. Rollback and rehearse recovery (6 minutes)

Save the repaired file as activity-verified.pkt. To undo the exercise, open the saved healthy baseline activity-start.pkt after you have saved configurations into it at Step 3, or paste the saved pre-fault running configuration into a clean topology. For the specific repair, retain the exact old command/value rather than guessing a trunk list or ACL. Repeat one positive and one relevant negative test after recovery.

```text
File > Save As > activity-verified.pkt; close working topology; reopen saved healthy baseline.
```

### 8. Submit observed evidence and explain the forwarding mechanism (6 minutes)

Submit the verified .pkt file, a cabling/address table, pre-fault and post-repair show outputs, screenshots of traffic tests, diagnosis and rollback notes. Explain why LACP needs at least one active peer and STP treats a correctly bundled channel as one logical link Keep synthetic checker output separate from real simulator observations.

```text
Record simulator version, device models and tests actually completed.
```

## Untimed appendix: independent fixture analysis

These independent synthetic cases supplement the allocated hands-on time. They do not configure the simulator.

### Appendix 1. Establish the baseline

Open activity04-etherchannel-stp-resilience; inspect topology.md, case.json and observations.csv. Identify the controls for: Check LACP negotiation and spanning-tree redundancy without confusing blocked paths with failed links.

```text
python3 --version
```

### Appendix 2. Run the faulty evidence case

Run the checker against case.json; exit status 1 is expected at this stage. Record each FAIL label and the calculated detail.

```text
python3 checker.py case.json
```

### Appendix 3. Propose the repair

Use active/passive or active/active LACP. Set both members to speed 1000 and VLAN signature 10,20,99; set bundled true only for the corrected synthetic evidence. Explain why passive/passive never initiates negotiation.

```text
Open case.json in a plain text editor; preserve JSON types.
```

### Appendix 4. Validate the corrected case

Save a separate working copy first. Run the checker after each narrow edit until all controls PASS; capture output as evidence. This validates fixtures only.

```text
python3 checker.py case.json > evidence.txt
```

### Appendix 5. Verify checker behavior

Run self-test; it must accept corrected reference evidence and reject the faulty fixture and the independent corrupted-control test.

```text
python3 checker.py --self-test
```

## Expected evidence

Corrected reference: all checks PASS, exit 0; faulty fixture: one or more FAIL, exit 1; self-test: PASS, exit 0. Domain-specific computed fields appear in JSON detail.

Calculated corrected-fixture results:

```json
{
  "calculated_root": "DIST1",
  "convergence_seconds": 2.1
}
```

Required PASS controls:

- LACP initiation
- channel member consistency
- intended STP root
- one redundant alternate
- alternate takes over within budget

The checker calculates domain results instead of relying on a single success label. Inspect each PASS/FAIL control and JSON detail. Save evidence.txt, your corrected case.json, an incident explanation and any genuine sandbox show outputs with device/model/time.

## Troubleshooting

- Exit 1 means a control failed; read the specific label and repair one field at a time.
- Exit 2 means malformed evidence or a missing key; restore faulty.json to case.json and reapply edits with correct JSON types.
- Run from this folder or pass an absolute fixture path. The checker finds its own reference files for self-test.
- A CLI command rejected by a simulator is unsupported on that model; retain the limitation and do not fabricate output.
- A passing fixture with failed real traffic requires fresh device evidence; a JSON edit cannot repair a live network.

## Close and reset

Confirm each acceptance item in checklist.pdf. Restore simulator settings from the saved baseline or apply your reviewed rollback; preserve diagnostic evidence. To reset the offline exercise copy faulty.json over case.json.

## References

Cisco CCNA v1.1 exam topics: https://learningcontent.cisco.com/documents/marketing/exam-topics/200-301-CCNA-v1.1.pdf
Cisco IOS XE configuration guides: https://www.cisco.com/c/en/us/support/ios-nx-os-software/ios-xe/products-installation-and-configuration-guides-list.html
Python ipaddress: https://docs.python.org/3/library/ipaddress.html
