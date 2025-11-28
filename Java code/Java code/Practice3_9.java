class Student {
        private String name;  // 定义私有成员变量 name
        private int age;      // 定义私有成员变量 age

                // 带参构造方法（初始化 name 和 age）
                public Student(String name, int age) {
                   this.name = name;  // 使用 this 区分成员变量和局部变量
                   this.age = age;     // 修正赋值语句
               }

               // 成员方法：sayHello()
               public void sayHello() {
                   System.out.println("我是：" + name + "，年龄：" + age);
               }
   }

           public class Practice3_9 {
       public static void main(String[] args) {
                   Student stu = new Student("张海", 21);  // 实例化 Student 对象
                   stu.sayHello();  // 调用 sayHello() 方法
                  }
   }