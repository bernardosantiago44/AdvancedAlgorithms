import matplotlib.pyplot as plt
import argparse
from collections import namedtuple
from math import sqrt

Point = namedtuple("Point", ["x", "y"])

# chatazo porque plotear en python no tiene sentido 😝
def _normalize_points(iterable) -> list[Point]:
    """Coerce iterable items into a flat list of Point instances."""
    normalized: list[Point] = []
    for item in iterable:
        if isinstance(item, Point):
            normalized.append(item)
            continue
        if isinstance(item, (list, tuple)):
            # If the entry holds other Points (e.g., closest pairs), flatten it.
            if all(isinstance(sub_item, Point) for sub_item in item):
                normalized.extend(sub_item for sub_item in item)
                continue
            if len(item) == 2 and all(isinstance(coord, (int, float)) for coord in item):
                normalized.append(Point(item[0], item[1]))
                continue
        raise TypeError("Unsupported point format for plotting.")
    return normalized

def plotPoints(points, color='blue', ax=None) -> plt.Axes:
    points = _normalize_points(points)
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    if ax is None:
        fig, ax = plt.subplots()
    ax.scatter(x_coords, y_coords, color=color)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Geometric Points')
    ax.grid(True)
    return ax

def distanceBetweenPoints(p1: Point, p2: Point) -> float:
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def minDistInSublist(points: list[Point]):
    if len(points) == 1:
        return distanceBetweenPoints((0, 0), (0, 0))
    
    minDist = float('inf')
    
    # Calcular distancia todos contra todos
    l = 0
    while l < len(points):
        r = l + 1
        while r < len(points) and r > l:
            dist = distanceBetweenPoints(points[r], points[l])
            if dist < minDist: minDist = dist
            r += 1
        l += 1
    return minDist


def minGlobalDistance(points):
    n = len(points)
    mid = n // 2

    left = points[:mid]
    right = points[mid:]

    leftMinDist = minDistInSublist(left)
    rightMinDist = minDistInSublist(right)
    d = min(leftMinDist, rightMinDist)

    # Linea divisora vertical
    X = points[mid].x
    xMinStrip = X - d
    xMaxStrip = X + d

    strip = []
    dStrip = float('inf')
    for point in points:
        if abs(point.x - X) < d: strip.append(point)
    
    strip = sorted(strip, key=lambda point: point.y)
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j].y - strip[i].y) < d:
            dist = distanceBetweenPoints(strip[i], strip[j])
            if dist < dStrip: dStrip = dist
            j += 1
    minDist = min(d, dStrip)
    print(f"{minDist:.6f}")
    return minDist

# closest pairs with tolerance for floating point precision
def closestPairs(points, dist, tol=1e-9):
    closest_pairs = []
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            d = distanceBetweenPoints(points[i], points[j])
            if abs(d - dist) <= tol:
                closest_pairs.append((points[i], points[j]))
    return closest_pairs


def main():
    # parse plot argument
    parser = argparse.ArgumentParser(description="Geometric Search Point Plotter")
    parser.add_argument('-p', '--plot', action='store_true', help='Enable plotting of points')
    args = parser.parse_args()

    numPoints = int(input(""))

    points = []
    for _ in range(numPoints):
        # format of input: (x, y)
        pointInput = input().strip()
        pointStr = pointInput.strip("()")
        x, y = map(float, pointStr.split(","))
        points.append(Point(x, y))
    points = sorted(points, key=lambda point: point.x) # sort by x-coordinate
    d = minGlobalDistance(points)
    closestPairsList = closestPairs(points, d)
    for p1, p2 in closestPairsList:
        print(f"({p1.x}, {p1.y}) - ({p2.x}, {p2.y}). Distance: {d:.6f}")

    if args.plot:
        ax = plotPoints(points)
        plotPoints(closestPairsList, color='red', ax=ax)
        ax.set_title(f'Closest Pairs (Distance: {d:.6f})')
        plt.show()

if __name__ == "__main__":
    main()
