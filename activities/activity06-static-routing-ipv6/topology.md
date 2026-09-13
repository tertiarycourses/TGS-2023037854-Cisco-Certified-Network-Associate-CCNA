# Mandatory simulation topology

2 x Router 2911 (R1,R2), 2 x Switch2960 (S1,S2), 2 x PC-PT (PC1,PC2)

| Device/port A | Device/port B | Cable |
|---|---|---|
| PC1 FastEthernet0 | S1 FastEthernet0/1 | Straight-through |
| S1 FastEthernet0/24 | R1 GigabitEthernet0/0 | Straight-through |
| R1 GigabitEthernet0/1 | R2 GigabitEthernet0/1 | Cross-over/Auto |
| R2 GigabitEthernet0/0 | S2 FastEthernet0/24 | Straight-through |
| S2 FastEthernet0/1 | PC2 FastEthernet0 | Straight-through |

Set Desktop > IP Configuration > Static on each endpoint.

| Endpoint | Address | Mask | Gateway | DNS |
|---|---|---|---|---|
| PC1 | 10.10.10.10 | 255.255.255.0 | 10.10.10.1 | none |
| PC2 | 10.10.20.20 | 255.255.255.0 | 10.10.20.1 | none |

Also set PC1 IPv6 2001:db8:10::10/64 gateway2001:db8:10::1; PC2 IPv6 2001:db8:20::20/64 gateway2001:db8:20::1.


# Activity 06 topology and evidence contract

Scenario: Apply longest-prefix match, a floating route and interface-scoped IPv6 link-local next hops.

Campus fixture: endpoint -> access switch -> trunk -> distribution gateway -> edge router -> documentation-address service. Management uses VLAN99 (10.10.99.0/24); Staff VLAN20 (10.10.20.0/24); Guest VLAN30 (10.10.30.0/24). Individual fixtures may use a smaller addressing block or 10.10.10.0/24 user VLAN. Use the actual prefixes in case.json.

Offline Python 3.9+ needs no packages and performs no network connections. The CSV is a flattened snapshot of the original faulty JSON; it remains unchanged for comparison. reference.json is corrected synthetic evidence for self-study, not an assessment key. It does not prove device behavior.

Optional simulation: use Cisco Packet Tracer or a trainer-owned IOS/IOS XE sandbox. Build at least two switches, two routers and two endpoints for redundant/L3 exercises; use a WLC/AP-capable sandbox for wireless evidence. Map Gi1/0/x and Gi0/x to your device names. Packet Tracer models may lack VRRP, OSPFv3, RA Guard, RESTCONF, enterprise wireless or detailed counter support. For unsupported features inspect specimens and fixtures and mark live execution as unavailable.

Never paste all specimens into production. Preserve console access, save the starting configuration and arrange a narrow rollback. All example addresses and secrets are training placeholders.
