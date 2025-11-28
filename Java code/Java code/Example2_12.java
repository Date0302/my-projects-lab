public class Example2_12 {
    public static void main(String[] args) {
        int[][] matrix = {
                {1, 2, 3, 4, 5},
                {6, 7, 8, 9, 10},
                {11,12,13,14,15},
                {16,17,18,19,20},
                {21,22,23,24,25}
        };
        int sum = 0;
        for (int i = 0; i < 5; i++) {
            sum += matrix[i][i];         // 主对角线
            sum += matrix[i][4 - i];     // 副对角线
        }
        sum -= matrix[2][2];            // 去除重复计算的中心点
        System.out.println("两对角线之和：" + sum);
    }
}