import numpy as np


#creating 1D array
s = []
arr_s=int(input("Enter the size of the array: "))
for i in range(arr_s):
    element = int(input("Enter the element: "))
    s.append(element)
arr2 = np.array(s)
print(arr2)
print(f'dimension of this array is {arr2.ndim}')

#creating 2D array
row_s = int(input("enter the number of rows: "))
column_s = int(input("enter the number of columns: "))
arr3 = []
for i in range(row_s):
    row = []
    for j in range(column_s):
        element = int(input(f"Enter the element: "))
        row.append(element)
    arr3.append(row)
arr3 = np.array(arr3)
print(arr3)
print(f'dimension of this array is {arr3.ndim}')

#Arithmetic operations

array1 = np.array([1, 2, 3, 4])
array2 = np.array([5, 6, 7, 8])
print("array1: ", array1)
print("array2: ", array2)
print("addition of two arrays: ", np.add(array1, array2))
print("subtraction of two arrays: ", np.subtract(array1, array2))
print("multiplication of two arrays: ", np.multiply(array1, array2))
print("division of two arrays: ", np.divide(array1, array2))
print("power of two arrays: ", np.power(array1, array2))
print("modulus of two arrays: ", np.mod(array1, array2))

#Find the maximum, minimum, mean, and sum of an array.
print(array1)
print("maximum of the array: ", np.max(array1))
print("minimum of the array: ", np.min(array1)) 
print("mean of the array: ", np.mean(array1))
print("sum of the array: ", np.sum(array1))

#Reshape arrays into different dimensions.
print("array: ", array1)
ar = array1.reshape(2, 2)
print("reshaped array in 2D: ", ar)

ar2 = ar.reshape(-1)
print("reshaped array back to 1D: ", ar2)

ar3 = ar2.reshape(1,2,2)
print("reshaped array in 3D: ", ar3)

ar4 = ar3.reshape(2,1,-1)
print("reshaped array in 3D using -1: ", ar4)


#Slice and index arrays.

one_d_array = np.array([10, 20, 30, 40, 50])
print("array(1D): ", one_d_array[::])
print("array reversed: ", one_d_array[::-1])
print("array sliced: ", one_d_array[1:2])

index = int(input("Enter the index(0-4): "))
print(one_d_array[index])

two_d_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("array(2D): ", two_d_array[:: , ::])
print("array reversed: ", two_d_array[::-1, ::-1])
print("array sliced: ", two_d_array[1:2, 1:2])
print("array sliced: ", two_d_array[2, ::2]) 
index1 = int(input("Enter the row index(0-2): "))
index2 = int(input("Enter the column index(0-2): "))
print(two_d_array[index1, index2])



