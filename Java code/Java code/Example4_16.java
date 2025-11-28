// 第一题：抽象类Shape及其子类
public class Example4_16 {
}

abstract class Shape {//定义抽象类Shape
    protected String color;//定义属性color

    public Shape(String color) {// 构造方法
        this.color = color;
    }

    public abstract double getArea();// 抽象方法 - 获取面积

    public String getColor() {// 获取颜色
        return color;
    }
}

class Rectangle extends Shape {// Rectangle 类继承 Shape
    private double width;
    private double height;

    public Rectangle(String color, double width, double height) {// 构造方法
        super(color);
        this.width = width;
        this.height = height;
    }

    @Override// 实现获取面积方法
    public double getArea() {
        return width * height;
    }
}

class Circle extends Shape {// Circle 类继承 Shape
    private double radius;

    public Circle(String color, double radius) {// 构造方法
        super(color);
        this.radius = radius;
    }

    // 实现获取面积方法
    @Override
    public double getArea() {
        return Math.PI * radius * radius;
    }
}

class ShapeTest {// 测试程序
    public static void main(String[] args) {
        // 创建各种形状对象
        Shape rectangle = new Rectangle("红色", 5.0, 3.0);
        Shape circle = new Circle("蓝色", 2.5);
        // 测试矩形
        System.out.println("矩形信息:");
        System.out.println("颜色: " + rectangle.getColor());
        System.out.println("面积: " + rectangle.getArea());
        // 测试圆形
        System.out.println("\n圆形信息:");
        System.out.println("颜色: " + circle.getColor());
        System.out.println("面积: " + circle.getArea());
        // 创建形状数组并遍历
        Shape[] shapes = {
                new Rectangle("绿色", 4.0, 6.0),
                new Circle("黄色", 3.0),
                new Rectangle("紫色", 2.0, 2.0)
        };

        System.out.println("\n所有形状信息:");
        for (Shape shape : shapes) {
            System.out.println("类型: " + shape.getClass().getSimpleName() +
                    ", 颜色: " + shape.getColor() +
                    ", 面积: " + shape.getArea());
        }
    }
}