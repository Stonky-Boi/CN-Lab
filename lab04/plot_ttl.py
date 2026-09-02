import matplotlib.pyplot as plt

def read_file(filename):
    iterations = []
    ttls = []
    with open(filename) as f:
        next(f)
        for line in f:
            i, ttl = line.strip().split(",")
            iterations.append(int(i))
            ttls.append(float(ttl))
    return iterations, ttls
iterations, ttl = read_file("q7.txt")

plt.plot(
    iterations,
    ttl,
    marker="o",
    label="www.iitb.ac.in"
)

plt.xlabel("Iteration")
plt.ylabel("TTL (seconds)")
plt.title("DNS TTL over 10 Iterations")

plt.legend()
plt.grid(True)

plt.savefig("q7.png")
plt.show()