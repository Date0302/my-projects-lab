package ch4.example.xmj;

import java.util.Scanner;

class CPerson {
    private long no;
    private String name;
    private String sex;
    private String birthday;

    public CPerson() {
    }

    public CPerson(long no, String name, String sex, String birthday) {
        this.no = no;
        this.name = name;
        this.sex = sex;
        this.birthday = birthday;
    }

    public void input() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入编号:");
        no = scanner.nextInt();
        System.out.print("姓名:");
        name = scanner.next();
        System.out.print("性别:");
        sex = scanner.next();
        System.out.print("生日:");
        birthday = scanner.next();
    }

    public void printCPersonInfo() {
        System.out.printf("编号:%d;姓名:%s;性别:%s;生日:%s", no, name, sex, birthday);
    }
}

// 派生类 CStudent，继承自CPerson
class CStudent extends CPerson {
    private String[] courses = {"数学", "语文", "政治", "体育", "自然"}; // 学生课程数组
    private int[] grades = new int[5]; // 学生成绩数组

    // 默认构造函数
    public CStudent() {
    }

    // 输入学生课程成绩的方法
    public void inputCourse() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("input your scores: ");
        for (int i = 0; i < courses.length; i++) {
            System.out.print(courses[i] + ": "); // 提示输入每门课程的成绩
            grades[i] = scanner.nextInt(); // 读取用户输入的成绩
        }
    }

    // 打印学生课程成绩的方法
    public void printCourse() {
        System.out.print("student's courses score are: ");
        for (int i = 0; i < courses.length; i++) {
            System.out.print(courses[i]); // 打印课程名称
            System.out.printf(" is :%d", grades[i]); // 打印课程成绩
        }
        System.out.println();
    }
}

// 派生类 CTeacher，继承自CPerson
class CTeacher extends CPerson {
    private String depart; // 教师所在部门
    private String prof;   // 教师职称

    // 默认构造函数
    public CTeacher() {
    }

    // 输入教师信息的方法
    public void inputTeacherInfo() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入部门: ");
        depart = scanner.next(); // 读取用户输入的部门
        System.out.print("职称: ");
        prof = scanner.next();   // 读取用户输入的职称
    }

    // 打印教师信息的方法
    public void printCTeacherInfo() {
        System.out.printf("所在部门: %s; 职称是: %s", depart, prof); // 打印部门和职称
    }
}

public class Example4_13 {
    // 测试类的主方法
    public static void main(String[] args) {
        CStudent s1 = new CStudent(); // 创建学生对象
        s1.input();                  // 调用父类的input方法输入学生基本信息
        s1.inputCourse();            // 输入学生课程成绩
        s1.printCPersonInfo();       // 调用父类的printCPersonInfo方法打印学生基本信息
        s1.printCourse();            // 打印学生课程成绩

        CTeacher t1 = new CTeacher(); // 创建教师对象
        t1.input();                  // 调用父类的input方法输入教师基本信息
        t1.inputTeacherInfo();       // 输入教师部门和职称
        t1.printCPersonInfo();       // 调用父类的printCPersonInfo方法打印教师基本信息
        t1.printCTeacherInfo();      // 打印教师部门和职称
    }
}