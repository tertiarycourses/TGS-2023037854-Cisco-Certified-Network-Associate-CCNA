# Lab 02 - Device Basics, Cabling, and Management Access

## Objectives

- Configure basic router and switch settings.
- Verify interface status.
- Configure SSH management.
- Use CDP and LLDP.

## Steps

1. Build a topology with one router, one switch, and two PCs.
2. Cable devices using Ethernet links.
3. Configure device hostnames.
4. Configure enable secret and console password.
5. Enable service password encryption.
6. Configure router interface IP addresses.
7. Configure a switch management SVI.
8. Configure the switch default gateway.
9. Verify with `show ip interface brief`.
10. Configure local username, domain name, and RSA keys.
11. Enable SSH on VTY lines.
12. Test SSH access.
13. Run `show cdp neighbors detail`.
14. Enable and verify LLDP if available.
15. Save the configuration.

## Validation

- Interfaces are up/up where expected.
- Switch management IP is reachable.
- SSH works and Telnet is not required.
- Neighbor discovery shows connected devices.

## Review Questions

1. Why should SSH be used instead of Telnet?
2. What does an interface state of administratively down mean?
3. Why does a Layer 2 switch need a default gateway?
4. How do CDP and LLDP help operations?
