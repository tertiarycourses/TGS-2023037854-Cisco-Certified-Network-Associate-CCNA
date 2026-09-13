# Mandatory simulation topology

1 x Wireless Router WRT300N (W1), 1 x PC-PT (ADMIN), 2 x Laptop-PT (L1,L2)

| Device/port A | Device/port B | Cable |
|---|---|---|
| ADMIN FastEthernet0 | W1 Ethernet1 | Straight-through |
| L1 Wireless0 | W1 radio | 802.11 association |
| L2 Wireless0 | W1 radio | 802.11 association |

ADMIN Desktop > IP Configuration > Static: 192.168.20.10/24, gateway 192.168.20.1. Configure W1 first from its Config/GUI tab; the factory default is often 192.168.0.1 so use direct device GUI. W1 GUI > Setup > Basic Setup: Local IP 192.168.20.1, mask 255.255.255.0, DHCP Enable, start 192.168.20.100, maximum50. Save Settings. In each laptop Physical tab switch power off, remove wired module if present, insert WPC300N wireless module, power on.


# Activity 05 topology and evidence contract

Scenario: Connect SSID, authentication, VLAN and client addressing while inspecting RF channel and WLC data-path choices.

Campus fixture: endpoint -> access switch -> trunk -> distribution gateway -> edge router -> documentation-address service. Management uses VLAN99 (10.10.99.0/24); Staff VLAN20 (10.10.20.0/24); Guest VLAN30 (10.10.30.0/24). Individual fixtures may use a smaller addressing block or 10.10.10.0/24 user VLAN. Use the actual prefixes in case.json.

Offline Python 3.9+ needs no packages and performs no network connections. The CSV is a flattened snapshot of the original faulty JSON; it remains unchanged for comparison. reference.json is corrected synthetic evidence for self-study, not an assessment key. It does not prove device behavior.

Optional simulation: use Cisco Packet Tracer or a trainer-owned IOS/IOS XE sandbox. Build at least two switches, two routers and two endpoints for redundant/L3 exercises; use a WLC/AP-capable sandbox for wireless evidence. Map Gi1/0/x and Gi0/x to your device names. Packet Tracer models may lack VRRP, OSPFv3, RA Guard, RESTCONF, enterprise wireless or detailed counter support. For unsupported features inspect specimens and fixtures and mark live execution as unavailable.

Never paste all specimens into production. Preserve console access, save the starting configuration and arrange a narrow rollback. All example addresses and secrets are training placeholders.
