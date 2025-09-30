package Tries;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        // Enter N and N words to insert into the Trie
        Scanner scanner = new Scanner(System.in);
        Trie trie = new Trie();

        System.out.print("Enter the number of words to insert: ");
        int n = scanner.nextInt();
        scanner.nextLine();  // Consume newline

        for (int i = 0; i < n; i++) {
            System.out.print("Enter word " + (i + 1) + ": ");
            String word = scanner.nextLine();
            trie.insert(word);
        }

        int m = scanner.nextInt();
        scanner.nextLine();  // Consume newline
        for (int i = 0; i < m; i++) {
            System.out.print("Enter word to search: ");
            String searchWord = scanner.nextLine();
            System.out.println("Search result: " + trie.search(searchWord));
        }

        scanner.close();
    }
}
