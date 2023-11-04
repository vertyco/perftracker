import cProfile
import timeit
from time import sleep

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from perftracker import perf


def measure_overhead(func, iterations=100):
    # Define the function with different performance tracking packages
    @perf(max_entries=100)
    def func_with_perf():
        func()

    def func_with_cProfile():
        pr = cProfile.Profile()
        pr.enable()
        func()
        pr.disable()
        return pr.getstats()

    # Measure overhead for each package
    overhead_perf = []
    overhead_cProfile = []
    overhead_none = []

    for _ in range(iterations):
        start_time = timeit.default_timer()
        func_with_perf()
        overhead_perf.append((timeit.default_timer() - start_time) * 1000)

        start_time = timeit.default_timer()
        func_with_cProfile()
        overhead_cProfile.append((timeit.default_timer() - start_time) * 1000)

        start_time = timeit.default_timer()
        func()
        overhead_none.append((timeit.default_timer() - start_time) * 1000)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(overhead_perf, label="PerfTracker")
    plt.plot(overhead_cProfile, label="cProfile")
    plt.plot(overhead_none, label="None")

    min_val = min(min(overhead_perf), min(overhead_cProfile), min(overhead_none))
    max_val = max(max(overhead_perf), max(overhead_cProfile), max(overhead_none))
    plt.ylim([min_val, max_val])
    formatter = FormatStrFormatter("%.2f")
    plt.gca().yaxis.set_major_formatter(formatter)

    plt.xlabel("Iterations")
    plt.ylabel("Overhead (milliseconds)")
    plt.title("Overhead of Performance Tracking Packages")
    plt.legend()
    plt.grid(True)

    # Save the plot
    plt.savefig(".github/ASSETS/overhead_comparison_test.png")


# Test function
def my_function():
    for _ in range(10000):
        sleep(0)


# Run the comparison
measure_overhead(my_function)
