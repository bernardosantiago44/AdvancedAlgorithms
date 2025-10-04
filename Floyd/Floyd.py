from __future__ import annotations
import math
from typing import List, Tuple

# --- Matriz 20x20 incrustada (del enunciado) ---
MATRIX: List[List[float]] = [
    [ 0, 3,-2, 4, 7, 1,-3, 2, 6, 9, 4,-5, 7, 8, 3, 1, 5, 6,-4, 2],
    [ 3, 0, 5, 2,-1, 4, 7, 2, 1, 6,-3, 2, 8, 4, 1, 5, 7,-2, 6, 3],
    [-2, 5, 0, 3, 4,-1, 2, 7, 3, 1, 2, 4,-3, 6, 5, 8, 2, 4, 7, 1],
    [ 4, 2, 3, 0, 5, 6, 7,-2, 8, 1, 4, 3, 2, 9, 1, 4, 5, 6, 2, 7],
    [ 7,-1, 4, 5, 0, 2, 3, 8, 9, 4, 7, 1, 5, 6, 8, 3, 1, 5, 2, 6],
    [ 1, 4,-1, 6, 2, 0, 5, 3, 1, 8, 2, 7, 6,-2, 4, 5, 7, 2, 3, 8],
    [-3, 7, 2, 7, 3, 5, 0, 4, 2, 6, 1, 8, 2, 7, 9, 4, 1, 5, 2, 7],
    [ 2, 2, 7,-2, 8, 3, 4, 0, 5, 1, 2, 7, 9, 6, 2, 5, 7, 8, 2, 3],
    [ 6, 1, 3, 8, 9, 1, 2, 5, 0, 2, 4, 7, 8, 1, 6, 3, 5, 7, 2, 9],
    [ 9, 6, 1, 1, 4, 8, 6, 1, 2, 0, 7, 2, 5, 8, 3, 7, 9, 4, 1, 2],
    [ 4,-3, 2, 4, 7, 2, 1, 2, 4, 7, 0, 6, 8, 2, 3, 9, 4, 5, 1, 7],
    [-5, 2, 4, 3, 1, 7, 8, 7, 7, 2, 6, 0, 3, 1, 6, 7, 2, 5, 4, 8],
    [ 7, 8,-3, 2, 5, 6, 2, 9, 8, 5, 8, 3, 0, 6, 7, 5, 8, 2, 3, 7],
    [ 8, 4, 6, 9, 6,-2, 7, 6, 1, 8, 2, 1, 6, 0, 9, 4, 5, 7, 2, 3],
    [ 3, 1, 5, 1, 8, 4, 9, 2, 6, 3, 3, 6, 7, 9, 0, 3, 6, 7, 8, 4],
    [ 1, 5, 8, 4, 3, 5, 4, 5, 3, 7, 9, 7, 5, 4, 3, 0, 2, 1, 7, 6],
    [ 5, 7, 2, 5, 1, 7, 1, 7, 5, 9, 4, 2, 8, 5, 6, 2, 0, 4, 7, 3],
    [ 6,-2, 4, 6, 5, 2, 5, 8, 7, 4, 5, 5, 2, 7, 7, 1, 4, 0, 5, 2],
    [-4, 6, 7, 2, 2, 3, 2, 2, 2, 1, 1, 4, 3, 2, 8, 7, 7, 5, 0, 4],
    [ 2, 3, 1, 7, 6, 8, 7, 3, 9, 2, 7, 8, 7, 3, 4, 6, 3, 2, 4, 0],
]

def floyd_warshall_with_row_stats(matrix: List[List[float]]) -> Tuple[List[List[float]], int]:
    """
    Aplica Floyd-Warshall y cuenta (comparaciones + actualizaciones)
    SOLO sobre la última fila (fila N). Devuelve (distancias, total_ops_fila_N).
    """
    n = len(matrix)
    if n == 0:
        return [], 0

    dist = [row[:] for row in matrix]
    for i in range(n):
        dist[i][i] = 0

    target_row = n - 1
    comparisons = 0
    updates = 0

    for k in range(n):
        dist_k = dist[k]
        for i in range(n):
            row_i = dist[i]
            dik = row_i[k]
            for j in range(n):
                candidate = dik + dist_k[j]
                if i == target_row:
                    comparisons += 1
                if candidate < row_i[j]:
                    row_i[j] = candidate
                    if i == target_row:
                        updates += 1

    return dist, comparisons + updates

def main() -> None:
    dist, operations = floyd_warshall_with_row_stats(MATRIX)

    print("Matriz D(20):")
    for row in dist:
        print(" ".join(str(int(x)) if not math.isinf(x) else "inf" for x in row))
    print(f"Floyd realizó {operations} operaciones")

if __name__ == "__main__":
    main()
