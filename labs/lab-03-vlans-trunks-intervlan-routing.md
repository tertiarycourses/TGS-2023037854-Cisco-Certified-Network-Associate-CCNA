# Lab 03 - VLANs, Trunks, and Inter-VLAN Routing

## Objectives

- Configure VLANs and access ports.
- Configure 802.1Q trunks.
- Configure inter-VLAN routing.
- Verify VLAN reachability.

## Steps

1. Build a topology with two switches, one router or Layer 3 switch, and four PCs.
2. Create VLAN 10 and VLAN 20.
3. Name the VLANs.
4. Assign two PCs to VLAN 10 and two PCs to VLAN 20.
5. Configure the inter-switch link as a trunk.
6. Verify with `show vlan brief`.
7. Verify with `show interfaces trunk`.
8. Configure router-on-a-stick subinterfaces or Layer 3 SVIs.
9. Assign default gateways to PCs.
10. Test same-VLAN connectivity.
11. Test inter-VLAN connectivity.
12. Troubleshoot one issue such as wrong access VLAN or trunk not formed.
13. Save working configurations.

## Validation

- VLAN membership is correct.
- Trunk carries required VLANs.
- Hosts in different VLANs can communicate through the gateway.
- Troubleshooting notes identify symptom, cause, and fix.

## Review Questions

1. What is the purpose of a VLAN?
2. Why is trunking needed between switches?
3. What does the native VLAN do?
4. How does router-on-a-stick provide inter-VLAN routing?
