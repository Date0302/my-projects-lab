import java.util.Scanner;
public class Example2_11 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        double[] data = new double[10];
        System.out.print("请输入10个数值：");
        for (int i = 0; i < 10; i++) {
            data[i] = scanner.nextDouble();
        }
        double max = data[0], min = data[0], sum = 0;
        for (double num : data) {
            max = Math.max(max, num);
            min = Math.min(min, num);
            sum += num;
        }
        double avg = sum / 10;
        System.out.println("最大值：" + max);
        System.out.println("最小值：" + min);
        System.out.println("平均值：" + avg);
        System.out.print("高于平均值的数据：");
        int count = 0;
        for (double num : data) {
            if (num > avg) {
                System.out.print(num + " ");
                count++;
            }
        }
        System.out.println("\n数量：" + count);
        scanner.close();
    }
}