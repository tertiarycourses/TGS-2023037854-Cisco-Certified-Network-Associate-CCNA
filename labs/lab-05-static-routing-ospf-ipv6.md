# Lab 05 - Static Routing, OSPF, and IPv6

## Objectives

- Configure static and default routes.
- Configure floating static routes.
- Configure single-area OSPFv2.
- Configure basic IPv6 connectivity.

## Steps

1. Build a three-router topology.
2. Assign IPv4 addresses to all router links and LAN interfaces.
3. Configure PC addresses and default gateways.
4. Configure static routes between LANs.
5. Configure a default route on an edge router.
6. Configure a floating static route with higher administrative distance.
7. Verify with `show ip route`.
8. Test with `ping` and `traceroute`.
9. Remove or ignore static routes for OSPF practice.
10. Configure OSPF process ID and router IDs.
11. Advertise connected networks in area 0.
12. Verify with `show ip ospf neighbor`.
13. Verify learned OSPF routes.
14. Configure IPv6 addresses on a simple link.
15. Test IPv6 connectivity.

## Validation

- Static routing works before OSPF.
- OSPF neighbors form successfully.
- Routing table shows expected routes.
- IPv6 link test succeeds.

## Review Questions

1. What is longest prefix match?
2. What is administrative distance?
3. Why does OSPF need neighbor adjacency?
4. How is a floating static route used?
