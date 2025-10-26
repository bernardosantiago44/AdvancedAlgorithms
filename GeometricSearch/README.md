# Geometric Search Algorithm
## Closest Pair of Points Problem
Bernardo Santiago Marin A01638915

This repository contains an implementation of the Geometric Search Algorithm to solve the Closest Pair of Points Problem in a 2D plane. The algorithm efficiently finds the pair of points that are closest to each other among a given set of points.

To run the algorithm, use the provided `GeometricSearch.py` script. You can test the implementation with various input files located in the repository. Add the -p flag to see the plot of the points and the closest pair highlighted.

Run command:
```bash
python GeometricSearch.py -p < input_file.txt
```

For the input file:
1. The first line should contain an integer `n`, the number of points.
2. The next `n` lines should each contain the coordinates in the format `(x, y)`.
Example input file:
```
5
(0, 0)
(1, 1)
(2, 2)
(3, 3)
(0, 1)
```

The output will display the closest pair of points and the distance between them. If the -p flag is used, a plot will be generated showing all points and highlighting the closest pair.

---

Alternatively, you can run the algorithm without plotting by manually entering the points in the terminal:
```bash
python GeometricSearch.py -p
```
Then input the number of points followed by the coordinates in the specified format above.

---
## Random Point Generator
I also included a `GenerateRandomPoints.py` script to create random test cases for the algorithm. You can specify the number of points and the range for the coordinates.

To generate random points, run:
```bash
python GenerateRandomPoints.py -n <number_of_points> -r <min> <max>
```
This will create a file named `points.txt` with the specified number of random points within the