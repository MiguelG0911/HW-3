#region imports
from DoolittleMethod import Doolittle
from matrixOperations import Transpose
#endregion

#region function definitions
def is_symmetric(A):
    """
    Checks if the matrix A is symmetric.
    :param A: Square matrix
    :return: True if symmetric, False otherwise
    """
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != A[j][i]:
                return False
    return True

def is_positive_definite(A):
    """
    Checks if the matrix A is positive definite.
    :param A: Square matrix
    :return: True if positive definite, False otherwise
    """
    n = len(A)
    for i in range(n):
        # Check if the leading principal minors are positive
        sub_matrix = [row[:i+1] for row in A[:i+1]]
        det = determinant(sub_matrix)
        if det <= 0:
            return False
    return True

def determinant(matrix):
    """
    Computes the determinant of a square matrix using recursive expansion by minors.
    :param matrix: Square matrix
    :return: Determinant of the matrix
    """
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for col in range(n):
        sub_matrix = [row[:col] + row[col+1:] for row in matrix[1:]]
        det += ((-1) ** col) * matrix[0][col] * determinant(sub_matrix)
    return det

def cholesky_decomposition(A):
    """
    Performs Cholesky decomposition on a symmetric positive definite matrix A.
    :param A: Symmetric positive definite matrix
    :return: Lower triangular matrix L such that A = L * L^T
    """
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            if i == j:
                sum_k = sum(L[i][k] ** 2 for k in range(j))
                L[i][j] = (A[i][i] - sum_k) ** 0.5
            else:
                sum_k = sum(L[i][k] * L[j][k] for k in range(j))
                L[i][j] = (A[i][j] - sum_k) / L[j][j]
    return L

def forward_substitution(L, b):
    """
    Solves the system L * y = b using forward substitution.
    :param L: Lower triangular matrix
    :param b: Right-hand side vector
    :return: Solution vector y
    """
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][j] * y[j] for j in range(i))) / L[i][i]
    return y

def backward_substitution(U, y):
    """
    Solves the system U * x = y using backward substitution.
    :param U: Upper triangular matrix
    :param y: Right-hand side vector
    :return: Solution vector x
    """
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

def cholesky_solve(A, b):
    """
    Solves Ax = b using the Cholesky decomposition method.
    :param A: Symmetric positive definite matrix
    :param b: Right-hand side vector
    :return: Solution vector x
    """
    L = cholesky_decomposition(A)  # Get lower triangular matrix L
    y = forward_substitution(L, b)  # Solve L * y = b
    x = backward_substitution(Transpose(L), y)  # Solve L^T * x = y
    return x

def main():
    """
    This program determines whether to use the Cholesky or Doolittle method
    to solve Ax = b and prints the solution.
    """
    matrices = [
        {
            "A": [[1, -1, 3, 2], [-1, 5, -5, -2], [3, -5, 19, 3], [2, -2, 3, 21]],
            "b": [15, -35, 94, 1]
        },
        {
            "A": [[4, 2, 4, 0], [2, 2, 3, 2], [4, 3, 6, 3], [0, 2, 3, 9]],
            "b": [20, 36, 60, 122]
        }
    ]

    for i, problem in enumerate(matrices, 1):
        A = problem["A"]
        b = problem["b"]

        print(f"\nProblem {i}:")
        print("Matrix A:")
        for row in A:
            print(row)

        print("Vector b:", b)

        if is_symmetric(A) and is_positive_definite(A):
            print("Using Cholesky method...")
            x = cholesky_solve(A, b)
        else:
            print("Using Doolittle method...")
            augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]  # Convert to augmented form
            x = Doolittle(augmented_matrix)

        print("Solution vector x:", [round(val, 3) for val in x])

#endregion

if __name__ == "__main__":
    main()
