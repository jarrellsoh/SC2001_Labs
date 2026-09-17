# Implementation of insertion sort portion of hybrid sort
def insertion_sort(arr, start, end, comparisons):
    for i in range(start + 1, end):
        curr = arr[i]
        j = i - 1
        
        # Compare downwards and shift elements right until correct position reached
        while j >= start:
            comparisons += 1
            if arr[j] > curr:
                arr[j+1] = arr[j]
                j -= 1
            # Correct position reached, break out of loop
            else:
                break
            
        # Place current element in correct position
        arr[j+1] = curr
    return comparisons


# Merge portion of hybrid sort        
def merge(arr, start, mid, end, comparisons):
    
    # Copy left and right subarrays as temporary arrays
    left_arr = arr[start:mid]
    right_arr = arr[mid:end]
    
    # i tracks current position in left_arr
    # j tracks current position in right_arr
    # k tracks position to write into original array
    i = j = 0
    k = start
    
    # Lengths of temporary arrays
    len_left = len(left_arr)
    len_right = len(right_arr)
    
    # Compare elements from left and right subarrays, merge in sorted order
    while i < len_left and j < len_right:
        comparisons += 1
        
        # Append smaller element to result, increment index of that subarray
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
            
        # Move to next position in original array
        k += 1
        
    # Append remaining elements of the remaining subarray, if any
    if i < len_left:
        arr[k:end] = left_arr[i:]
    if j < len_right:
        arr[k:end] = right_arr[j:]
    
    return comparisons

    
#Main calling function for hybrid sort
def hybrid_sort(arr, start, end, s, comparisons = 0):
    length = end - start
    if length <= s:
        #If the array is small enough, switch to insertion sort
        return insertion_sort(arr, start, end, comparisons)
    else:
        #Recusively split the array into halves and sort each half
        mid = (start + end)//2
        comparisons = hybrid_sort(arr, start, mid, s, comparisons)
        comparisons = hybrid_sort(arr, mid, end, s, comparisons)
        return merge(arr, start, mid, end, comparisons)


# ----------Calling of hybrid sort for testing----------

#array of length 20
# arr = [12, 11, 13, 5, 6, 7, 3, 1, 9, 10, 15, 14, 8, 4, 2, 16, 18, 17, 20, 19]

# #S-value, the size of subarray where sorting changes to insertion sort
# s = 5

# comparisons = hybrid_sort(arr, 0, len(arr), s)
# print(arr, comparisons)