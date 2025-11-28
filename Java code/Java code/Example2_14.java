import java.util.Arrays;
import java.util.Random;
public class Example2_14 {
    public static void main(String[] args) {
        Random random = new Random();
        int[] grades = new int[20];
        for (int i = 0; i < 20; i++) {
            grades[i] = random.nextInt(101);
        }
        System.out.println("排序前：" + Arrays.toString(grades));
        Arrays.sort(grades);
        for (int i = 0; i < grades.length / 2; i++) {
            int temp = grades[i];
            grades[i] = grades[grades.length - 1 - i];
            grades[grades.length - 1 - i] = temp;
        }
        System.out.println("排序后：" + Arrays.toString(grades));
    }
}