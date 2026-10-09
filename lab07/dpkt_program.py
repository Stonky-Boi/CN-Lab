import dpkt
import socket

def get_ip_tcp(buf):
    try:
        eth = dpkt.ethernet.Ethernet(buf)
        if not isinstance(eth.data, dpkt.ip.IP):
            return None, None, None
        ip = eth.data
        tcp = ip.data if isinstance(ip.data, dpkt.tcp.TCP) else None
        return eth, ip, tcp
    except (dpkt.UnpackError, ValueError, TypeError):
        return None, None, None

def task_a(packets):
    print("\n--- (a) Packet Count and MAC Addresses ---")
    print("Total number of packets:", len(packets))
    for i, (ts, buf) in enumerate(packets[:10], start=1):
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            print(
                f"Packet {i}: "
                f"Source MAC = {dpkt.utils.mac_to_str(eth.src)}, "
                f"Destination MAC = {dpkt.utils.mac_to_str(eth.dst)}"
            )
        except (dpkt.UnpackError, ValueError, TypeError):
            print(f"Packet {i}: Unable to parse Ethernet frame")

def task_b(packets):
    print("\n--- (b) TCP, UDP and ICMP Packet Counts ---")
    tcp_count = 0
    udp_count = 0
    icmp_count = 0
    ip_count = 0
    for ts, buf in packets:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            if not isinstance(ip, dpkt.ip.IP):
                continue
            ip_count += 1
            if ip.p == dpkt.ip.IP_PROTO_TCP:
                tcp_count += 1
            elif ip.p == dpkt.ip.IP_PROTO_UDP:
                udp_count += 1
            elif ip.p == dpkt.ip.IP_PROTO_ICMP:
                icmp_count += 1
        except (dpkt.UnpackError, ValueError, TypeError):
            continue
    print("Total IPv4 packets:", ip_count)
    print("TCP packets:", tcp_count)
    print("UDP packets:", udp_count)
    print("ICMP packets:", icmp_count)

def task_c(packets):
    print("\n--- (c) TCP SYN Packets ---")
    syn_count = 0
    syn_without_ack = 0
    for ts, buf in packets:
        eth, ip, tcp = get_ip_tcp(buf)
        if tcp is None:
            continue
        if tcp.flags & dpkt.tcp.TH_SYN:
            syn_count += 1
            if not (tcp.flags & dpkt.tcp.TH_ACK):
                syn_without_ack += 1
                print(
                    "SYN without ACK:",
                    "Source IP =", socket.inet_ntoa(ip.src),
                    "Destination IP =", socket.inet_ntoa(ip.dst),
                    "Source Port =", tcp.sport,
                    "Destination Port =", tcp.dport
                )
    print("Total TCP packets with SYN flag:", syn_count)
    print("SYN without ACK packets:", syn_without_ack)

def task_d(packets):
    print("\n--- (d) HTTP GET Requests ---")
    get_count = 0
    for ts, buf in packets:
        eth, ip, tcp = get_ip_tcp(buf)
        if tcp is None or tcp.dport != 80 or not tcp.data:
            continue
        try:
            request = dpkt.http.Request(tcp.data)
            if request.method == "GET":
                get_count += 1
                print("Source IP:", socket.inet_ntoa(ip.src))
                print("Destination IP:", socket.inet_ntoa(ip.dst))
                print("Requested URL:", request.uri)
                print()
        except (dpkt.UnpackError, ValueError, TypeError):
            continue
    print("Total HTTP GET requests parsed:", get_count)

def task_e(packets):
    print("\n--- (e) HTTP Port 80 and HTTPS Port 443 ---")
    for ts, buf in packets:
        eth, ip, tcp = get_ip_tcp(buf)
        if tcp is None:
            continue
        if tcp.sport in (80, 443) or tcp.dport in (80, 443):
            service = (
                "HTTP (port 80)"
                if tcp.sport == 80 or tcp.dport == 80
                else "HTTPS (port 443)"
            )
            print("Protocol:", service)
            print("Source IP:", socket.inet_ntoa(ip.src))
            print("Source Port:", tcp.sport)
            print("Destination IP:", socket.inet_ntoa(ip.dst))
            print("Destination Port:", tcp.dport)
            print("-" * 40)

def task_f(packets):
    print("\n--- (f) TCP Conversation Between Two IPs ---")
    ip1 = "192.168.0.51"
    ip2 = "91.189.89.240"
    socket.inet_aton(ip1)
    socket.inet_aton(ip2)
    conversation_count = 0
    for ts, buf in packets:
        eth, ip, tcp = get_ip_tcp(buf)
        if tcp is None:
            continue
        src = socket.inet_ntoa(ip.src)
        dst = socket.inet_ntoa(ip.dst)
        if (src == ip1 and dst == ip2) or (src == ip2 and dst == ip1):
            conversation_count += 1
            print(f"Timestamp: {ts}")
            print(f"{src}:{tcp.sport} -> {dst}:{tcp.dport}")
            print(f"Sequence Number: {tcp.seq}")
            print(f"Acknowledgment Number: {tcp.ack}")
            print(f"Flags: {tcp.flags:#04x}")
            print(f"Payload Length: {len(tcp.data)}")
            if tcp.data:
                try:
                    text = tcp.data[:200].decode("utf-8")
                    print("Payload:", repr(text))
                except UnicodeDecodeError:
                    print("Payload: [binary data]")
            print("-" * 50)
    print("Total matching TCP packets:", conversation_count)

def main():
    filename = "cse.pcap"
    packets = []
    with open(filename, "rb") as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            packets.append((ts, buf))
    print("PCAP file loaded successfully:", filename)
    print("Total packets loaded:", len(packets))
    task_a(packets)
    task_b(packets)
    task_c(packets)
    task_d(packets)
    task_e(packets)
    task_f(packets)

if __name__ == "__main__":
    main()