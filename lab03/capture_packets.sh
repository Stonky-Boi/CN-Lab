#!/bin/bash

# Find network interface and machine IP
INTERFACE=$(route get default | awk '/interface: / {print $2}')
IP=$(ipconfig getifaddr "$INTERFACE")
echo "Interface: $INTERFACE"
echo "Host IP: $IP"
echo

# 1. Capture 20 packets
sudo tcpdump -i "$INTERFACE" -c 20 -w q1.pcap
echo

# 2. Traffic including host IP
sudo tcpdump -i "$INTERFACE" -c 20 host "$IP" -w q2.pcap
echo

# 3. TCP packets
sudo tcpdump -i "$INTERFACE" -c 20 tcp -w q3.pcap
echo

# 4. Destination port 443
sudo tcpdump -i "$INTERFACE" -c 20 dst port 443 -w q4.pcap
echo

# 5. Source port 443
sudo tcpdump -i "$INTERFACE" -c 20 src port 443 -w q5.pcap
echo

# 6. Host as destination
sudo tcpdump -i "$INTERFACE" -c 20 dst host "$IP" -w q6.pcap
echo

# 7. Host as source
sudo tcpdump -i "$INTERFACE" -c 20 src host "$IP" -w q7.pcap
echo

# 8. Host and port number
sudo tcpdump -i "$INTERFACE" -c 20 host "$IP" and port 443 -w q8.pcap
echo

# 9. Everything except UDP
sudo tcpdump -i "$INTERFACE" -c 20 not udp -w q9.pcap
echo