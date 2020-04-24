import numpy as np

print("A. Create a 1d array M with values ranging from 2 to 26 and print M\n")
M = np.arange(2,27)
print(M)

print("\nB. Reshape M as a 5x5 matrix and print M\n")

M = np.arange(2,27).reshape(5,5)
print(M)

print("\nC. Set the first column of the matrix M to 0 and print M\n")

for i in range(5):
    M[i][0] = 0
print(M)

print("\nD. Assign M^2 to the M and print M.\n")

M = M @ M
print(M)

print("\nE. Now, let`s consider the first row of matrix M as vector v. calutate the magnitude of the vector v and print it\n")

V = M[0]
sum = 0
for i in range(5):
    sum += V[i]*V[i]

x = np.sqrt(sum)

print(x)


