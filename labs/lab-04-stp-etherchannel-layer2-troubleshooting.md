# Lab 04 - STP, EtherChannel, and Layer 2 Troubleshooting

## Objectives

- Verify STP roles and states.
- Configure STP root bridge.
- Configure LACP EtherChannel.
- Troubleshoot Layer 2 issues.

## Steps

1. Build a three-switch topology with redundant links.
2. Run `show spanning-tree`.
3. Identify the root bridge.
4. Identify root ports, designated ports, and blocked ports.
5. Configure the intended switch as root bridge.
6. Enable PortFast on access ports.
7. Discuss when BPDU Guard should be used.
8. Configure two physical links as an LACP EtherChannel.
9. Verify with `show etherchannel summary`.
10. Verify MAC learning with `show mac address-table`.
11. Create a Layer 2 fault such as a wrong VLAN, down port, or trunk mismatch.
12. Troubleshoot with `show` commands.
13. Record symptom, root cause, fix, and verification.

## Validation

- Intended root bridge is active.
- EtherChannel is bundled.
- MAC table shows learned addresses.
- Troubleshooting log is complete.

## Review Questions

1. Why does STP block redundant links?
2. What is the benefit of EtherChannel?
3. Why should PortFast only be used on access ports?
4. What symptoms can a trunk mismatch cause?
