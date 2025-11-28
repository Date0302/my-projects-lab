import java.util.Scanner;
public class Example2_8 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入正整数n：");
        int n = scanner.nextInt();
        int s1 = 0, sum1 = 0;
        for (int i = 1; i <= n; i++) {
            sum1 += i;
            s1 += sum1;
        }
        System.out.println("第一问结果：" + s1);
        int s2 = 0;
        for (int i = 1; i <= n; i++) {
            s2 += 10 * i + 2;
        }
        System.out.println("第二问结果：" + s2);
        int s3 = 0, sign = 1;
        for (int i = 1; i <= n; i++) {
            s3 += sign * i * (i + 1);
            sign *= -1;
        }
        System.out.println("第三问结果：" + s3);
        double s4 = 0.0;
        int sum4 = 0;
        for (int i = 1; i <= n; i++) {
            sum4 += i;
            s4 += 1.0 / sum4;
        }
        System.out.printf("第四问结果：%.4f\n", s4);
        scanner.close();
    }
}