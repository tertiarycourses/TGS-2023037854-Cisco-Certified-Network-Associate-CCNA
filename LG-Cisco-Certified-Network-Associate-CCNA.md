# Learner Guide - Cisco Certified Network Associate (CCNA)

## Course Overview

This learner guide supports hands-on CCNA training for learners who need to understand, configure, operate, and troubleshoot small to medium routed and switched networks.

The labs follow the major CCNA skill areas:

1. Network fundamentals.
2. Network access.
3. IP connectivity.
4. IP services.
5. Security fundamentals.
6. Automation and programmability.

## Before You Start

### Recommended Lab Tools

Use one of the following:

- Cisco Packet Tracer.
- Cisco Modeling Labs.
- GNS3.
- EVE-NG.
- Physical Cisco routers and switches.

### Lab Journal

For every lab, record:

- Topology diagram.
- IP addressing table.
- Device names.
- Configuration commands.
- Verification commands.
- Test results.
- Troubleshooting notes.
- Final saved configuration.

### Core Verification Commands

```text
show running-config
show ip interface brief
show interfaces status
show vlan brief
show interfaces trunk
show spanning-tree
show etherchannel summary
show ip route
show ip ospf neighbor
show access-lists
show cdp neighbors
show lldp neighbors
ping
traceroute
```

## Learning Outcomes

By the end of the course, you should be able to:

1. Explain OSI, TCP/IP, encapsulation, and forwarding decisions.
2. Subnet IPv4 networks and recognize IPv6 address types.
3. Configure basic router and switch management.
4. Configure VLANs, trunks, and inter-VLAN routing.
5. Verify STP and EtherChannel behavior.
6. Configure static routes, default routes, and single-area OSPFv2.
7. Configure DHCP, NAT/PAT, NTP, DNS lookup, and syslog basics.
8. Secure management access and apply ACLs.
9. Explain wireless architecture and security concepts.
10. Use a structured troubleshooting method.
11. Explain controller-based networking, REST APIs, JSON, and automation basics.

## Course Flow

### Day 1

| Time | Activity |
| --- | --- |
| 09:00 | Course briefing, exam domains, lab setup |
| 09:30 | Lab 01 - Network Models, Addressing, and Subnetting |
| 11:00 | Lab 02 - Device Basics, Cabling, and Management Access |
| 13:00 | Lab 03 - VLANs, Trunks, and Inter-VLAN Routing |
| 15:30 | Lab 04 - STP, EtherChannel, and Layer 2 Troubleshooting |
| 17:00 | Review and configuration backup |

### Day 2

| Time | Activity |
| --- | --- |
| 09:00 | Day 1 recap and subnetting warm-up |
| 09:30 | Lab 05 - Static Routing, OSPF, and IPv6 |
| 11:30 | Lab 06 - IP Services: NAT, DHCP, DNS, NTP, and Syslog |
| 13:30 | Lab 07 - Security, ACLs, Port Security, and Wireless |
| 15:30 | Lab 08 - Troubleshooting, Automation, and Exam Review |
| 16:45 | Final cleanup and study plan |

## Lab 01 Guide - Network Models, Addressing, and Subnetting

### Objectives

- Explain OSI and TCP/IP layers.
- Understand encapsulation.
- Build an IPv4 subnet plan.
- Recognize IPv6 address types.

### Steps

1. Draw the OSI model and TCP/IP model side by side.
2. Map common protocols to the correct layers.
3. Explain what changes at each encapsulation step from application data to Ethernet frame.
4. Given a /24 network, divide it into at least four subnets.
5. Record network address, first host, last host, broadcast address, and prefix length.
6. Assign IP addresses to a simple topology.
7. Configure host IP addresses in Packet Tracer.
8. Use `ping` to test same-subnet reachability.
9. Review IPv6 global unicast, link-local, multicast, and loopback address examples.
10. Document the addressing table.

### Deliverables

- OSI/TCP-IP comparison.
- IPv4 subnet table.
- IPv6 address notes.
- Completed addressing table.

### Checkpoint

You can explain how a host decides whether to send traffic directly or to the default gateway.

## Lab 02 Guide - Device Basics, Cabling, and Management Access

### Objectives

- Configure basic Cisco device settings.
- Verify interface status.
- Enable secure management access.
- Use CDP and LLDP.

### Steps

1. Add one router, one switch, and two PCs to the lab topology.
2. Cable the devices using correct interface types.
3. Configure hostnames on router and switch.
4. Configure console password, enable secret, and service password encryption.
5. Configure a management IP address on the switch SVI.
6. Configure the default gateway on the switch.
7. Configure router interface IP addresses.
8. Verify with `show ip interface brief`.
9. Configure local username and SSH access.
10. Set domain name and generate RSA keys.
11. Test SSH from a PC or terminal client.
12. Use `show cdp neighbors detail` and `show lldp neighbors`.
13. Save the configuration.

### Deliverables

- Basic device configuration.
- Management IP plan.
- SSH verification notes.
- Neighbor discovery output.

### Checkpoint

You can securely access devices and verify physical/logical connectivity.

## Lab 03 Guide - VLANs, Trunks, and Inter-VLAN Routing

### Objectives

- Create VLANs.
- Configure access ports and trunks.
- Configure inter-VLAN routing.
- Verify VLAN connectivity.

### Steps

1. Build a topology with two switches, one router or Layer 3 switch, and four PCs.
2. Create VLAN 10 for users and VLAN 20 for admins.
3. Assign access ports to the correct VLANs.
4. Configure the inter-switch link as an 802.1Q trunk.
5. Verify with `show vlan brief` and `show interfaces trunk`.
6. Configure router-on-a-stick subinterfaces or Layer 3 SVIs.
7. Assign default gateways to PCs.
8. Test same-VLAN connectivity.
9. Test inter-VLAN connectivity.
10. Troubleshoot any native VLAN or allowed VLAN mismatch.
11. Save working configurations.

### Deliverables

- VLAN table.
- Trunk configuration.
- Inter-VLAN routing configuration.
- Ping test results.

### Checkpoint

You can explain how VLAN tags allow multiple VLANs across one trunk link.

## Lab 04 Guide - STP, EtherChannel, and Layer 2 Troubleshooting

### Objectives

- Verify STP behavior.
- Configure STP root bridge priority.
- Configure EtherChannel with LACP.
- Troubleshoot Layer 2 issues.

### Steps

1. Build a three-switch topology with redundant links.
2. Verify STP state with `show spanning-tree`.
3. Identify root bridge, root ports, designated ports, and blocked ports.
4. Configure the intended root bridge priority.
5. Enable PortFast on access ports.
6. Discuss BPDU Guard use cases.
7. Configure two physical links as an LACP EtherChannel.
8. Verify with `show etherchannel summary`.
9. Check MAC learning with `show mac address-table`.
10. Create and fix one troubleshooting scenario such as wrong VLAN, trunk mismatch, or down link.
11. Record symptoms, command output, cause, and fix.

### Deliverables

- STP role notes.
- Root bridge configuration.
- EtherChannel configuration.
- Layer 2 troubleshooting log.

### Checkpoint

You can identify why STP blocks links and how EtherChannel provides logical link aggregation.

## Lab 05 Guide - Static Routing, OSPF, and IPv6

### Objectives

- Configure static and default routes.
- Configure floating static routes.
- Configure single-area OSPFv2.
- Configure basic IPv6 addressing.

### Steps

1. Build a three-router topology.
2. Assign IPv4 addresses to router interfaces.
3. Configure host default gateways.
4. Add static routes between networks.
5. Configure a default route toward an edge router.
6. Configure a floating static route with higher administrative distance.
7. Verify with `show ip route`, `ping`, and `traceroute`.
8. Remove static routes and configure single-area OSPFv2.
9. Set router IDs.
10. Verify OSPF neighbors with `show ip ospf neighbor`.
11. Verify learned routes.
12. Configure IPv6 addresses and link-local awareness on a simple path.
13. Test IPv6 reachability.

### Deliverables

- Routing table screenshots or outputs.
- Static and OSPF configuration.
- IPv6 addressing notes.
- Reachability test results.

### Checkpoint

You can explain route selection using longest prefix match, administrative distance, and metric.

## Lab 06 Guide - IP Services: NAT, DHCP, DNS, NTP, and Syslog

### Objectives

- Configure DHCP services.
- Configure NAT/PAT.
- Configure DNS lookup behavior.
- Configure NTP and syslog basics.

### Steps

1. Build a small LAN-to-internet simulation topology.
2. Configure a DHCP pool for client PCs.
3. Exclude gateway and reserved addresses.
4. Verify client address assignment.
5. Configure static or dynamic NAT/PAT on the edge router.
6. Mark inside and outside interfaces.
7. Verify translations with `show ip nat translations`.
8. Configure DNS server address or disable unwanted DNS lookup as needed.
9. Configure NTP server settings or a simulated time source.
10. Configure syslog destination or logging buffer.
11. Generate events and review logs.
12. Document which IP services support network operations.

### Deliverables

- DHCP configuration.
- NAT/PAT configuration.
- NTP/syslog notes.
- Verification outputs.

### Checkpoint

You can explain how DHCP, NAT, DNS, NTP, and syslog support daily network operations.

## Lab 07 Guide - Security, ACLs, Port Security, and Wireless

### Objectives

- Secure device management.
- Configure standard and extended ACLs.
- Configure port security.
- Review wireless architecture and security.

### Steps

1. Review current management configuration.
2. Ensure SSH is used instead of Telnet.
3. Configure strong local credentials.
4. Configure a standard ACL to restrict VTY access.
5. Configure an extended ACL to permit one service and deny another.
6. Apply ACLs in the correct direction and interface.
7. Verify with `show access-lists` and traffic tests.
8. Configure port security on an access port.
9. Set maximum MAC addresses and violation action.
10. Verify port security status.
11. Review wireless components: AP, WLC, SSID, CAPWAP, WPA2/WPA3.
12. Discuss how WLAN security differs from wired access security.

### Deliverables

- Secure management configuration.
- ACL configuration and test results.
- Port security output.
- Wireless architecture notes.

### Checkpoint

You can choose where to place an ACL and explain how port security protects access ports.

## Lab 08 Guide - Troubleshooting, Automation, and Exam Review

### Objectives

- Use structured troubleshooting.
- Review automation and controller-based networking concepts.
- Read basic JSON.
- Build an exam readiness checklist.

### Steps

1. Use a broken topology from your trainer or intentionally misconfigure one item.
2. Start with the symptom and expected behavior.
3. Check physical/link status.
4. Check addressing and default gateways.
5. Check VLANs, trunks, routes, ACLs, and services.
6. Record each command used and what it proves.
7. Fix the issue and verify end-to-end reachability.
8. Review control plane and data plane concepts.
9. Compare traditional networking and controller-based networking.
10. Read a simple JSON object and identify keys and values.
11. Explain REST API methods: GET, POST, PUT/PATCH, DELETE.
12. Create a final personal study checklist for weak CCNA topics.

### Deliverables

- Troubleshooting log.
- Fixed configuration.
- Automation concepts notes.
- Exam readiness checklist.

### Checkpoint

You can troubleshoot methodically and explain why automation changes network management workflows.

## Final Skills Checklist

Before finishing the course, confirm that you can:

- Subnet IPv4 networks.
- Recognize common IPv6 address types.
- Configure basic router and switch management.
- Configure VLANs and trunks.
- Configure inter-VLAN routing.
- Verify STP and EtherChannel.
- Configure static routes and OSPFv2.
- Configure DHCP and NAT.
- Apply ACLs safely.
- Secure management access.
- Explain wireless architecture basics.
- Explain controller-based networking and REST API basics.
