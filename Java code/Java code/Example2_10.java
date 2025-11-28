public class Example2_10 {
    public static void main(String[] args) {
        System.out.print("同构数：");
        for (int i = 1; i <= 100; i++) {
            long square = (long) i * i;
            String numStr = String.valueOf(i);
            String squareStr = String.valueOf(square);
            if (squareStr.endsWith(numStr)) {
                System.out.print(i + " ");
            }
        }
    }
}