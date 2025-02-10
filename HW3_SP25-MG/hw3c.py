#region imports
import numpy as np
from DoolittleMethod import Doolittle
from matrixOperations import Transpose, MatrixMultiply
#endregion

#region function definitions
def is_symmetric(A):
    """
    Checks if the matrix A is symmetric.
    :param A: Square matrix
    :return: True if symmetric, False otherwise
    """
    return np.allclose(A, Transpose(A))

def is_positive_definite(A):
    """
    Checks if the matrix A is positive definite.
    :param A: Square matrix
    :return: True if positive definite, False otherwise
    """
    try:
        np.linalg.cholesky(A)
        return True
    except np.linalg.LinAlgError:
        return False

def cholesky_solve(A, b):
    """
    Solves Ax = b using the Cholesky decomposition method.
    :param A: Symmetric positive definite matrix
    :param b: Right-hand side vector
    :return: Solution vector x
    """
    L = np.linalg.cholesky(A)  # Get lower triangular matrix L
    y = np.linalg.solve(L, b)  # Solve L * y = b
    x = np.linalg.solve(L.T, y)  # Solve L.T * x = y
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