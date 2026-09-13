# Activity 08: NAT DHCP DNS and time

Tertiary Infotech Academy Pte Ltd | TGS-2023037854 | v7.0 | 100 minutes

## Goal

Correlate translated transport tuples, DHCP scope options, DNS records and synchronized logging.

## Before you start

Cisco Packet Tracer for the compulsory core simulation, Python 3.9+, a text editor and this entire folder. Offline checkers need no pip installation, Internet access or real credentials. Use the exact device models, cabling and baseline configurations below. Separately labelled advanced extensions may require CML/IOS XE or remain evidence-only on unsupported PT models. Keep case.json as your working fixture; faulty.json resets it. reference.json is corrected synthetic evidence for self-study. The simulator uses the stated campus addresses; offline fixtures are independent documentation-address cases and do not connect to the simulator.

## Detailed procedure

### 1. Construct and save the mandatory simulator topology (12 minutes)

Start Cisco Packet Tracer 8.x or a current compatible version. File > New; use the bottom device palette, drag these models into the workspace and rename them via Config > Display Name: 2 x Router2911 (R1,R2), 2 x Switch2960 (S1,S2), 1 x PC-PT (PC1), 1 x Server-PT (SRV). Choose Connections > Copper Straight-Through for the table unless otherwise stated. Switch-to-switch links use Copper Cross-Over or Automatically Choose Connection Type. Click the first device and select its named interface; click the peer and select its named interface. Wait for links to initialize. Save as activity-start.pkt.

| Device/port A | Device/port B | Cable |
|---|---|---|
| PC1 FastEthernet0 | S1 FastEthernet0/1 | Straight-through |
| S1 FastEthernet0/24 | R1 GigabitEthernet0/0 | Straight-through |
| R1 GigabitEthernet0/1 | R2 GigabitEthernet0/1 | Cross-over/Auto |
| R2 GigabitEthernet0/0 | S2 FastEthernet0/24 | Straight-through |
| S2 FastEthernet0/1 | SRV FastEthernet0 | Straight-through |

```text
Save both activity-start.pkt and a working activity-working.pkt; use File > Save As.
```

### 2. Assign endpoint addresses and inspect interface identifiers (10 minutes)

Set Desktop > IP Configuration > Static on each endpoint.

| Endpoint | Address | Mask | Gateway | DNS |
|---|---|---|---|---|
| PC1 | DHCP | DHCP | DHCP option | DHCP option |
| SRV | 192.0.2.50 | 255.255.255.0 | 192.0.2.1 | 192.0.2.50 |

SRV Services > HTTP: HTTP On and HTTPS On if offered. DNS On; add A record app.example.test ->192.0.2.50. NTP On if available (no authentication for this isolated exercise). PC1 gets DHCP from R1; do not enable a competing SRV DHCP scope.

For routers/switches open CLI. Answer no to the initial configuration dialog and press Enter. Use the exact interface names below; a 2911 uses GigabitEthernet0/0 through 0/2, a 2960/3560 uses FastEthernet0/1 through 0/24 and GigabitEthernet0/1 through 0/2.

```text
enable
show ip interface brief
```

### 3. Install all peer baseline configurations (26 minutes)

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
interface GigabitEthernet0/0
 ip nat inside
exit
interface GigabitEthernet0/1
 ip nat outside
exit
ip dhcp excluded-address 10.10.10.1 10.10.10.20
ip dhcp pool USERS
 network 10.10.10.0 255.255.255.0
 default-router 10.10.10.1
 dns-server 192.0.2.50
exit
access-list 1 permit 10.10.10.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/1 overload
ip route 0.0.0.0 0.0.0.0 10.0.0.2
ntp server 192.0.2.50
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
 ip address 192.0.2.1 255.255.255.0
 no shutdown
exit
interface GigabitEthernet0/1
 ip address 10.0.0.2 255.255.255.252
 no shutdown
exit
ip route 10.10.10.0 255.255.255.0 10.0.0.1
end
copy running-config startup-config
```

```text
show running-config
show ip interface brief
copy running-config startup-config
```

### 4. Prove the healthy baseline with actual packets (12 minutes)

Run every test below before introducing the fault. PC/Desktop > Command Prompt provides ping, ipconfig and arp. Use Simulation mode and Edit Filters to keep ARP, ICMP and the protocol under study; click Add Simple PDU for a ping and Capture/Forward to inspect hops. The first ping may lose one packet during ARP; repeat and record the second result. Do not mark a test passed until observed.

PC1 ipconfig shows10.10.10.21+ /24 gateway10.10.10.1 DNS192.0.2.50. PC1 ping 192.0.2.50 succeeds. Browser http://app.example.test returns the PT server page. R1 show ip dhcp binding shows the leased client; show ip nat translations during traffic shows inside local10.10.10.x mapped to inside global10.0.0.1; show ntp associations/status should show synchronized peer if the PT NTP model supports it. In Simulation inspect DHCP DORA, DNS question/answer and NAT address rewrite.

After all healthy tests pass, File > Save As > activity-start.pkt to preserve the CONFIGURED healthy baseline, then File > Save As > activity-working.pkt before introducing the fault. The initial empty construction is not the rollback baseline.

```text
Save baseline screenshots / CLI text with device names; File > Save.
```

### 5. Introduce and diagnose the controlled fault (12 minutes)

Save the baseline first. Apply only the following fault to the specified device. Repeat the same traffic tests, capture the first failing hop/control and compare show output with the healthy baseline.

On R1 DHCP pool USERS change dns-server 192.0.2.99. PC1 Desktop > IP Configuration select Static then DHCP to request a new lease. PC1 ping 192.0.2.50 succeeds but Web Browser http://app.example.test fails. Preserve that IP-versus-name difference. Restore DNS then remove R1 ip nat inside from Gi0/0 and inspect missing translations during fresh HTTP sessions; return routing may permit traffic without NAT in this private sandbox, so NAT failure is proven by translation absence, not by assuming ping always fails.

```text
Retain activity-start.pkt and baseline running configurations; work in activity-working.pkt.
```

### 6. Apply the narrow repair and re-test the network (12 minutes)

Restore R1 pool DNS to192.0.2.50 and renew the lease. Restore ip nat inside on Gi0/0. Create new traffic and inspect the translation tuple rather than relying on old entries.

Repeat the baseline test matrix. Check surrounding controls as well as the repaired flow. why a successful ping by address cannot prove DNS, HTTP, synchronized time or NAT translation

```text
Save actual show output and allowed/denied traffic results; copy running-config startup-config only after successful verification.
```

### 7. Rollback and rehearse recovery (6 minutes)

Save the repaired file as activity-verified.pkt. To undo the exercise, open the saved healthy baseline activity-start.pkt after you have saved configurations into it at Step 3, or paste the saved pre-fault running configuration into a clean topology. For the specific repair, retain the exact old command/value rather than guessing a trunk list or ACL. Repeat one positive and one relevant negative test after recovery.

```text
File > Save As > activity-verified.pkt; close working topology; reopen saved healthy baseline.
```

### 8. Submit observed evidence and explain the forwarding mechanism (6 minutes)

Submit the verified .pkt file, a cabling/address table, pre-fault and post-repair show outputs, screenshots of traffic tests, diagnosis and rollback notes. Explain why a successful ping by address cannot prove DNS, HTTP, synchronized time or NAT translation Keep synthetic checker output separate from real simulator observations.

```text
Record simulator version, device models and tests actually completed.
```

### 9. Complete the separately labelled extension (4 minutes)

DNS MX/NS/PTR and SFTP/SCP are transition extensions: PT DNS often supports only A/CNAME. Use the supplied record fixtures for MX preference and reverse names. checker.py calculates a genuine local SHA-256 of transfer-copy.cfg; alter one character and observe rejection, then restore. A real SCP/SFTP transfer requires SSH-capable IOS XE/CML plus a trainer-owned file server; no real transfer is claimed by the local hash test.

```text
Record supported platform, output observed or evidence-only limitation.
```

## Untimed appendix: independent fixture analysis

These independent synthetic cases supplement the allocated hands-on time. They do not configure the simulator.

### Appendix 1. Establish the baseline

Open activity08-nat-dhcp-dns-time; inspect topology.md, case.json and observations.csv. Identify the controls for: Correlate translated transport tuples, DHCP scope options, DNS records and synchronized logging.

```text
python3 --version
```

### Appendix 2. Run the faulty evidence case

Run the checker against case.json; exit status 1 is expected at this stage. Record each FAIL label and the calculated detail.

```text
python3 checker.py case.json
```

### Appendix 3. Propose the repair

Make translated ports unique by setting the second global_port to 30002; restore DHCP gateway 10.10.10.1; set synchronized true and offset_ms 2. Verify the raw translation fields before concluding NAT succeeds.

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
  "PAT_global_tuples": [
    [
      "203.0.113.2",
      30001,
      "tcp"
    ],
    [
      "203.0.113.2",
      30002,
      "tcp"
    ]
  ],
  "DHCP_network": "10.10.10.0/24",
  "DNS_record_types": [
    "A",
    "AAAA",
    "MX",
    "NS",
    "PTR"
  ],
  "offset_ms": 2
}
```

Required PASS controls:

- PAT tuple disambiguation
- DHCP scope and options
- DNS forward and refresh records
- NTP selected synchronized source
- secure transfer integrity

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

Refresh extension: inspect MX preference, NS authority and reverse PTR names; compare SSH-based SCP/SFTP with unauthenticated TFTP. The checker calculates the real SHA-256 of transfer-copy.cfg and compares it with the fixture digests; this proves local file integrity only, not an actual network transfer.

## References

Cisco CCNA v1.1 exam topics: https://learningcontent.cisco.com/documents/marketing/exam-topics/200-301-CCNA-v1.1.pdf
Cisco IOS XE configuration guides: https://www.cisco.com/c/en/us/support/ios-nx-os-software/ios-xe/products-installation-and-configuration-guides-list.html
Python ipaddress: https://docs.python.org/3/library/ipaddress.html
