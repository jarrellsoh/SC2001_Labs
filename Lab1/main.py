import statistics
import time
import csv
import random
from hybrid_sort import hybrid_sort
from Original_merge_sort import merge_sort

# Compare key comparisons over input size, value of S fixed at 10 (part c i)
def comparisons_against_input_size():

    #Fix S value at 10 for this comparison
    s = 10
    comparison_dict = {}

    # x values for 10^x
    exponent_values = [3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7]
    
    for i in range(5):
        print(f"Running comparison for iteration {i + 1}...")
        print("--------------------------------")
        # Iterate through each exponent value, store number of comparisons for each input size
        for x in exponent_values:
            # Generate unsorted data for each input size
            size = int(10 ** x)
            unsorted_data = [random.randint(1, size) for _ in range(size)]
            
            print(f"Running hybrid sort for input size 10^{x}...")
            #Sort the data using the hybrid sort
            comparisons = hybrid_sort(unsorted_data, 0, len(unsorted_data), s)
            
            #Store the number of comparisons for this input size
            if comparison_dict.get(x) is None:
                comparison_dict[x] = [comparisons]
            else:
                comparison_dict[x].append(comparisons)
                
    # Write average number of comparisons for each input size into a CSV file
    with open("comparison_against_input_size.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Input Size (10^x)", "Average Comparisons"])
        for x, comparisons in comparison_dict.items():
            average_comparisons = round(sum(comparisons) / len(comparisons))
            writer.writerow([x, average_comparisons])

# Compare key comparisons over value of S, input size fixed at 10^6 (part c ii)
def comparisons_against_s():
    comparison_dict = {}
    
    # Run comparisons for 5 iterations to get average comparisons for each value of S
    for i in range(5):
        print(f"Running comparison for iteration {i + 1}...")
        print("--------------------------------")
        
        #In each iteration, use the same randomly generated unsorted data to ensure consistency
        unsorted_data = [random.randint(1, 10**6) for _ in range(10**6)]
        
        #Compare key comparisons for S values from 1 to 100
        for s in range(1, 101):
            print(f"Running hybrid sort with S={s}...")
            
            
            # Sort the data using the hybrid sort with the current value of S
            data = unsorted_data.copy()  # Create a copy of the data to sort for each value of S
            print(data[-10:])  # Print the last 10 elements of the unsorted data
            comparisons = hybrid_sort(data, 0, len(data), s)
            print(data[-10:])  # Print the last 10 elements of the sorted data
            
            if comparison_dict.get(s) is None:
                comparison_dict[s] = [comparisons]
            else:
                comparison_dict[s].append(comparisons)

    # Write the average number of comparisons for each value of S to a CSV file
    with open("comparison_against_s.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["S", "Comparisons"])
        for s, comparisons in comparison_dict.items():
            average_comparisons = round(sum(comparisons) / len(comparisons))
            writer.writerow([s, average_comparisons])

# Compare merge sort and hybrid sort in terms of key comparisons
#Input size fixed at 10^7, and S value fixed at the optimal value of 11 (part d)
def compare_merge_hybrid():
    input_size = 10**7
    s = 11
    
    merge_comparison_list = []
    hybrid_comparison_list = []
    merge_time_list = []
    hybrid_time_list = []
    
    # Repeat comparison across 5 iterations to get the median time and comparisons for each algorithm
    for i in range(5):
        print(f"Running comparison for iteration {i + 1}...")
        print("--------------------------------")
        
        # Generate random unsorted data of size 10^7
        unsorted_data = [random.randint(1, input_size) for _ in range(input_size)]
        
        # Sort data using merge sort
        merge_data = unsorted_data.copy()
        
        start_time = time.perf_counter()
        print(merge_data[-10:])  # Print the last 10 elements of the unsorted data
        merge_comparisons = merge_sort(merge_data, 0, len(merge_data))
        print(merge_data[-10:])  # Print the last 10 elements of the sorted data
        end_time = time.perf_counter()
        merge_time = end_time - start_time
        
        # Add stats to the list
        merge_comparison_list.append(merge_comparisons)
        merge_time_list.append(merge_time)
        
        print("Merge Sort Completed in", merge_time, "seconds.")
        
        # Sort data using hybrid sort
        # No need to copy as this is the last sort operation
        start_time = time.perf_counter()
        print(unsorted_data[-10:])  # Print the last 10 elements of the unsorted data
        hybrid_comparisons = hybrid_sort(unsorted_data, 0, len(unsorted_data), s)
        print(unsorted_data[-10:])  # Print the last 10 elements of the sorted data
        end_time = time.perf_counter()
        hybrid_time = end_time - start_time
        
        #Add stats to the list
        hybrid_comparison_list.append(hybrid_comparisons)
        hybrid_time_list.append(hybrid_time)
        
        print("Hybrid Sort Completed in", hybrid_time, "seconds.")
    
    # Write all merge sort comparisons and timings on a separate CSV file
    with open("merge_comparisons_and_timings.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Iteration", "Comparisons", "Time (seconds)"])
        for i, (comparisons, curr_time) in enumerate(zip(merge_comparison_list, merge_time_list), start=1):
            writer.writerow([i, comparisons, curr_time])

    # Write all hybrid sort comparisons and timings on a separate CSV file
    with open("hybrid_comparisons_and_timings.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Iteration", "Comparisons", "Time (seconds)"])
        for i, (comparisons, curr_time) in enumerate(zip(hybrid_comparison_list, hybrid_time_list), start=1):
            writer.writerow([i, comparisons, curr_time])

    # Write median number of comparisons and time taken for both algorithms to a CSV file
    with open("merge_vs_hybrid.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Algorithm", "Comparisons", "Time (seconds)"])
        writer.writerow(["Merge Sort", statistics.median(merge_comparison_list), statistics.median(merge_time_list)])
        writer.writerow(["Hybrid Sort", statistics.median(hybrid_comparison_list), statistics.median(hybrid_time_list)])


# ----------Extra Functions for testing----------

# Compare time taken over value of S, input size fixed at 10^6 (used for part c iii)
def times_against_s():
    time_dict = {}
    
    # Run comparisons for 5 iterations to get median time for each value of S
    for i in range(5):
        print(f"Running comparison for iteration {i + 1}...")
        print("--------------------------------")
        
        #In each iteration, use the same randomly generated unsorted data to ensure consistency
        unsorted_data = [random.randint(1, 10**6) for _ in range(10**6)]
        
        #Compare time taken for S values from 1 to 100
        for s in range(1, 101):
            print(f"Running hybrid sort with S={s}...")
            
            # Sort the data using the hybrid sort with the current value of S and measure time taken
            data = unsorted_data.copy()  # Create a copy of the data to sort for each value of S
            start_time = time.perf_counter()
            hybrid_sort(data, 0, len(data), s)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            
            if time_dict.get(s) is None:
                time_dict[s] = [elapsed_time]
            else:
                time_dict[s].append(elapsed_time)

    # Write the all times and average time taken for each value of S to a CSV file
    with open("time_against_s_all.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["S", "Time (tun 1)", "Time (run 2)", "Time (run 3)", "Time (run 4)", "Time (run 5)", "Average Time"])
        for s, times in time_dict.items():
            average_time = round(sum(times) / len(times), 6)
            writer.writerow([s] + times + [average_time])

# Compare over s but for multiple input sizes
def compare_s_over_multiple_input_sizes():
    exponent_values = [3, 4, 5, 6]
    comparison_dict = {}
    for x in exponent_values:
        print(f"Running comparisons for input size 10^{x}...")
        print("--------------------------------")
        # Generate unsorted data for each input size
        size = int(10 ** x)
        unsorted_data = [random.randint(1, size) for _ in range(size)]
        
        # Compare key comparisons for S values from 1 to 20
        
        for s in range(1, 21):
            print(f"Running hybrid sort with S={s}...")
            # Sort the data using the hybrid sort with the current value of S
            data = unsorted_data.copy()  # Create a copy of the data to sort for each value of S
            comparisons = hybrid_sort(data, 0, len(data), s)
            
            if comparison_dict.get(s) is None:
                comparison_dict[s] = [comparisons]
            else:
                comparison_dict[s].append(comparisons)

    # Write number of comparisons for each value of S and for each input size into a CSV file
    filename = f"comparison_against_s_input_size_10^{x}.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["S", "10^3", "10^4", "10^5", "10^6", "10^7"])
        for s, comparisons in comparison_dict.items():
            writer.writerow([s] + comparisons)

# Compare multiple S over multiple input sizes, comparing number of comparisons and time taken
def find_optimal_s():
    exponent_values = [3, 4, 5, 6, 7]
    comparison_dict = {}
    times_dict = {}
    
    for x in exponent_values:
        print(f"Running comparisons for input size 10^{x}...")
        print("--------------------------------")
        # Generate unsorted data for each input size
        size = int(10 ** x)
        unsorted_data = [random.randint(1, size) for _ in range(size)]
        
        # Compare key comparisons for S values from 1 to 20
        for s in range(2, 21, 2):
            print(f"Running hybrid sort with S={s}...")
            # Sort the data using the hybrid sort with the current value of S
            data = unsorted_data.copy()  # Create a copy of the data to sort for each value of S
            start_time = time.perf_counter()
            comparisons = hybrid_sort(data, 0, len(data), s)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            
            if times_dict.get(s) is None:
                times_dict[s] = [elapsed_time]
            else:
                times_dict[s].append(elapsed_time)
            
            if comparison_dict.get(s) is None:
                comparison_dict[s] = [comparisons]
            else:
                comparison_dict[s].append(comparisons)

    # Write number of comparisons for each value of S and for each input size into a CSV file
    # Also write the time taken for each value of S and for each input size
    filename = f"comparison_against_s_input_size_10^{x}.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["S", "10^3 Comparisons", "10^4 Comparisons", "10^5 Comparisons", "10^6 Comparisons", "10^7 Comparisons",
                         "10^3 Time (s)", "10^4 Time (s)", "10^5 Time (s)", "10^6 Time (s)", "10^7 Time (s)"])
        for s in range(2, 21, 2):
            comparisons = comparison_dict.get(s, [])
            times = times_dict.get(s, [])
            writer.writerow([s] + comparisons + times)


def demonstrate_hybrid_sort(x, s):
    # Generate random unsorted data
    size = int(10 ** x)
    arr = [random.randint(1, size) for _ in range(size)]
    
    #Print first 10 and last 10 elements of unsorted array
    print("Unsorted array: ")
    print(arr[:10])
    print(arr[-10:])
    
    #Use hybrid sort
    start_time = time.perf_counter()
    comparisons = hybrid_sort(arr, 0, len(arr), s)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    
    #Print sorted array, number of comarions made, and time taken
    print("Sorted array:")
    print(arr[:10])
    print(arr[-10:])
    print("Time taken to sort:", elapsed_time, "seconds")
    print("Number of comparisons made:", comparisons)

# ----------Calling of functions----------

# comparisons_against_s()
# comparisons_against_input_size()
# compare_merge_hybrid()
# times_against_s()
# find_optimal_s()
# compare_s_over_multiple_input_sizes()
# find_optimal_s()
demonstrate_hybrid_sort(6, 10) # First argument is x for n = 10^x, second argument is S value


