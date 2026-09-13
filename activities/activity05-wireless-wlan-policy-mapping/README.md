# Activity 05: Wireless WLAN and policy mapping

Tertiary Infotech Academy Pte Ltd | TGS-2023037854 | v7.0 | 90 minutes

## Goal

Connect SSID, authentication, VLAN and client addressing while inspecting RF channel and WLC data-path choices.

## Before you start

Cisco Packet Tracer for the compulsory core simulation, Python 3.9+, a text editor and this entire folder. Offline checkers need no pip installation, Internet access or real credentials. Use the exact device models, cabling and baseline configurations below. Separately labelled advanced extensions may require CML/IOS XE or remain evidence-only on unsupported PT models. Keep case.json as your working fixture; faulty.json resets it. reference.json is corrected synthetic evidence for self-study. The simulator uses the stated campus addresses; offline fixtures are independent documentation-address cases and do not connect to the simulator.

## Detailed procedure

### 1. Construct and save the mandatory simulator topology (11 minutes)

Start Cisco Packet Tracer 8.x or a current compatible version. File > New; use the bottom device palette, drag these models into the workspace and rename them via Config > Display Name: 1 x Wireless Router WRT300N (W1), 1 x PC-PT (ADMIN), 2 x Laptop-PT (L1,L2). Choose Connections > Copper Straight-Through for the table unless otherwise stated. Switch-to-switch links use Copper Cross-Over or Automatically Choose Connection Type. Click the first device and select its named interface; click the peer and select its named interface. Wait for links to initialize. Save as activity-start.pkt.

| Device/port A | Device/port B | Cable |
|---|---|---|
| ADMIN FastEthernet0 | W1 Ethernet1 | Straight-through |
| L1 Wireless0 | W1 radio | 802.11 association |
| L2 Wireless0 | W1 radio | 802.11 association |

```text
Save both activity-start.pkt and a working activity-working.pkt; use File > Save As.
```

### 2. Assign endpoint addresses and inspect interface identifiers (9 minutes)

ADMIN Desktop > IP Configuration > Static: 192.168.20.10/24, gateway 192.168.20.1. Configure W1 first from its Config/GUI tab; the factory default is often 192.168.0.1 so use direct device GUI. W1 GUI > Setup > Basic Setup: Local IP 192.168.20.1, mask 255.255.255.0, DHCP Enable, start 192.168.20.100, maximum50. Save Settings. In each laptop Physical tab switch power off, remove wired module if present, insert WPC300N wireless module, power on.

For routers/switches open CLI. Answer no to the initial configuration dialog and press Enter. Use the exact interface names below; a 2911 uses GigabitEthernet0/0 through 0/2, a 2960/3560 uses FastEthernet0/1 through 0/24 and GigabitEthernet0/1 through 0/2.

```text
W1 > GUI > Setup / Wireless; laptop > Desktop > PC Wireless / IP Configuration
```

### 3. Install all peer baseline configurations (24 minutes)

Configure W1 through its GUI using the exact values in the address and traffic-test steps. There is no IOS CLI on WRT300N. Set SSID CCNA-Staff/channel6 and WPA2-Personal/AES before attempting associations; Save Settings after each screen. Complete DHCP leases and healthy pings before saving the baseline .pkt file.

```text
Save Settings on W1; capture laptop association and DHCP results; save configured topology.
```

### 4. Prove the healthy baseline with actual packets (11 minutes)

Run every test below before introducing the fault. PC/Desktop > Command Prompt provides ping, ipconfig and arp. Use Simulation mode and Edit Filters to keep ARP, ICMP and the protocol under study; click Add Simple PDU for a ping and Capture/Forward to inspect hops. The first ping may lose one packet during ARP; repeat and record the second result. Do not mark a test passed until observed.

W1 GUI > Wireless > Basic Wireless Settings: SSID CCNA-Staff, channel6; Save Settings. Wireless Security: WPA2 Personal, AES, create a training-only passphrase of at least12 characters; Save Settings. On each laptop Desktop > PC Wireless > Connect choose CCNA-Staff and enter that phrase; Desktop > IP Configuration > DHCP. Expect 192.168.20.100+ leases with gateway192.168.20.1. L1/L2 ping 192.168.20.1 and ADMIN192.168.20.10 should succeed. Wrong PSK association must fail. Capture SSID/security/channel and DHCP evidence without showing the passphrase.

After all healthy tests pass, File > Save As > activity-start.pkt to preserve the CONFIGURED healthy baseline, then File > Save As > activity-working.pkt before introducing the fault. The initial empty construction is not the rollback baseline.

```text
Save baseline screenshots / CLI text with device names; File > Save.
```

### 5. Introduce and diagnose the controlled fault (11 minutes)

Save the baseline first. Apply only the following fault to the specified device. Repeat the same traffic tests, capture the first failing hop/control and compare show output with the healthy baseline.

W1 GUI > Wireless > Wireless Security: change the configured WPA2-Personal passphrase to a different training-only value while leaving the old value on L2. Save Settings. L2 loses association/traffic; L1 must be reconnected with the new phrase to remain healthy. Inspect association before changing IP settings.

```text
Retain activity-start.pkt and baseline running configurations; work in activity-working.pkt.
```

### 6. Apply the narrow repair and re-test the network (11 minutes)

Restore the original exercise passphrase on W1 and reconnect both laptops. Do not place it in course submissions/screenshots. Keep WPA2/AES enabled; do not repair by disabling authentication.

Repeat the baseline test matrix. Check surrounding controls as well as the repaired flow. the difference between PSK association failure, DHCP failure and a routed policy denial

```text
Save actual show output and allowed/denied traffic results; copy running-config startup-config only after successful verification.
```

### 7. Rollback and rehearse recovery (5 minutes)

Save the repaired file as activity-verified.pkt. To undo the exercise, open the saved healthy baseline activity-start.pkt after you have saved configurations into it at Step 3, or paste the saved pre-fault running configuration into a clean topology. For the specific repair, retain the exact old command/value rather than guessing a trunk list or ACL. Repeat one positive and one relevant negative test after recovery.

```text
File > Save As > activity-verified.pkt; close working topology; reopen saved healthy baseline.
```

### 8. Submit observed evidence and explain the forwarding mechanism (5 minutes)

Submit the verified .pkt file, a cabling/address table, pre-fault and post-repair show outputs, screenshots of traffic tests, diagnosis and rollback notes. Explain the difference between PSK association failure, DHCP failure and a routed policy denial Keep synthetic checker output separate from real simulator observations.

```text
Record simulator version, device models and tests actually completed.
```

### 9. Complete the separately labelled extension (3 minutes)

Mandatory core WPA2-PSK GUI exercise above covers current v1.1 WLAN configuration. Then inspect the supplied Staff WPA2-Enterprise/802.1X versus Guest PSK fixture. For WLAN-to-VLAN policy use a PT WLC-2504, two lightweight3702i APs, 3560 switch and AAA/DHCP Server-PT if supported: keep the WLC/AP/AAA in a management VLAN, create Staff VLAN20 and Guest VLAN30 at the switch, map Staff WLAN to VLAN20 and Guest WLAN to VLAN30, and point Staff802.1X to the AAA server. IOS XE/CML/controller GUI names vary, so this advanced mapping extension requires trainer-provided platform baseline. Export actual policy/client VLAN evidence or mark evidence-only; no enterprise deployment is claimed by the WRT300N core exercise.

```text
Record supported platform, output observed or evidence-only limitation.
```

## Untimed appendix: independent fixture analysis

These independent synthetic cases supplement the allocated hands-on time. They do not configure the simulator.

### Appendix 1. Establish the baseline

Open activity05-wireless-wlan-policy-mapping; inspect topology.md, case.json and observations.csv. Identify the controls for: Connect SSID, authentication, VLAN and client addressing while inspecting RF channel and WLC data-path choices.

```text
python3 --version
```

### Appendix 2. Run the faulty evidence case

Run the checker against case.json; exit status 1 is expected at this stage. Record each FAIL label and the calculated detail.

```text
python3 checker.py case.json
```

### Appendix 3. Propose the repair

Restore Staff VLAN 20 and WPA2-Enterprise; set channels [1,6,11] for this 2.4GHz example, and guest_to_staff_permitted false. An actual RF plan requires a survey and regulatory-domain support.

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
  "staff_vlan": 20,
  "radio_channels": [
    1,
    6,
    11
  ],
  "data_path": "local site switching"
}
```

Required PASS controls:

- staff enterprise and VLAN20
- clients match WLAN subnet
- 2.4GHz plan 1 6 11
- CAPWAP control and local data
- guest isolation

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
