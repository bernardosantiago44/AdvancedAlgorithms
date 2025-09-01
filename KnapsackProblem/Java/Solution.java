package Java;

import java.util.ArrayList;

public class Solution {
    public static ArrayList<Integer> knapsack(int W, int[] w, int[] v) {
        int[][] table = new int[v.length + 1][W + 1];

        // Iterate the list of items, starting with index 1 (because it represents)
        // Taking the first item into the knapsack
        for (int item = 1; item <= v.length; item++ ) {
            for (int cap = 0; cap <= W; cap++) {
                int currentWeight, currentValue;
                currentWeight = w[item - 1];
                currentValue = v[item - 1];

                // Consider what if we don't take the item
                table[item][cap] = table[item - 1][cap];

                // We only take the item if it's more profitable
                // We must also consider the value of the previous items
                if (currentWeight <= cap && currentValue + table[item - 1][cap - currentWeight] > table[item][cap]) {
                    table[item][cap] = currentValue + table[item - 1][cap - currentWeight];
                }
            }
        }

        // Backtrack to find the items that were included
        ArrayList<Integer> selectedItems = new ArrayList<>();
        int remainingWeight = W;

        // We start looking at the maximum value of the knapsack
        // with the current capacity.
        for (int i = v.length; i > 0 && remainingWeight > 0; i--) {
            // If the item was included (that is, the current value is 
            // different than the previous one with the same weight) then we
            // add the current item index into the list.
            if (table[i][remainingWeight] != table[i - 1][remainingWeight]) {
                selectedItems.add(i - 1); // Item i-1 was included
                remainingWeight -= w[i - 1];
            }
        }

        return selectedItems;
    }
}
