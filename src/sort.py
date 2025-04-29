def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


if __name__ == "__main__":
    # Example usage
    data = [64, 34, 25, 12, 22, 11, 90]
    print("Unsorted array:", data)
    sorted_data = bubble_sort(data)
    print("Sorted array:", sorted_data)
    # Example usage with a larger dataset

    
