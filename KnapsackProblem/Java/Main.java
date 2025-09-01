package Java;

import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        int[] weights = {1, 2, 3};
        int[] values = {1, 2, 3};

        ArrayList<Integer> selectedItems = Solution.knapsack(4, weights, values);
        System.out.println("Selected items (0-based index): " + selectedItems);
        System.out.println("Total value: " + selectedItems.stream().mapToInt(i -> values[i]).sum());
    }
}
