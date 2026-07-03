# Tools Reference

## Free Tools

| Tool | Use in Course |
| --- | --- |
| Cisco Packet Tracer | Main simulator for CCNA labs. |
| Wireshark | Packet capture and protocol inspection. |
| PuTTY / Tera Term / Windows Terminal | Console or SSH access. |
| diagrams.net | Topology diagrams and addressing plans. |
| Text editor | Save running configs, command output, and notes. |

## Core Cisco IOS Commands

```text
enable
configure terminal
hostname <name>
show running-config
show startup-config
show ip interface brief
show interfaces status
show vlan brief
show interfaces trunk
show spanning-tree
show etherchannel summary
show mac address-table
show ip route
show ip ospf neighbor
show ip nat translations
show access-lists
copy running-config startup-config
```

## Troubleshooting Flow

1. Identify symptom and expected result.
2. Check cabling and interface status.
3. Check IP address, mask, and gateway.
4. Check VLAN membership and trunking.
5. Check routing table and next hop.
6. Check ACLs, NAT, and services.
7. Change one thing at a time.
8. Verify and document the fix.
