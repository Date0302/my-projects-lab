import java.util.Scanner;
public class Example2_6 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入整数n：");
        int n = scanner.nextInt();
        long factorial = 1;

        for (int i = 1; i <= n; i++) {
            factorial *= i;
            System.out.printf("%d: %d\n", i, factorial);
        }
        scanner.close();
    }
}