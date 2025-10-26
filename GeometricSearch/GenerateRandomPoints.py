import random
import argparse

# Function to generate random points
def generate_points(n, coord_range=(-2000, 2000)):
    return [(random.randint(*coord_range), random.randint(*coord_range)) for _ in range(n)]

parser = argparse.ArgumentParser(description="Generate Random Points for Geometric Search")
parser.add_argument("-n", "--num_points", type=int, default=100, help="Number of random points to generate")
parser.add_argument("-r", "--range", type=int, nargs=2, default=[-2000, 2000], help="Range for x and y coordinates")
args = parser.parse_args()

# Generate 3 lists of points
list = generate_points(args.num_points, tuple(args.range))

# Function to save to text file
def save_points(filename, points):
    with open(filename, "w") as f:
        f.write(f"{len(points)}\n")
        for x, y in points:
            f.write(f"({x}, {y})\n")

# Save all lists
save_points("points.txt", list)