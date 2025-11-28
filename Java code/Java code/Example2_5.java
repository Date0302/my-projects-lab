import java.util.Scanner;
public class Example2_5 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入购物金额：");
        double amount = scanner.nextDouble();

        int range = (amount >= 5000) ? 4 :
                (amount >= 3000) ? 3 :
                        (amount >= 2000) ? 2 :
                                (amount >= 1000) ? 1 : 0;
        double rate;
        switch (range) {
            case 4: rate = 0.8;   break;
            case 3: rate = 0.85;  break;
            case 2: rate = 0.9;   break;
            case 1: rate = 0.95;  break;
            default: rate = 1.0;  break;
        }
        double finalPrice = amount * rate;
        System.out.printf("优惠后金额：%.2f", finalPrice);
        scanner.close();
    }
}