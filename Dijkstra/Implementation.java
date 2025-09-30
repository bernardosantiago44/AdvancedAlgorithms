package Dijkstra;
import java.util.ArrayList;
import java.util.List;

public class Implementation {
    public static void main(String[] args) {
        Test2();
    }

    private static void Test1() {
        Graph graph = new Graph(4);

        graph.addEdge(0, 1, 4);
        graph.addEdge(0, 2, 2);
        graph.addEdge(1, 2, 5);
        graph.addEdge(1, 3, 10);
        graph.addEdge(2, 3, 8);

        System.out.println("Dijkstra from vertex 0: " + dijkstra(graph, 0));
    }

    private static void Test2() {
        Graph graph = new Graph(6);

        graph.addEdge(0, 1, 4);
        graph.addEdge(0, 2, 7);
        graph.addEdge(1, 3, 3);
        graph.addEdge(1, 2, 1);
        graph.addEdge(3, 4, 2);
        graph.addEdge(2, 4, 5);
        graph.addEdge(2, 4, 8);
        graph.addEdge(2, 5, 6);
        graph.addEdge(4, 5, 3);

        System.out.println("Dijkstra from vertex 0: " + dijkstra(graph, 0));
    }

    private static List<Integer> dijkstra(Graph graph, int start) {
        List<Integer> dist = new ArrayList<>();
        List<Integer> prev = new ArrayList<>();

        for (int i = 0; i < graph.getVertices(); i++) {
            dist.add(Integer.MAX_VALUE);
            prev.add(null);
        }
        dist.set(start, 0);

        for (int i = 0; i < graph.getVertices(); i++) {
            for (Graph.Edge edge : graph.getAdj(i)) {
                int current = i;
                int v = edge.dest;
                int weight = edge.weight;
                int alt = dist.get(current) + weight;

                if (alt < dist.get(v)) {
                    dist.set(v, alt);
                    prev.set(v, current);
                }
            }
        }
        return dist;
    }
}