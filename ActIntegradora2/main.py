import sys
import math
from collections import deque
from itertools import combinations

# --------------------------
# Utilidades de parsing/IO
# --------------------------

def idx_to_label(idx):
    """Convierte 0->A, 25->Z, 26->AA, etc."""
    s = ""
    idx2 = idx
    while True:
        s = chr(idx2 % 26 + ord('A')) + s
        idx2 = idx2 // 26 - 1
        if idx2 < 0:
            break
    return s

def read_all_numbers(lines, count):
    """Lee 'count' números flotantes/enteros recorriendo líneas (ignora vacías)."""
    nums = []
    i = 0
    while i < len(lines) and len(nums) < count:
        line = lines[i].strip()
        if line:
            # separa por espacios
            parts = line.replace(",", " ").split()
            for p in parts:
                # permite enteros o floats
                try:
                    nums.append(float(p))
                except ValueError:
                    pass
        i += 1
    return nums

def parse_matrix_from_chunk(lines_iter, N):
    """Lee una matriz NxN de números (enteros o floats). Tolerante a espacios."""
    nums = []
    while len(nums) < N*N:
        try:
            line = next(lines_iter)
        except StopIteration:
            break
        line = line.strip()
        if not line:
            continue
        # reemplaza múltiples espacios y comas
        parts = line.replace(",", " ").split()
        for p in parts:
            try:
                nums.append(float(p))
            except ValueError:
                continue
    if len(nums) < N*N:
        raise ValueError("No se pudieron leer N x N números para la matriz.")
    # arma la matriz
    M = []
    k = 0
    for _ in range(N):
        M.append(nums[k:k+N])
        k += N
    return M

def parse_points(lines_iter, N):
    """Lee N puntos con formato tipo '(x,y)' (espacios tolerados)."""
    pts = []
    while len(pts) < N:
        line = next(lines_iter, None)
        if line is None:
            break
        line = line.strip()
        if not line:
            continue
        # extrae lo que esté entre paréntesis
        if '(' in line and ')' in line:
            inside = line[line.find('(')+1:line.find(')')]
        else:
            inside = line
        inside = inside.replace(",", " ")
        parts = inside.split()
        if len(parts) >= 2:
            try:
                x = float(parts[0]); y = float(parts[1])
                pts.append((x, y))
            except ValueError:
                pass
    if len(pts) < N:
        raise ValueError("No se pudieron leer N puntos para las centrales.")
    return pts

def load_input(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = [line.rstrip('\n') for line in f]

    # Cursor de lectura
    it = iter(raw)

    # Lee N
    N = None
    for line in it:
        line = line.strip()
        if not line:
            continue
        try:
            N = int(line)
            break
        except ValueError:
            continue
    if N is None or N <= 0:
        raise ValueError("No se pudo leer N válido (>0).")

    # Matriz de distancias
    dist_mat = parse_matrix_from_chunk(it, N)

    # Matriz de capacidades (flujo)
    cap_mat = parse_matrix_from_chunk(it, N)

    # Lista de N puntos (centrales)
    points = parse_points(it, N)

    return N, dist_mat, cap_mat, points

# --------------------------
# 1) MST con Kruskal + DSU
# --------------------------

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n
    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.r[ra] < self.r[rb]:
            self.p[ra] = rb
        elif self.r[ra] > self.r[rb]:
            self.p[rb] = ra
        else:
            self.p[rb] = ra
            self.r[ra] += 1
        return True

def mst_kruskal(dist_mat):
    n = len(dist_mat)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            w = dist_mat[i][j]
            if math.isfinite(w) and w > 0:
                edges.append((w, i, j))
    edges.sort()
    dsu = DSU(n)
    mst_edges = []
    for w,i,j in edges:
        if dsu.union(i,j):
            mst_edges.append((i,j))
            if len(mst_edges) == n-1:
                break
    return mst_edges

# --------------------------
# 2) TSP
#    - Held-Karp exacto si N<=12
#    - Vecino más cercano + 2-opt si N>12
# --------------------------

def tour_length(tour, dist):
    L = 0.0
    for k in range(len(tour)-1):
        L += dist[tour[k]][tour[k+1]]
    return L

def tsp_held_karp(dist):
    n = len(dist)
    if n == 1:
        return [0, 0], 0.0

    start_mask = 1 << 0
    costs = {(start_mask, 0): 0.0}
    parent = {}

    for subset_size in range(2, n + 1):
        for subset in combinations(range(1, n), subset_size - 1):
            mask = start_mask
            for node in subset:
                mask |= 1 << node
            for last in subset:
                full_mask = mask
                prev_mask = full_mask ^ (1 << last)
                best_cost = math.inf
                best_prev = None
                for prev in range(n):
                    if prev == last:
                        continue
                    if not (prev_mask & (1 << prev)):
                        continue
                    prev_cost = costs.get((prev_mask, prev))
                    if prev_cost is None:
                        continue
                    cand = prev_cost + dist[prev][last]
                    if cand < best_cost:
                        best_cost = cand
                        best_prev = prev
                if best_prev is not None:
                    costs[(full_mask, last)] = best_cost
                    parent[(full_mask, last)] = best_prev

    full_mask = (1 << n) - 1
    best_cost = math.inf
    best_last = None
    for last in range(1, n):
        state = (full_mask, last)
        if state not in costs:
            continue
        cand = costs[state] + dist[last][0]
        if cand < best_cost:
            best_cost = cand
            best_last = last

    if best_last is None:
        raise ValueError("No se encontró una ruta Hamiltoniana válida para el TSP.")

    order = []
    mask = full_mask
    last = best_last
    while last != 0:
        order.append(last)
        prev = parent[(mask, last)]
        mask ^= 1 << last
        last = prev

    order.reverse()
    route = [0] + order + [0]
    return route, best_cost

def nearest_neighbor(dist, start=0):
    n = len(dist)
    unvis = set(range(n))
    path = [start]
    unvis.remove(start)
    cur = start
    while unvis:
        nxt = min(unvis, key=lambda j: dist[cur][j] if cur!=j else math.inf)
        path.append(nxt)
        unvis.remove(nxt)
        cur = nxt
    path.append(start)
    return path

def two_opt(path, dist, max_iter=2000):
    improved = True
    n = len(path)-1
    count = 0
    while improved and count < max_iter:
        improved = False
        count += 1
        for i in range(1, n-1):
            for k in range(i+1, n):
                a,b = path[i-1], path[i]
                c,d = path[k], path[(k+1)%len(path)]
                delta = (dist[a][c] + dist[b][d]) - (dist[a][b] + dist[c][d])
                if delta < -1e-12:
                    path[i:k+1] = reversed(path[i:k+1])
                    improved = True
    return path

def tsp_solve(dist):
    n = len(dist)
    if n <= 12:
        route, cost = tsp_held_karp(dist)
    else:
        route = nearest_neighbor(dist, start=0)
        route = two_opt(route, dist)
        cost = tour_length(route, dist)
    return route, cost

# --------------------------
# 3) Flujo máximo (Edmonds-Karp)
# --------------------------

def edmonds_karp(capacity, s, t):
    n = len(capacity)
    flow = 0.0
    # residual como copia
    residual = [row[:] for row in capacity]

    while True:
        parent = [-1]*n
        parent[s] = s
        q = deque([s])
        while q and parent[t] == -1:
            u = q.popleft()
            for v in range(n):
                if parent[v] == -1 and residual[u][v] > 1e-12:
                    parent[v] = u
                    q.append(v)
        if parent[t] == -1:
            break
        # bottleneck
        aug = math.inf
        v = t
        while v != s:
            u = parent[v]
            aug = min(aug, residual[u][v])
            v = u
        # actualiza residuales
        v = t
        while v != s:
            u = parent[v]
            residual[u][v] -= aug
            residual[v][u] += aug
            v = u
        flow += aug
    return flow

# --------------------------
# 4) Voronoi por intersección de semiplanos
#     - Sutherland–Hodgman sobre rectángulo de encuadre
# --------------------------

def bounding_box(points, margin_ratio=0.2):
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    dx = xmax - xmin
    dy = ymax - ymin
    dx = dx if dx>0 else 1.0
    dy = dy if dy>0 else 1.0
    mx = dx*margin_ratio
    my = dy*margin_ratio
    return (xmin - mx, ymin - my, xmax + mx, ymax + my)

def clip_polygon_with_halfplane(poly, a, b, c):
    """Mantiene puntos que satisfacen a*x + b*y <= c."""
    if not poly:
        return []
    out = []
    n = len(poly)
    def inside(P):
        x,y = P
        return a*x + b*y <= c + 1e-12
    def intersect(P, Q):
        # Intersección del segmento PQ con la línea a x + b y = c
        x1,y1 = P; x2,y2 = Q
        f1 = a*x1 + b*y1 - c
        f2 = a*x2 + b*y2 - c
        denom = f1 - f2
        if abs(denom) < 1e-18:
            return Q  # casi paralelos; devolver Q
        t = f1 / (f1 - f2)
        return (x1 + t*(x2-x1), y1 + t*(y2-y1))
    for i in range(n):
        P = poly[i]
        Q = poly[(i+1)%n]
        Pin = inside(P); Qin = inside(Q)
        if Pin and Qin:
            out.append(Q)
        elif Pin and not Qin:
            out.append(intersect(P,Q))
        elif (not Pin) and Qin:
            out.append(intersect(P,Q))
            out.append(Q)
        else:
            # fuera -> fuera (no agregamos)
            pass
    return out

def voronoi_polygons(sites):
    # Rectángulo base
    xmin, ymin, xmax, ymax = bounding_box(sites, margin_ratio=0.4)
    base_poly = [(xmin,ymin),(xmax,ymin),(xmax,ymax),(xmin,ymax)]
    polys = []
    n = len(sites)
    for i in range(n):
        Pi = sites[i]
        poly = base_poly[:]
        for j in range(n):
            if i == j: 
                continue
            Pj = sites[j]
            # Semiplano: puntos más cerca de Pi que de Pj
            # Derivado de: ||x-Pi||^2 <= ||x-Pj||^2  => (q-p)·x <= (||q||^2 - ||p||^2)/2
            a = (Pj[0] - Pi[0])
            b = (Pj[1] - Pi[1])
            c = (Pj[0]**2 + Pj[1]**2 - Pi[0]**2 - Pi[1]**2)/2.0
            poly = clip_polygon_with_halfplane(poly, a, b, c)
            if not poly:
                break
        polys.append(poly)
    return polys

# --------------------------
# Formateo de salida
# --------------------------

def format_edges_as_labels(edges):
    return [(idx_to_label(u), idx_to_label(v)) for (u,v) in edges]

def format_route_as_labels(route):
    return [idx_to_label(i) for i in route]

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_entrada>")
        sys.exit(1)

    N, dist_mat, cap_mat, centers = load_input(sys.argv[1])

    # 1) MST
    mst_edges = mst_kruskal(dist_mat)
    mst_labeled = format_edges_as_labels(mst_edges)

    # 2) TSP (desde A)
    tsp_route, tsp_cost = tsp_solve(dist_mat)
    tsp_labeled = format_route_as_labels(tsp_route)

    # 3) Flujo máximo de A a última colonia
    s, t = 0, N-1
    maxflow = edmonds_karp(cap_mat, s, t)

    # 4) Polígonos Voronoi
    vor_polys = voronoi_polygons(centers)

    # --- Impresión solicitada ---
    print("1) Forma de cablear (MST):")
    print(mst_labeled)
    print()

    print("2) Ruta TSP (inicio y fin en A):")
    print(tsp_labeled)
    print(f"Costo total (km): {tsp_cost:.3f}")
    print()

    print("3) Flujo máximo de {} a {}:".format(idx_to_label(s), idx_to_label(t)))
    if abs(maxflow - round(maxflow)) < 1e-9:
        print(int(round(maxflow)))
    else:
        print(f"{maxflow:.6f}")
    print()

    print("4) Polígonos de Voronoi (lista por central):")
    # cada polígono como lista de tuplas (x,y)
    formatted = []
    for poly in vor_polys:
        formatted.append([(round(x,6), round(y,6)) for (x,y) in poly])
    print(formatted)

if __name__ == "__main__":
    main()
