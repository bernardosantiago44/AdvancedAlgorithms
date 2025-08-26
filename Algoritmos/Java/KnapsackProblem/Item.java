package Java.KnapsackProblem;

public class Item {
    private int value;
    private int weight;

    public Item(int value, int weight) {
        this.value = value;
        this.weight = weight;
    }

    public int GetValue() {
        return this.value;
    }

    public int GetWeight() {
        return this.weight;
    }
}