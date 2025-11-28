import java.util.Arrays;
import java.util.Scanner;
public class Example2_13 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入数组长度：");
        int n = scanner.nextInt();
        int[] arr = new int[n];
        System.out.print("请输入数组元素：");
        for (int i = 0; i < n; i++) {
            arr[i] = scanner.nextInt();
        }
        for (int i = 0; i < n / 2; i++) {
            int temp = arr[i];
            arr[i] = arr[n - 1 - i];
            arr[n - 1 - i] = temp;
        }
        System.out.println("逆序结果：" + Arrays.toString(arr));
        scanner.close();
    }
}