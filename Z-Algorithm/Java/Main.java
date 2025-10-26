package Java;

import java.util.ArrayList;
import java.util.Collections;

public class Main {
    public static void main(String[] args) {
        String s = "abra$abracadabra";
        ArrayList<Integer> result = ZAlgorithm(s);

        System.out.println(result);
        System.out.print("[");
        for (char c : s.toCharArray()) {
            System.out.print(c + ", ");
        }
        System.out.print("]\n");
    }

    private static ArrayList<Integer> ZAlgorithm(String s) {
        int n = s.length();
        ArrayList<Integer> Z = new ArrayList<>(Collections.nCopies(n, 0));
        int L, R, K;
        L = R = K = 0;

        for (int i = 1; i < n; i++) {
            if (i > R) {
                L = R = i;
                // Expand the window while the prefix and lookup 
                // position's strings are the same.
                while (R < n && s.charAt(R) == s.charAt(R - L)) Z.set(i, Z.get(i) + 1);

                Z.set(i, R - L); // Z[i] = R - L;
                R--; // Step R back to continue looking for substring in the next iteration
            } else {
                K = i - L;
                if (Z.get(K) < R - i + 1) 
                    Z.set(i, Z.get(K));
                else {
                    // Expand the window while the prefix and lookup 
                    // position's strings are the same.
                    while (R < n && s.charAt(R) == s.charAt(R - L)) Z.set(i, Z.get(i) + 1);

                    Z.set(i, R - L); // Z[i] = R - L;
                    R--; // Step R back to continue looking for substring in the next iteration
                } 
            }
        }

        return Z;
    }
}