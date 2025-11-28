// 第二题：三角形类及其子类
import java.util.Scanner;

public class Example4_17 {
    // 三角形类
    class Triangle {
        protected float a, b, c; // 三条边长
        // 构造方法
        public Triangle(float a, float b, float c) {
            this.a = a;
            this.b = b;
            this.c = c;
        }
        // 判断是否为三角形
        public boolean isTriangle() {
            return (a + b > c) && (a + c > b) && (b + c > a);
        }
        // 重写toString方法
        @Override
        public String toString() {
            return "三角形三条边长: a=" + a + ", b=" + b + ", c=" + c;
        }
    }
    // 直角三角形子类
    class RightTriangle extends Triangle {
        // 构造方法
        public RightTriangle(float a, float b, float c) {
            super(a, b, c);
        }
        // 判断是否为直角三角形
        public boolean isRightTriangle() {
            // 检查勾股定理
            return (a * a + b * b == c * c) ||
                    (a * a + c * c == b * b) ||
                    (b * b + c * c == a * a);
        }
        // 计算周长
        public float getPerimeter() {
            return a + b + c;
        }
        // 计算面积
        public float getArea() {
            // 找出两条直角边
            if (a * a + b * b == c * c) {
                return (a * b) / 2;
            } else if (a * a + c * c == b * b) {
                return (a * c) / 2;
            } else {
                return (b * c) / 2;
            }
        }
    }

    // 测试程序
    public class TriangleTest {
        public static void main(String[] args) {
            Scanner scanner = new Scanner(System.in);

            System.out.println("请输入三角形的三条边长:");
            System.out.print("边a: ");
            float a = scanner.nextFloat();
            System.out.print("边b: ");
            float b = scanner.nextFloat();
            System.out.print("边c: ");
            float c = scanner.nextFloat();

            // 创建三角形对象
            Triangle triangle = new Triangle(a, b, c);

            // 判断是否为三角形
            if (triangle.isTriangle()) {
                System.out.println("\n" + triangle.toString());

                // 创建直角三角形对象
                RightTriangle rightTriangle = new RightTriangle(a, b, c);

                // 判断是否为直角三角形
                if (rightTriangle.isRightTriangle()) {
                    System.out.println("这是一个直角三角形");
                    System.out.println("周长: " + rightTriangle.getPerimeter());
                    System.out.println("面积: " + rightTriangle.getArea());
                } else {
                    System.out.println("这不是一个直角三角形");
                }
            } else {
                System.out.println("这三条边不能构成三角形");
            }

            scanner.close();
        }
    }
}