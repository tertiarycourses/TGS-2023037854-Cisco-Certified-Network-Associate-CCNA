# Lab 06 - IP Services: NAT, DHCP, DNS, NTP, and Syslog

## Objectives

- Configure DHCP.
- Configure NAT/PAT.
- Review DNS and NTP behavior.
- Configure basic logging.

## Steps

1. Build a LAN-to-edge-router topology.
2. Configure a DHCP pool for LAN clients.
3. Exclude gateway and reserved addresses.
4. Verify client IP assignment.
5. Configure NAT overload for inside clients.
6. Mark inside and outside interfaces.
7. Generate traffic from a client.
8. Verify with `show ip nat translations`.
9. Configure DNS server address or disable unwanted DNS lookup.
10. Configure NTP settings or review NTP concepts if simulator support is limited.
11. Configure logging buffer or syslog destination.
12. Generate an interface event.
13. Review log output.
14. Save configuration and notes.

## Validation

- Clients receive DHCP addresses.
- NAT translations appear.
- DNS/NTP behavior is explained.
- Logs show generated events.

## Review Questions

1. What is the DHCP DORA process?
2. Why is NAT overload commonly used?
3. Why is time synchronization important for logs?
4. How does syslog support troubleshooting?
