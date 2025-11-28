class Student {  // 去掉public修饰符
    private String name;  // Name
    private int age;      // Age

    // No-argument constructor
    public Student() {
        System.out.println("An instance of a new Student object has been created.");
    }

    // Parameterized constructor
    public Student(String name, int age) {
        this();  // Call the no-argument constructor
        this.name = name;
        this.age = age;
    }

    // Member method: Returns self-introduction information
    public String sayHello() {
        return "I am:" + name + "，age:" + age;
    }
}

public class Example3_10 {
    public static void main(String[] args) {
        Student stu = new Student("Zhang Hai", 21);  // Instantiate Student object
        System.out.println(stu.sayHello());
    }
}