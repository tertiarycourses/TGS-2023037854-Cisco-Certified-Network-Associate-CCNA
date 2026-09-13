# Activity 07: OSPF and gateway failover

Tertiary Infotech Academy Pte Ltd | TGS-2023037854 | v7.0 | 120 minutes

## Goal

Diagnose OSPF adjacency, path costs and a virtual gateway; distinguish current v1.1 FHRP explanation from refresh practice.

## Before you start

Cisco Packet Tracer for the compulsory core simulation, Python 3.9+, a text editor and this entire folder. Offline checkers need no pip installation, Internet access or real credentials. Use the exact device models, cabling and baseline configurations below. Separately labelled advanced extensions may require CML/IOS XE or remain evidence-only on unsupported PT models. Keep case.json as your working fixture; faulty.json resets it. reference.json is corrected synthetic evidence for self-study. The simulator uses the stated campus addresses; offline fixtures are independent documentation-address cases and do not connect to the simulator.

## Detailed procedure

### 1. Construct and save the mandatory simulator topology (15 minutes)

Start Cisco Packet Tracer 8.x or a current compatible version. File > New; use the bottom device palette, drag these models into the workspace and rename them via Config > Display Name: 3 x Router2911 (R1,R2,R3), 2 x Switch2960 (S1,S2), 2 x PC-PT (PC1,PC2). Choose Connections > Copper Straight-Through for the table unless otherwise stated. Switch-to-switch links use Copper Cross-Over or Automatically Choose Connection Type. Click the first device and select its named interface; click the peer and select its named interface. Wait for links to initialize. Save as activity-start.pkt.

| Device/port A | Device/port B | Cable |
|---|---|---|
| PC1 FastEthernet0 | S1 FastEthernet0/1 | Straight-through |
| S1 FastEthernet0/24 | R1 GigabitEthernet0/0 | Straight-through |
| R1 GigabitEthernet0/1 | R2 GigabitEthernet0/1 | Cross-over/Auto |
| R2 GigabitEthernet0/0 | S2 FastEthernet0/24 | Straight-through |
| S2 FastEthernet0/1 | PC2 FastEthernet0 | Straight-through |
| S1 FastEthernet0/23 | R3 GigabitEthernet0/0 | Straight-through |
| R2 GigabitEthernet0/2 | R3 GigabitEthernet0/1 | Cross-over/Auto |

```text
Save both activity-start.pkt and a working activity-working.pkt; use File > Save As.
```

### 2. Assign endpoint addresses and inspect interface identifiers (12 minutes)

Set Desktop > IP Configuration > Static on each endpoint.

| Endpoint | Address | Mask | Gateway | DNS |
|---|---|---|---|---|
| PC1 | 10.10.10.10 | 255.255.255.0 | 10.10.10.254 | none |
| PC2 | 10.10.20.20 | 255.255.255.0 | 10.10.20.1 | none |

For routers/switches open CLI. Answer no to the initial configuration dialog and press Enter. Use the exact interface names below; a 2911 uses GigabitEthernet0/0 through 0/2, a 2960/3560 uses FastEthernet0/1 through 0/24 and GigabitEthernet0/1 through 0/2.

```text
enable
show ip interface brief
```

### 3. Install all peer baseline configurations (29 minutes)

Paste the following device-specific blocks into each named device CLI one device at a time. Wait for the router/switch prompt between blocks. These are complete activity configurations for the stated construction. Do not apply configuration from a different activity. When copy asks for Destination filename, press Enter. Save the Packet Tracer working file after all blocks.

Device S1
```text
enable
configure terminal
hostname S1
no ip domain-lookup
interface range FastEthernet0/1,FastEthernet0/24
 switchport mode access
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
interface range FastEthernet0/1,FastEthernet0/24
 switchport mode access
 no shutdown
exit
end
copy running-config startup-config
```

Device R1
```text
enable
configure terminal
hostname R1
no ip domain-lookup
interface GigabitEthernet0/0
 ip address 10.10.10.1 255.255.255.0
 no shutdown
exit
interface GigabitEthernet0/1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
exit
router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.0.3 area 0
 network 10.10.10.0 0.0.0.255 area 0
 passive-interface GigabitEthernet0/0
exit
interface GigabitEthernet0/0
 standby 10 ip 10.10.10.254
 standby 10 priority 110
 standby 10 preempt
exit
end
copy running-config startup-config
```

Device R2
```text
enable
configure terminal
hostname R2
no ip domain-lookup
interface GigabitEthernet0/0
 ip address 10.10.20.1 255.255.255.0
 no shutdown
exit
interface GigabitEthernet0/1
 ip address 10.0.0.2 255.255.255.252
 no shutdown
exit
router ospf 1
 router-id 2.2.2.2
 network 10.0.0.0 0.0.0.3 area 0
 network 10.10.20.0 0.0.0.255 area 0
 passive-interface GigabitEthernet0/0
exit
interface GigabitEthernet0/2
 ip address 10.0.0.5 255.255.255.252
 no shutdown
exit
router ospf 1
 network 10.0.0.4 0.0.0.3 area 0
exit
end
copy running-config startup-config
```

Device R3
```text
enable
configure terminal
hostname R3
no ip domain-lookup
interface GigabitEthernet0/0
 ip address 10.10.10.3 255.255.255.0
 standby 10 ip 10.10.10.254
 standby 10 priority 100
 standby 10 preempt
 no shutdown
exit
interface GigabitEthernet0/1
 ip address 10.0.0.6 255.255.255.252
 no shutdown
exit
router ospf 1
 router-id 3.3.3.3
 network 10.10.10.0 0.0.0.255 area 0
 network 10.0.0.4 0.0.0.3 area 0
 passive-interface GigabitEthernet0/0
exit
end
copy running-config startup-config
```

```text
show running-config
show ip interface brief
copy running-config startup-config
```

### 4. Prove the healthy baseline with actual packets (15 minutes)

Run every test below before introducing the fault. PC/Desktop > Command Prompt provides ping, ipconfig and arp. Use Simulation mode and Edit Filters to keep ARP, ICMP and the protocol under study; click Add Simple PDU for a ping and Capture/Forward to inspect hops. The first ping may lose one packet during ARP; repeat and record the second result. Do not mark a test passed until observed.

R1/R2 show ip ospf neighbor: FULL adjacency on Gi0/1; R2/R3 FULL on their transit link. R1 show ip route ospf includes 10.10.20.0/24; R2 learns10.10.10.0/24 through equal advertised LAN paths according to cost. show standby brief: R1 Active, R3 Standby, VIP10.10.10.254. PC1 ping 10.10.20.20 succeeds. After R1 isolation R3 Active and PC1 remote ping recovers using unchanged gateway. Capture before/failure/recovery route and HSRP outputs.

After all healthy tests pass, File > Save As > activity-start.pkt to preserve the CONFIGURED healthy baseline, then File > Save As > activity-working.pkt before introducing the fault. The initial empty construction is not the rollback baseline.

```text
Save baseline screenshots / CLI text with device names; File > Save.
```

### 5. Introduce and diagnose the controlled fault (15 minutes)

Save the baseline first. Apply only the following fault to the specified device. Repeat the same traffic tests, capture the first failing hop/control and compare show output with the healthy baseline.

On R2 Gi0/1 set ip ospf hello-interval 5 and ip ospf dead-interval 20. Wait past the old dead timer; R1/R2 adjacency disappears. Restore timers. Next shut BOTH R1 Gi0/0 and Gi0/1 to simulate router isolation; R3 takes virtual gateway ownership and has an independent route through R2.

```text
Retain activity-start.pkt and baseline running configurations; work in activity-working.pkt.
```

### 6. Apply the narrow repair and re-test the network (15 minutes)

Restore R2 Gi0/1: ip ospf hello-interval 10; ip ospf dead-interval 40. Restore both R1 interfaces with no shutdown. Preempt lets R1 retake HSRP ownership after recovery; observe actual timing rather than assuming instant failover.

Repeat the baseline test matrix. Check surrounding controls as well as the repaired flow. how OSPF route convergence and HSRP virtual-gateway transfer are different mechanisms

```text
Save actual show output and allowed/denied traffic results; copy running-config startup-config only after successful verification.
```

### 7. Rollback and rehearse recovery (7 minutes)

Save the repaired file as activity-verified.pkt. To undo the exercise, open the saved healthy baseline activity-start.pkt after you have saved configurations into it at Step 3, or paste the saved pre-fault running configuration into a clean topology. For the specific repair, retain the exact old command/value rather than guessing a trunk list or ACL. Repeat one positive and one relevant negative test after recovery.

```text
File > Save As > activity-verified.pkt; close working topology; reopen saved healthy baseline.
```

### 8. Submit observed evidence and explain the forwarding mechanism (7 minutes)

Submit the verified .pkt file, a cabling/address table, pre-fault and post-repair show outputs, screenshots of traffic tests, diagnosis and rollback notes. Explain how OSPF route convergence and HSRP virtual-gateway transfer are different mechanisms Keep synthetic checker output separate from real simulator observations.

```text
Record simulator version, device models and tests actually completed.
```

### 9. Complete the separately labelled extension (5 minutes)

Current v1.1 core configures OSPFv2 and explains FHRP; the HSRP hands-on deepens that explanation. OSPFv3 and VRRP transition fixtures are evidence-only when PT lacks support. On a supported IOS XE/CML platform create a separate copy, replace OSPFv2 with IPv6 OSPFv3 and replace HSRP with VRRP; do not run both FHRPs on the same VIP. Use specimen.cfg for syntax examples and record the exact supported version.

```text
Record supported platform, output observed or evidence-only limitation.
```

## Untimed appendix: independent fixture analysis

These independent synthetic cases supplement the allocated hands-on time. They do not configure the simulator.

### Appendix 1. Establish the baseline

Open activity07-ospf-gateway-failover; inspect topology.md, case.json and observations.csv. Identify the controls for: Diagnose OSPF adjacency, path costs and a virtual gateway; distinguish current v1.1 FHRP explanation from refresh practice.

```text
python3 --version
```

### Appendix 2. Run the faulty evidence case

Run the checker against case.json; exit status 1 is expected at this stage. Record each FAIL label and the calculated detail.

```text
python3 checker.py case.json
```

### Appendix 3. Propose the repair

Set peer hello/dead to 10/40 and state FULL in corrected evidence; set installed_next 10.0.0.2 because costs 20 and 30 are unequal. Keep host gateway .1 during ownership transfer.

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
  "path_costs": {
    "10.0.0.2": 20,
    "10.0.0.6": 30
  },
  "virtual_gateway": "10.10.10.1"
}
```

Required PASS controls:

- unique router IDs
- compatible adjacency
- lowest OSPF path cost
- single virtual gateway owner
- refresh OSPFv3 IPv6 adjacency
- refresh VRRP unique master

The checker calculates domain results instead of relying on a single success label. Inspect each PASS/FAIL control and JSON detail. Save evidence.txt, your corrected case.json, an incident explanation and any genuine sandbox show outputs with device/model/time.

## Troubleshooting

- Exit 1 means a control failed; read the specific label and repair one field at a time.
- Exit 2 means malformed evidence or a missing key; restore faulty.json to case.json and reapply edits with correct JSON types.
- Run from this folder or pass an absolute fixture path. The checker finds its own reference files for self-test.
- A CLI command rejected by a simulator is unsupported on that model; retain the limitation and do not fabricate output.
- A passing fixture with failed real traffic requires fresh device evidence; a JSON edit cannot repair a live network.

## Close and reset

Confirm each acceptance item in checklist.pdf. Restore simulator settings from the saved baseline or apply your reviewed rollback; preserve diagnostic evidence. To reset the offline exercise copy faulty.json over case.json.

## Transition practice

Refresh extension: OSPFv3 and VRRP are introduced for the announced 3 February 2027 transition. Current CCNA v1.1 requires single-area OSPFv2 configuration and an explanation of FHRP purpose; do not represent the extension as a current v1.1 configuration requirement.

## References

Cisco CCNA v1.1 exam topics: https://learningcontent.cisco.com/documents/marketing/exam-topics/200-301-CCNA-v1.1.pdf
Cisco IOS XE configuration guides: https://www.cisco.com/c/en/us/support/ios-nx-os-software/ios-xe/products-installation-and-configuration-guides-list.html
Python ipaddress: https://docs.python.org/3/library/ipaddress.html
