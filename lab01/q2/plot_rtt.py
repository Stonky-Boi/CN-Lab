import matplotlib.pyplot as plt

def read_file(filename):
    iterations = []
    rtts = []
    with open(filename) as f:
        next(f)
        for line in f:
            i, rtt = line.split()
            iterations.append(int(i))
            rtts.append(float(rtt))
    return iterations, rtts

google_x, google_y = read_file("google_com_rtt.txt")
wikipedia_x, wikipedia_y = read_file("wikipedia_org_rtt.txt")

plt.plot(
    google_x,
    google_y,
    marker="o",
    label="Google"
)
plt.plot(
    wikipedia_x,
    wikipedia_y,
    marker="o",
    label="Wikipedia"
)

plt.xlabel("Iteration")
plt.ylabel("Final Hop RTT (ms)")
plt.title("Traceroute RTT over 10 Iterations")

plt.legend()
plt.grid(True)

plt.savefig("rtt_comparison.png")
plt.show()