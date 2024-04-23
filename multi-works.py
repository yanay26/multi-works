import numpy as np
from multiprocessing import Pool, cpu_count

# Функция перемножения элементов матриц
def element(index, A, B, result_filename):
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    # Открываем файл для записи результатов
    with open(result_filename, 'a') as result_file:
        result_file.write(f"{res}\n")
    return res

# Функция для распараллеливания вычислений
def parallel_multiply_matrices(A, B, result_filename):
    if len(A[0]) != len(B):
        raise ValueError("Количество столбцов матрицы A должно быть равно количеству строк матрицы B")

    # Создаем список индексов для каждого элемента результирующей матрицы
    indices = [(i, j) for i in range(len(A)) for j in range(len(B[0]))]

    # Создаем пул процессов, используя количество доступных ядер процессора
    with Pool(cpu_count()) as pool:
        # Выполняем перемножение элементов матриц параллельно с помощью функции element
        result_elements = pool.starmap(element, [(index, A, B, result_filename) for index in indices])

    # Преобразуем список результатов в матрицу
    result_matrix = np.reshape(result_elements, (len(A), len(B[0])))

    return result_matrix

def read_matrix_from_file(filename):
    # Чтение матрицы из файла
    with open(filename, 'r') as file:
        matrix = [[int(num) for num in line.split()] for line in file.readlines()]
    return np.array(matrix)

def write_matrix_to_file(matrix, filename):
    # Запись матрицы в файл
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')

if __name__ == '__main__':
    a, b = map(int, input("For matrix1, a,b: ").split())
    c, d = map(int, input("For matrix2, c,d: ").split())

    # Создаем две случайные матрицы размером a x b и c x d
    A = np.random.randint(0, 10, size=(a, b))
    B = np.random.randint(0, 10, size=(c, d))

    try:
        # Выполняем перемножение матриц с использованием многопроцессорности
        result_filename = "result.txt"
        with open(result_filename, "w") as result_file:
            # Очищаем файл перед записью новых результатов
            result_file.truncate(0)
        result = parallel_multiply_matrices(A, B, result_filename)

        # Читаем результат из промежуточного файла
        with open(result_filename, 'r') as result_file:
            result_matrix = [[int(line.strip()) for line in result_file.readlines()]]

        # Выводим результат
        print("Matrix A:")
        print(A)
        print("\nMatrix B:")
        print(B)
        print("\nResult:")
        print(result_matrix)

        # Записываем результат в файл
        write_matrix_to_file(result_matrix, "result_matrix.txt")
    except ValueError as e:
        print(e)