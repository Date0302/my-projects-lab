public class Example2_7 {
    public static void main(String[] args) {
        long totalSum = 0;
        for (int i = 1; i <= 9; i += 2) {
            long factorial = 1;
            for (int j = 1; j <= i; j++) {
                factorial *= j;
            }
            totalSum += factorial;
        }
        System.out.println("1!+3!+5!+7!+9! = " + totalSum);
    }
}