#!/usr/bin/env bash

PCAP="packet.pcapng"

tshark -r "$PCAP" -Y "ip.src == 10.203.6.196"
tshark -r "$PCAP" -Y "ipv6.dst == ff02::1:ff7f:b94c"
tshark -r "$PCAP" -Y "ip.src == 10.203.6.196 or ip.dst == 10.203.6.196"
tshark -r "$PCAP" -Y "arp"
tshark -r "$PCAP" -Y "tcp.port == 40104 or udp.port == 40104"
tshark -r "$PCAP" -Y "udp.dstport == 443"
tshark -r "$PCAP" -Y "frame.number >= 5 and frame.number <= 10"
tshark -r "$PCAP" -Y "frame.number >= 25 and frame.number <= 40 and not (udp and ipv6.dst == ff02::1:ff7f:b94c)"