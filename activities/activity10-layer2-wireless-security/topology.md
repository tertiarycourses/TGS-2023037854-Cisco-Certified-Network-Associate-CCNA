# Mandatory simulation topology

1 x Switch2960 (S1), 1 x Router2911 (R1), 1 x Server-PT (DHCP), 2 x PC-PT (PC1,PC2)

| Device/port A | Device/port B | Cable |
|---|---|---|
| PC1 FastEthernet0 | S1 FastEthernet0/1 | Straight-through |
| PC2 FastEthernet0 | S1 FastEthernet0/2 | Straight-through |
| DHCP FastEthernet0 | S1 FastEthernet0/24 | Straight-through |
| R1 GigabitEthernet0/0 | S1 GigabitEthernet0/1 | Straight-through |

Set Desktop > IP Configuration > Static on each endpoint.

| Endpoint | Address | Mask | Gateway | DNS |
|---|---|---|---|---|
| DHCP | 10.10.10.50 | 255.255.255.0 | 10.10.10.1 | 10.10.10.50 |
| PC1 | DHCP | DHCP | DHCP | DHCP |
| PC2 | DHCP | DHCP | DHCP | DHCP |

DHCP Services > DHCP: On; pool USERS; Default Gateway10.10.10.1; DNS10.10.10.50; Start IP10.10.10.100; Mask255.255.255.0; maximum50; Add/Save. PC1/PC2 Desktop > IP Configuration > DHCP.


# Activity 10 topology and evidence contract

Scenario: Map trusted infrastructure ports and untrusted edge ports to DHCP snooping, DAI, port security and wireless authentication.

Campus fixture: endpoint -> access switch -> trunk -> distribution gateway -> edge router -> documentation-address service. Management uses VLAN99 (10.10.99.0/24); Staff VLAN20 (10.10.20.0/24); Guest VLAN30 (10.10.30.0/24). Individual fixtures may use a smaller addressing block or 10.10.10.0/24 user VLAN. Use the actual prefixes in case.json.

Offline Python 3.9+ needs no packages and performs no network connections. The CSV is a flattened snapshot of the original faulty JSON; it remains unchanged for comparison. reference.json is corrected synthetic evidence for self-study, not an assessment key. It does not prove device behavior.

Optional simulation: use Cisco Packet Tracer or a trainer-owned IOS/IOS XE sandbox. Build at least two switches, two routers and two endpoints for redundant/L3 exercises; use a WLC/AP-capable sandbox for wireless evidence. Map Gi1/0/x and Gi0/x to your device names. Packet Tracer models may lack VRRP, OSPFv3, RA Guard, RESTCONF, enterprise wireless or detailed counter support. For unsupported features inspect specimens and fixtures and mark live execution as unavailable.

Never paste all specimens into production. Preserve console access, save the starting configuration and arrange a narrow rollback. All example addresses and secrets are training placeholders.
