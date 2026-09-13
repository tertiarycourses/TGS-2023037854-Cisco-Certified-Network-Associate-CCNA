# Activity 11: REST JSON and configuration automation

Tertiary Infotech Academy Pte Ltd | TGS-2023037854 | v7.0 | 80 minutes

## Goal

Validate REST status and JSON types, produce an idempotent plan and select a bounded agentic AI prompt.

## Before you start

Cisco Packet Tracer for the compulsory core simulation, Python 3.9+, a text editor and this entire folder. Offline checkers need no pip installation, Internet access or real credentials. Use the exact device models, cabling and baseline configurations below. Separately labelled advanced extensions may require CML/IOS XE or remain evidence-only on unsupported PT models. Keep case.json as your working fixture; faulty.json resets it. reference.json is corrected synthetic evidence for self-study. The simulator uses the stated campus addresses; offline fixtures are independent documentation-address cases and do not connect to the simulator.

## Detailed procedure

### 1. Construct and save the mandatory simulator topology (10 minutes)

Start Cisco Packet Tracer 8.x or a current compatible version. File > New; use the bottom device palette, drag these models into the workspace and rename them via Config > Display Name: 1 x Router2911 (R1), 1 x Switch2960 (S1), 1 x PC-PT (PC1). Choose Connections > Copper Straight-Through for the table unless otherwise stated. Switch-to-switch links use Copper Cross-Over or Automatically Choose Connection Type. Click the first device and select its named interface; click the peer and select its named interface. Wait for links to initialize. Save as activity-start.pkt.

| Device/port A | Device/port B | Cable |
|---|---|---|
| PC1 FastEthernet0 | S1 FastEthernet0/1 | Straight-through |
| S1 FastEthernet0/24 | R1 GigabitEthernet0/0 | Straight-through |

```text
Save both activity-start.pkt and a working activity-working.pkt; use File > Save As.
```

### 2. Assign endpoint addresses and inspect interface identifiers (8 minutes)

Set Desktop > IP Configuration > Static on each endpoint.

| Endpoint | Address | Mask | Gateway | DNS |
|---|---|---|---|---|
| PC1 | 10.10.10.10 | 255.255.255.0 | 10.10.10.1 | none |

For routers/switches open CLI. Answer no to the initial configuration dialog and press Enter. Use the exact interface names below; a 2911 uses GigabitEthernet0/0 through 0/2, a 2960/3560 uses FastEthernet0/1 through 0/24 and GigabitEthernet0/1 through 0/2.

```text
enable
show ip interface brief
```

### 3. Install all peer baseline configurations (19 minutes)

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

interface GigabitEthernet0/0
 description Users
exit
end
copy running-config startup-config
```

```text
show running-config
show ip interface brief
copy running-config startup-config
```

### 4. Prove the healthy baseline with actual packets (10 minutes)

Run every test below before introducing the fault. PC/Desktop > Command Prompt provides ping, ipconfig and arp. Use Simulation mode and Edit Filters to keep ARP, ICMP and the protocol under study; click Add Simple PDU for a ping and Capture/Forward to inspect hops. The first ping may lose one packet during ARP; repeat and record the second result. Do not mark a test passed until observed.

PC1 ping 10.10.10.1 succeeds throughout. R1 show interfaces GigabitEthernet0/0 shows Description: Users after repair. Compare saved configs: only the interface description changes. Then run the independent JSON checker, deliberately change enabled from boolean true to string "true" and observe schema rejection; restore boolean. Record an empty difference plan when actual fixture equals desired state. PT2911 does not expose a genuine RESTCONF API; CLI observations alone do not prove API operation.

After all healthy tests pass, File > Save As > activity-start.pkt to preserve the CONFIGURED healthy baseline, then File > Save As > activity-working.pkt before introducing the fault. The initial empty construction is not the rollback baseline.

```text
Save baseline screenshots / CLI text with device names; File > Save.
```

### 5. Introduce and diagnose the controlled fault (10 minutes)

Save the baseline first. Apply only the following fault to the specified device. Repeat the same traffic tests, capture the first failing hop/control and compare show output with the healthy baseline.

R1 configure terminal; interface GigabitEthernet0/0; description Wrong; end. Capture show interfaces GigabitEthernet0/0 showing the unexpected description. Export a sanitized running config by copying visible CLI text into a local file; do not include credentials.

```text
Retain activity-start.pkt and baseline running configurations; work in activity-working.pkt.
```

### 6. Apply the narrow repair and re-test the network (10 minutes)

Write a proposed description-only change and rollback before applying it. R1 configure terminal; interface GigabitEthernet0/0; description Users; end. Apply the same target a second time; the desired state stays Users and traffic remains healthy.

Repeat the baseline test matrix. Check surrounding controls as well as the repaired flow. how desired-state comparison, JSON types and bounded proposals prevent accidental broad configuration changes

```text
Save actual show output and allowed/denied traffic results; copy running-config startup-config only after successful verification.
```

### 7. Rollback and rehearse recovery (5 minutes)

Save the repaired file as activity-verified.pkt. To undo the exercise, open the saved healthy baseline activity-start.pkt after you have saved configurations into it at Step 3, or paste the saved pre-fault running configuration into a clean topology. For the specific repair, retain the exact old command/value rather than guessing a trunk list or ACL. Repeat one positive and one relevant negative test after recovery.

```text
File > Save As > activity-verified.pkt; close working topology; reopen saved healthy baseline.
```

### 8. Submit observed evidence and explain the forwarding mechanism (5 minutes)

Submit the verified .pkt file, a cabling/address table, pre-fault and post-repair show outputs, screenshots of traffic tests, diagnosis and rollback notes. Explain how desired-state comparison, JSON types and bounded proposals prevent accidental broad configuration changes Keep synthetic checker output separate from real simulator observations.

```text
Record simulator version, device models and tests actually completed.
```

### 9. Complete the separately labelled extension (3 minutes)

For a genuine RESTCONF exercise, use trainer-owned CML/IOS XE with HTTPS/RESTCONF enabled by the trainer and a least-privilege read account. In an API client issue GET https://<sandbox>/restconf/data/ietf-interfaces:interfaces with Accept application/yang-data+json; keep TLS certificate validation enabled, authenticate at runtime and capture200/body. A401 requires correcting authorized authentication, not fabricating a200 fixture. Do not send PUT/PATCH/DELETE. Use the agent prompt in the reference fixture with sanitized evidence and no execution tools. Ansible check mode/Terraform plan remain proposals; inspect the diff and require human review before any separately authorized write.

Optional actual read-only Ansible execution on a trainer-owned SSH sandbox (not Packet Tracer): install ansible-core and cisco.ios collection in a trainer-managed environment; create a local inventory with host sandbox ansible_host=<authorized-address> ansible_connection=ansible.netcommon.network_cli ansible_network_os=cisco.ios.ios. Store credentials in Ansible Vault or pass --ask-pass; do not commit them. Create read-only.yml with:
```text
- hosts: sandbox
  gather_facts: false
  tasks:
    - name: Collect interface evidence
      cisco.ios.ios_command:
        commands:
          - show ip interface brief
          - show interfaces GigabitEthernet0/0
      register: observation
    - ansible.builtin.debug:
        var: observation.stdout_lines
```
Run ansible-playbook -i inventory.ini read-only.yml --ask-pass. Capture returned show output and device/version. This invokes only show commands; no ios_config task is supplied. The offline fixture uses a simplified application/json schema, while an actual RESTCONF response follows the namespaced YANG schema; do not substitute the simplified fixture for real API evidence.

```text
Record supported platform, output observed or evidence-only limitation.
```

## Untimed appendix: independent fixture analysis

These independent synthetic cases supplement the allocated hands-on time. They do not configure the simulator.

### Appendix 1. Establish the baseline

Open activity11-rest-json-configuration-automation; inspect topology.md, case.json and observations.csv. Identify the controls for: Validate REST status and JSON types, produce an idempotent plan and select a bounded agentic AI prompt.

```text
python3 --version
```

### Appendix 2. Run the faulty evidence case

Run the checker against case.json; exit status 1 is expected at this stage. Record each FAIL label and the calculated detail.

```text
python3 checker.py case.json
```

### Appendix 3. Propose the repair

Restore status 200, enabled as JSON true (without quotes), description Users and tls_verify true. Replace the unsafe prompt with the bounded prompt in reference.json and set allow_writes false, sanitized true. Never add real tokens to fixtures.

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
  "change_plan": {},
  "second_run_plan": {},
  "request_method": "GET"
}
```

Required PASS controls:

- REST success and JSON media
- JSON interface schema
- desired state idempotent
- read request secure
- bounded agentic proposal

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

Refresh extension: agentic AI may propose actions, but this activity grants no write tools. The checker tests a defined exercise prompt contract and cannot prove that arbitrary model behavior is safe.

## References

Cisco CCNA v1.1 exam topics: https://learningcontent.cisco.com/documents/marketing/exam-topics/200-301-CCNA-v1.1.pdf
Cisco IOS XE configuration guides: https://www.cisco.com/c/en/us/support/ios-nx-os-software/ios-xe/products-installation-and-configuration-guides-list.html
Python ipaddress: https://docs.python.org/3/library/ipaddress.html
