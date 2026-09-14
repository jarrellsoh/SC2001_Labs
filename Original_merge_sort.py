import time

def merge(arr, start, mid, end):
    # Count the number of key comparisons made
    comparisons = 0

    # Copy the left half into a temporary array
    # start is included, mid is excluded
    left_arr = arr[start:mid]

    # Copy the right half into another temporary array
    # mid is included, end is excluded
    right_arr = arr[mid:end]

    # i tracks the current position in left_arr
    # j tracks the current position in right_arr
    # k tracks the position to write into the original array
    i = 0
    j = 0
    k = start

    # Continue while both temporary arrays still have elements
    while i < len(left_arr) and j < len(right_arr):

        # Compare one key from the left side with one key from the right side
        comparisons += 1

        # Place the smaller element into the original array
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1

        # Move to the next position in the original array
        k += 1

    # If there are leftover elements in the left half,
    # copy them directly into the original array
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1

    # If there are leftover elements in the right half,
    # copy them directly into the original array
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1

    # Return the number of comparisons made during this merge
    return comparisons


def merge_sort(arr, start, end):
    # Store the total number of comparisons
    comparisons = 0

    # Base case:
    # if the current section has 0 or 1 element,
    # it is already sorted
    if end - start <= 1:
        return comparisons

    # Find the midpoint of the current section
    mid = start + (end - start) // 2

    # Recursively sort the left half
    # Range: start up to, but not including, mid
    comparisons += merge_sort(arr, start, mid)

    # Recursively sort the right half
    # Range: mid up to, but not including, end
    comparisons += merge_sort(arr, mid, end)

    # Merge the two sorted halves back together
    comparisons += merge(arr, start, mid, end)

    # Return the total number of key comparisons
    return comparisons



#------------------------------------------------------------
# Test array (comment out when not in use or remove after)
arr = [5, 2, 8, 1, 3]

# Record the CPU time before sorting starts
start_time = time.process_time()

# Sort the full array
# start = 0
# end = len(arr), because end is exclusive
comparisons = merge_sort(arr, 0, len(arr))

# Record the CPU time after sorting finishes
end_time = time.process_time()

# Calculate how much CPU time the sorting took
cpu_time = end_time - start_time 

# Display the result
print("Sorted array:", arr)
print("Key comparisons:", comparisons)
print("CPU time:", cpu_time, "seconds")
#------------------------------------------------------------
