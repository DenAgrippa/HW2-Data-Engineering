import json
import numpy as np

matrix = np.load('./data/first_task.npy')

size = matrix.size

matrix_props = {
    'sum': 0,
    'avg': 0,
    'sumMD': 0,
    'avgMD': 0,
    'sumSD': 0,
    'avgSD': 0,
    'max': matrix[0][0],
    'min': matrix[0][0]
}

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        el = matrix[i][j]
        matrix_props['sum'] += el
        if i == j:
            matrix_props['sumMD'] += el
        if j == matrix.shape[1] - i - 1:
            matrix_props['sumSD'] += el
        
        if matrix_props['max'] < el:
            matrix_props['max'] = el
        if matrix_props['min'] > el:
            matrix_props['min'] = el

matrix_props['avg'] = matrix_props['sum'] / size
matrix_props['avgMD'] = matrix_props['sumMD'] / matrix.shape[0]
matrix_props['avgSD'] = matrix_props['sumSD'] / matrix.shape[1]

for key in matrix_props.keys():
    matrix_props[key] = float(matrix_props[key])

with open('./results/first_task_result.json', "w", encoding="utf-8") as f:
    json.dump(matrix_props, f)

norm_matrix = matrix / matrix_props['sum']
np.save("./results/first_task_result_matrix.npy", norm_matrix)

print(np.load("./results/first_task_result_matrix.npy").sum())