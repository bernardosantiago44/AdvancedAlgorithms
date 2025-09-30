package Dijkstra;
import java.util.*;

/// Undirected Weighted Graph
/// Adjacency List Representation
/// 
class Graph {
    private int vertices;
    private List<List<Edge>> adjList;
    private Set<Edge> edges;

    public Graph(int vertices) {
        this.vertices = vertices;
        adjList = new ArrayList<>(vertices);
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }

    public void addEdge(int src, int dest, int weight) {
        adjList.get(src).add(new Edge(dest, weight));
        adjList.get(dest).add(new Edge(src, weight));
    }

    public List<Edge> getAdj(int vertex) {
        return adjList.get(vertex);
    }

    public int getVertices() {
        return vertices;
    }

    static class Edge {
        int dest;
        int weight;

        Edge(int dest, int weight) {
            this.dest = dest;
            this.weight = weight;
        }
    }
}