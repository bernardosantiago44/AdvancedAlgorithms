from __future__ import annotations

import heapq
import math
from typing import Iterable, List, Sequence, Tuple

# --- Matriz 20x20 incrustada (del enunciado) ---
MATRIX: List[List[float]] = [
    [0, 3, -2, 4, 7, 1, -3, 2, 6, 9, 4, -5, 7, 8, 3, 1, 5, 6, -4, 2],
    [3, 0, 5, 2, -1, 4, 7, 2, 1, 6, -3, 2, 8, 4, 1, 5, 7, -2, 6, 3],
    [-2, 5, 0, 3, 4, -1, 2, 7, 3, 1, 2, 4, -3, 6, 5, 8, 2, 4, 7, 1],
    [4, 2, 3, 0, 5, 6, 7, -2, 8, 1, 4, 3, 2, 9, 1, 4, 5, 6, 2, 7],
    [7, -1, 4, 5, 0, 2, 3, 8, 9, 4, 7, 1, 5, 6, 8, 3, 1, 5, 2, 6],
    [1, 4, -1, 6, 2, 0, 5, 3, 1, 8, 2, 7, 6, -2, 4, 5, 7, 2, 3, 8],
    [-3, 7, 2, 7, 3, 5, 0, 4, 2, 6, 1, 8, 2, 7, 9, 4, 1, 5, 2, 7],
    [2, 2, 7, -2, 8, 3, 4, 0, 5, 1, 2, 7, 9, 6, 2, 5, 7, 8, 2, 3],
    [6, 1, 3, 8, 9, 1, 2, 5, 0, 2, 4, 7, 8, 1, 6, 3, 5, 7, 2, 9],
    [9, 6, 1, 1, 4, 8, 6, 1, 2, 0, 7, 2, 5, 8, 3, 7, 9, 4, 1, 2],
    [4, -3, 2, 4, 7, 2, 1, 2, 4, 7, 0, 6, 8, 2, 3, 9, 4, 5, 1, 7],
    [-5, 2, 4, 3, 1, 7, 8, 7, 7, 2, 6, 0, 3, 1, 6, 7, 2, 5, 4, 8],
    [7, 8, -3, 2, 5, 6, 2, 9, 8, 5, 8, 3, 0, 6, 7, 5, 8, 2, 3, 7],
    [8, 4, 6, 9, 6, -2, 7, 6, 1, 8, 2, 1, 6, 0, 9, 4, 5, 7, 2, 3],
    [3, 1, 5, 1, 8, 4, 9, 2, 6, 3, 3, 6, 7, 9, 0, 3, 6, 7, 8, 4],
    [1, 5, 8, 4, 3, 5, 4, 5, 3, 7, 9, 7, 5, 4, 3, 0, 2, 1, 7, 6],
    [5, 7, 2, 5, 1, 7, 1, 7, 5, 9, 4, 2, 8, 5, 6, 2, 0, 4, 7, 3],
    [6, -2, 4, 6, 5, 2, 5, 8, 7, 4, 5, 5, 2, 7, 7, 1, 4, 0, 5, 2],
    [-4, 6, 7, 2, 2, 3, 2, 2, 2, 1, 1, 4, 3, 2, 8, 7, 7, 5, 0, 4],
    [2, 3, 1, 7, 6, 8, 7, 3, 9, 2, 7, 8, 7, 3, 4, 6, 3, 2, 4, 0],
]


def floyd_warshall_with_row_stats(
    matrix: Sequence[Sequence[float]],
    target_row: int | None = None,
) -> Tuple[List[List[float]], int]:
    """Aplica Floyd-Warshall y contabiliza comparaciones/actualizaciones en la fila pedida."""
    n = len(matrix)
    if n == 0:
        return [], 0

    dist = [list(row) for row in matrix]
    for i in range(n):
        dist[i][i] = 0.0

    target = target_row if target_row is not None else n - 1
    if not 0 <= target < n:
        raise IndexError("target_row fuera de rango")

    comparisons = 0
    updates = 0

    for k in range(n):
        dist_k = dist[k]
        for i in range(n):
            row_i = dist[i]
            dik = row_i[k]
            for j in range(n):
                candidate = dik + dist_k[j]
                if i == target:
                    comparisons += 1
                if candidate < row_i[j]:
                    row_i[j] = candidate
                    if i == target:
                        updates += 1

    return dist, comparisons + updates


def dijkstra_last_row(
    matrix: Sequence[Sequence[float]],
) -> Tuple[List[float], int]:
    """Ejecuta Dijkstra tomando la última fila como fuente y cuenta comparaciones/actualizaciones."""
    n = len(matrix)
    if n == 0:
        return [], 0

    source = n - 1
    dist = [math.inf] * n
    dist[source] = 0.0
    visited = [False] * n
    heap: List[Tuple[float, int]] = [(0.0, source)]

    comparisons = 0
    updates = 0

    while heap:
        current_dist, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True

        row_u = matrix[u]
        for v, weight in enumerate(row_u):
            if math.isinf(weight):
                continue
            candidate = current_dist + weight
            comparisons += 1
            if candidate < dist[v]:
                dist[v] = candidate
                updates += 1
                heapq.heappush(heap, (candidate, v))

    return dist, comparisons + updates


def _format_number(value: float) -> str:
    if math.isinf(value):
        return "inf"
    if abs(value - round(value)) < 1e-9:
        return f"{int(round(value))}"
    return f"{value:.6f}"


def _print_matrix(matrix: Iterable[Sequence[float]]) -> None:
    for row in matrix:
        print(" ".join(_format_number(value) for value in row))


def _rows_match(row_a: Sequence[float], row_b: Sequence[float], *, tol: float = 1e-9) -> bool:
    if len(row_a) != len(row_b):
        return False
    for a, b in zip(row_a, row_b):
        if math.isinf(a) or math.isinf(b):
            if a != b:
                return False
            continue
        if abs(a - b) > tol:
            return False
    return True


def main() -> None:
    dist, floyd_ops = floyd_warshall_with_row_stats(MATRIX)
    dijkstra_row, dijkstra_ops = dijkstra_last_row(MATRIX)

    print("Matriz D(N):")
    _print_matrix(dist)

    print("\nVector de distancias desde fila N (Dijkstra):")
    print(" ".join(_format_number(value) for value in dijkstra_row))

    floyd_last_row = dist[-1] if dist else []
    if _rows_match(floyd_last_row, dijkstra_row):
        print("\nCoincidencia: la fila N de Floyd-Warshall coincide con Dijkstra.")
    else:
        print("\nAdvertencia: los resultados de la fila N no coinciden entre Floyd-Warshall y Dijkstra.")

    print(f"\nFloyd realizó {floyd_ops} operaciones")
    print(f"Dijkstra realizó {dijkstra_ops} operaciones")


if __name__ == "__main__":
    main()
