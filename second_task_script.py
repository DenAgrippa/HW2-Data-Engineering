import os
import json
import numpy as np

matrix = np.load("./data/second_task.npy")

x = []
y = []
z = []

for i in range(matrix.shape[0]):
    for j in range (matrix.shape[1]):
        if matrix[i][j] > 565:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez("./results/second_task_result.npz", x=x, y=y, z=z)
np.savez_compressed("./results/second_task_result_compressed.npz", x=x, y=y, z=z)

savez_size = os.path.getsize("./results/second_task_result.npz")
savez_compressed_size = os.path.getsize("./results/second_task_result_compressed.npz")

print(f"savez = {savez_size}")
print(f"savez_compressed = {savez_compressed_size}")
print(savez_size - savez_compressed_size)
