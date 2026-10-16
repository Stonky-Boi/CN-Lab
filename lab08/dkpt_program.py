import dpkt
import socket

filename = "cse.pcap"
unique_ips = set()
tcp_flag_details = []
syn_requests = set()
completed_handshakes = set()
syn_ack_responses = set()
detected_ports = set()
xmas_scans = set()

with open(filename, 'rb') as f:
    pcap = dpkt.pcap.Reader(f)

    for timestamp, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            if not isinstance(eth.data, dpkt.ip.IP):
                continue
            ip = eth.data
            src_ip = socket.inet_ntoa(ip.src)
            dst_ip = socket.inet_ntoa(ip.dst)
            unique_ips.add(src_ip)
            unique_ips.add(dst_ip)

            if isinstance(ip.data, dpkt.tcp.TCP):
                tcp = ip.data
                flags = tcp.flags
                tcp_flag_details.append((flags, src_ip, dst_ip))
                if tcp.dport > 100:
                    detected_ports.add((tcp.dport, src_ip, dst_ip))
                if (flags & dpkt.tcp.TH_FIN and flags & dpkt.tcp.TH_PUSH and flags & dpkt.tcp.TH_URG):
                    xmas_scans.add((src_ip, dst_ip))
                connection = (src_ip, tcp.sport, dst_ip, tcp.dport)
                reverse_connection = (dst_ip, tcp.dport, src_ip, tcp.sport)
                if (flags & dpkt.tcp.TH_SYN and not flags & dpkt.tcp.TH_ACK):
                    syn_requests.add(connection)
                if (flags & dpkt.tcp.TH_SYN and flags & dpkt.tcp.TH_ACK):
                    syn_ack_responses.add(reverse_connection)
                if (flags & dpkt.tcp.TH_ACK and not flags & dpkt.tcp.TH_SYN):
                    if connection in syn_ack_responses:
                        completed_handshakes.add(connection)

        except (dpkt.UnpackError, AttributeError):
            continue

print("\n1. Unique IP Addresses:")
for ip in sorted(unique_ips):
    print(ip)

print("\n2. TCP Flags and Associated IP Addresses:")
flag_names = {
    dpkt.tcp.TH_FIN: "FIN",
    dpkt.tcp.TH_SYN: "SYN",
    dpkt.tcp.TH_RST: "RST",
    dpkt.tcp.TH_PUSH: "PSH",
    dpkt.tcp.TH_ACK: "ACK",
    dpkt.tcp.TH_URG: "URG",
    dpkt.tcp.TH_ECE: "ECE",
    dpkt.tcp.TH_CWR: "CWR"
}
for flags, src, dst in tcp_flag_details:
    active_flags = [
        name for flag, name in flag_names.items()
        if flags & flag
    ]
    print(active_flags, src, "->", dst)

print("\n3. Successfully Completed TCP Handshakes:")
for conn in sorted(completed_handshakes):
    print(conn[0], "->", conn[2])

print("\n4. SYN Sent but Handshake Not Completed:")
for conn in sorted(syn_requests - completed_handshakes):
    print(conn[0], "->", conn[2])

print("\n5. Port Detected:")
for port, src, dst in sorted(detected_ports):
    print("Port detected:", port, src, "->", dst)

print("\n6. Xmas Scan Detected:")
for src, dst in sorted(xmas_scans):
    print("Xmas scan detected:", src, "->", dst)