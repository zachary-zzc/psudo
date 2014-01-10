def bubble(arr):
    for i in range(1, len(arr)):
        for j in range(len(arr) - i):
            print(j)
            if arr[j+1] < arr[j]:
                tmp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = tmp
