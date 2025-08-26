package Java;
import java.util.ArrayList;

public class Solution {
    private int capacity;
    private ArrayList<Item> items;
    
    public Solution(int capacity, ArrayList<Item> items) {
        this.capacity = capacity;
        this.items = items;
    }

    public Solution() {
        ArrayList<Item> items = new ArrayList<Item>();
        items.add(new Item(2, 3));
        items.add(new Item(2, 1));
        items.add(new Item(4, 3));
        items.add(new Item(5, 4));
        items.add(new Item(3, 2));
        
        this.capacity = 7;
        this.items = items;
    }

    public int maxValueOfKnapsack() {
        int[][] dp = new int[items.size() + 1][capacity + 1];
        for (int item = 1; item <= items.size(); item++) {
            Item currenItem = items.get(item - 1);
            int currentWeight = currenItem.GetWeight();
            int currentValue = currenItem.GetValue();

            for (int cap = 0; cap <= capacity; cap++) {
                // If we don't take the item
                dp[item][cap] = dp[item - 1][cap];

                // We take the item only if it's more profitable
                // We must also consider the value of the previous items
                if (currentWeight <= cap && currentValue + dp[item - 1][cap - currentWeight] > dp[item][cap]) {
                    dp[item][cap] = currentValue + dp[item - 1][cap - currentWeight];
                }
            }
        }

        int maxValue = dp[items.size()][capacity];
        return dp[items.size()][capacity];
        
        // Get the items that make up the exact capacity and max value
        // ArrayList<Item> selectedItems = new ArrayList<Item>();
        // int remainingCapacity = capacity;


        // return new ArrayList<Item>();
    }
}
