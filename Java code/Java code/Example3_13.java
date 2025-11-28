    class Student {
        String name;
       private int age;
        static {
                    System.out.println("我是静态代码块");
                }
       public Student() {
                   System.out.println("我是Student类的构造方法");
               }
       public Student(String name, int age) {
                   this.name = name;
                   this.age = age;
                   System.out.println("创建了" + name);
               }
   }
   public class Example3_13 {
       public static void main(String[] args) {
                   Student stu1 = new Student("张海", 21);
                   Student stu2 = new Student("李智宽", 22);
                   Student stu3 = new Student("王强", 22);
               }
   }