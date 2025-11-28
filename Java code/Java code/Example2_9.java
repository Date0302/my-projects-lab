public class Example2_9 {
    public static void main(String[] args) {
        double[] arr = new double[100];
        arr[0] = 1; arr[1] = 2; arr[2] = 3;
        int index = 3;
        while (true) {
            arr[index] = (arr[index-3] + arr[index-2] + arr[index-1]) / 2;
            if (arr[index] > 1200) {
                System.out.println("首次超过1200的项是第" + (index+1) + "项");
                break;
            }
            index++;
        }
    }
}