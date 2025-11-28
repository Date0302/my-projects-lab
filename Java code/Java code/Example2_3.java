import java.util.Scanner;
public class Example2_3 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入整数：");
        int n = scanner.nextInt();

        if (n % 5 == 0 && n % 7 == 0) {
            System.out.printf("%d能同时被5和7整除", n);
        } else {
            System.out.printf("%d不能同时被5和7整除", n);
        }
        scanner.close();
    }
}