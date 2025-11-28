import java.util.Scanner;
public class Example2_4 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入成绩（0-100）：");
        int score = scanner.nextInt();
        if (score < 0 || score > 100) {
            System.out.println("输入错误！");
            return;
        }
        char grade;
        if (score >= 90)       grade = 'A';
        else if (score >= 80)  grade = 'B';
        else if (score >= 70)  grade = 'C';
        else if (score >= 60)  grade = 'D';
        else                   grade = 'E';
        System.out.println("成绩等级为：" + grade);
        scanner.close();
    }
}