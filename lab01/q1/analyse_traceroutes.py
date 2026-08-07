import re
import glob
import ipaddress
import statistics

def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except:
        return False

def parse_traceroute(filename):
    data = {
        "website": filename.replace("_com.txt", ".com"),
        "destination": None,
        "hops": [],
        "rtts": [],
        "missing_hops": 0
    }
    with open(filename, "r", errors="ignore") as f:
        lines = f.readlines()
    for line in lines:
        # Extract destination IP
        if "traceroute to" in line:
            match = re.search(r"\(([\d.]+)\)", line)
            if match:
                data["destination"] = match.group(1)
        # Extract hop lines
        hop_match = re.match(r"\s*(\d+)\s+(.*)", line)
        if hop_match:
            hop_number = int(hop_match.group(1))
            content = hop_match.group(2)
            # Extract IP addresses
            ips = re.findall(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                content
            )
            # Extract RTT values
            rtts = re.findall(
                r"(\d+\.\d+)\s*ms",
                content
            )
            if "*" in content:
                data["missing_hops"] += 1
            hop = {
                "number": hop_number,
                "ips": ips,
                "rtt": [
                    float(x)
                    for x in rtts
                ]
            }
            data["hops"].append(hop)
            data["rtts"].extend(
                [
                    float(x)
                    for x in rtts
                ]
            )
    return data

def analyze(data):
    route = []
    private = []
    public = []
    for hop in data["hops"]:
        for ip in hop["ips"]:
            route.append(ip)
            if is_private_ip(ip):
                private.append(ip)
            else:
                public.append(ip)
    rtts = data["rtts"]
    result = {
        "Website": data["website"],
        "Destination": data["destination"],
        "Hops": len(data["hops"]),
        "Missing": data["missing_hops"],
        "RTT Samples": len(rtts),
        "Min RTT(ms)": round(min(rtts), 2) if rtts else "-",
        "Max RTT(ms)": round(max(rtts), 2) if rtts else "-",
        "Average RTT(ms)": round(statistics.mean(rtts), 2) if rtts else "-",
        "Private Hops": len(private),
        "Public Hops": len(public),
        "Route": route
    }
    return result

# -------------------------
# Main analysis
# -------------------------
results = []
routes = []
files = sorted(glob.glob("*_com.txt"))
if not files:
    print("No traceroute files found")
    exit()
for file in files:
    print("Analyzing:", file)
    parsed = parse_traceroute(file)
    result = analyze(parsed)
    results.append(result)
    routes.append(
        set(result["Route"])
    )

# -------------------------
# Common routers
# -------------------------
common_routes = set.intersection(*routes)

# -------------------------
# Generate main report
# -------------------------
with open(
    "traceroute_analysis.md",
    "w"
) as f:
    f.write("# Traceroute Analysis Report\n\n")
    headers = [
        "Website",
        "Destination",
        "Hops",
        "Missing",
        "RTT Samples",
        "Min RTT(ms)",
        "Max RTT(ms)",
        "Average RTT(ms)",
        "Private Hops",
        "Public Hops"
    ]
    f.write("| " + " | ".join(headers) + " |\n")
    f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")

    for r in results:
        row = [
            r["Website"],
            r["Destination"],
            r["Hops"],
            r["Missing"],
            r["RTT Samples"],
            r["Min RTT(ms)"],
            r["Max RTT(ms)"],
            r["Average RTT(ms)"],
            r["Private Hops"],
            r["Public Hops"]
        ]
        f.write("| " + " | ".join(map(str,row)) + " |\n")

# -------------------------
# Route report
# -------------------------
with open(
    "route_consistency.md",
    "w"
) as f:
    f.write("# Route Consistency Analysis\n\n")
    f.write("## Routers appearing in ALL routes\n\n")
    f.write("| Router IP |\n")
    f.write("| --- |\n")
    for ip in sorted(common_routes):
        f.write(f"| {ip} |\n")
    f.write("\n\n## Full Routes\n\n")
    for r in results:
        f.write(f"### {r['Website']}\n\n")
        f.write("```\n")
        f.write(" -> ".join(r["Route"]))
        f.write("\n```\n\n")

# -------------------------
# Console summary
# -------------------------
print("\n==============================")
print("COMMON ROUTERS")
print("==============================")
for ip in sorted(common_routes):
    print(ip)
print("\n==============================")
print("SUMMARY")
print("==============================")
for r in results:
    print(
        f"{r['Website']:20}"
        f"Hops: {r['Hops']:3} "
        f"Avg RTT: {r['Average RTT(ms)']} ms"
    )
print("\nGenerated:")
print(" - traceroute_analysis.md")
print(" - route_consistency.md")