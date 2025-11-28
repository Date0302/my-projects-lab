public class Example2_15 {
    public static void main(String[] args) {
        int[][] matrix = {
                {1, 2, 3, 4, 5},
                {2, 4, 6, 8, 10},
                {3, 6, 9, 12, 15},
                {4, 8, 12, 16, 20},
                {5, 10, 15, 20, 25}
        };
        long total = 0;
        for (int[] row : matrix) {
            for (int num : row) {
                total += num;
            }
        }
        double avg = total / 25.0;
        System.out.printf("平均值：%.2f\n", avg);
        int diagonalSum = 0;
        for (int i = 0; i < 5; i++) {
            diagonalSum += matrix[i][i];
            diagonalSum += matrix[i][4 - i];
        }
        diagonalSum -= matrix[2][2]; // 去重
        System.out.println("两对角线之和：" + diagonalSum);
    }
}