#Visualise the data from csv files in graphs using matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import statistics


#Plotting number of comparisons over the input size, for s = 10 (part c i)
def plot_comparisons_against_input_size():
    # Read data from CSV file
    input_sizes = []
    average_comparisons = []
    
    with open("comparison_against_input_size.csv", "r") as csvfile:
        next(csvfile)  # Skip header row
        for line in csvfile:
            size, avg_comp = line.strip().split(",")
            input_sizes.append(float(size))
            average_comparisons.append(int(avg_comp))
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(input_sizes, average_comparisons, marker='o', label = "S = 10")
    plt.title("Average Comparisons vs Input Size with S = 10")
    plt.xlabel("Input Size")
    plt.xscale("log")
    plt.ylabel("Average Comparisons")
    plt.xscale('log')
    plt.yscale('log')
    plt.gca().xaxis.set_major_formatter(ticker.LogFormatterMathtext())
    plt.xticks([3, 4, 5, 6, 7], [r"$10^3$", r"$10^4$", r"$10^5$", r"$10^6$", r"$10^7$"])
    plt.grid(True)
    plt.legend()
    plt.savefig("comparisons_vs_input_size.png")
    plt.show()
   
#Plotting of number of comparisons over the values of S, for input size = 10^6 (part c ii)
def plot_comparisons_against_s():
    # Read data from CSV file
    s_values = []
    comparisons_dict = {}
    
    with open("comparison_against_s.csv", "r") as csvfile:
        header = next(csvfile).strip().split(",")
        for line in csvfile:
            values = line.strip().split(",")
            s_values.append(int(values[0]))
            for i, comp in enumerate(values[1:]):
                if header[i + 1] not in comparisons_dict:
                    comparisons_dict[header[i + 1]] = []
                comparisons_dict[header[i + 1]].append(int(comp))
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    for input_size, comparisons in comparisons_dict.items():
        plt.plot(s_values, comparisons, marker='o', label="Input Size 10^6")
    
    plt.title("Comparisons vs S for Input size 10^6")
    plt.xlabel("S Value")
    plt.ylabel("Comparisons")
    plt.legend()
    plt.grid(True)
    plt.savefig("comparisons_vs_s.png")
    plt.show()
       
# Plotting bar graphs of median comparisons and median time for merge sort and hybrid sort
# Input size fixed at 10^6, S value fixed at 11 (part d)
def plot_merge_hybrid_comparisons_and_time():
    # Read data from CSV file
    algorithms = []
    median_comparisons = []
    median_times = []
    
    with open("merge_vs_hybrid.csv", "r") as csvfile:
        next(csvfile)  # Skip header row
        for line in csvfile:
            algo, median_comp, median_time = line.strip().split(",")
            algorithms.append(algo)
            median_comparisons.append(int(median_comp))
            median_times.append(float(median_time))
    
    # Plot the data
    x = range(len(algorithms))
    
    plt.figure(figsize=(12, 6))
    
    # Plot comparisons
    plt.subplot(1, 2, 1)
    plt.bar(x, median_comparisons, color='b', alpha=0.7)
    plt.xticks(x, algorithms)
    plt.title("Median Comparisons for Merge Sort and Hybrid Sort")
    plt.ylabel("Median Comparisons")
    
    # Plot time
    plt.subplot(1, 2, 2)
    plt.bar(x, median_times, color='g', alpha=0.7)
    plt.xticks(x, algorithms)
    plt.title("Median Time for Merge Sort and Hybrid Sort")
    plt.ylabel("Median Time (seconds)")
    
    plt.tight_layout()
    plt.savefig("merge_hybrid_comparisons_time.png")
    plt.show()

# Plotting of time taken over the values of S, for input size = 10^6, to find optimal S value (for part c iii)
def plot_time_against_s():
    # Read data from CSV file
    s_values = []
    time_dict = {}
    median_times = []
    
    with open("time_against_s_all.csv", "r") as csvfile:
        header = next(csvfile).strip().split(",")
        
        for line in csvfile:
            values = line.strip().split(",")
            s_values.append(int(values[0]))
            for i, time in enumerate(values[1:-1]):
                if values[0] not in time_dict:
                    time_dict[values[0]] = []
                time_dict[values[0]].append(float(time))
                
    for s, times in time_dict.items():
        median_times.append(statistics.median(times))
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(s_values, median_times, marker='o', label="Input Size 10^6")
    
    plt.title("Time vs S for Input Size 10^6")
    plt.xlabel("S Value")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.savefig("time_vs_s.png")
    plt.show()


# ----------Plot the data----------

plot_comparisons_against_input_size()
# plot_comparisons_against_s()
# plot_time_against_s()
# plot_merge_hybrid_comparisons_and_time()