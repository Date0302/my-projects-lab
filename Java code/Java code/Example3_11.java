    class Student {
        private String name;
        private int age;
        static int number = 0;
        public Student(String name, int age) {
                    this.name = name;
                   this.age = age;
                   System.out.println("创建了" + name);
                   number++;
               }
       public String sayHello() {
                   return "我是:" + name + ",年龄:" + age;
              }
       public void quitSchool() {
                   System.out.println(name + "退学了");
                   number--;
                   if (number < 3) {
                           System.out.println("警告！不足3人");
                       }
               }
   }
   public class Example3_11 {
       public static void main(String[] args) {
                   Student stu1 = new Student("张海", 21);  // 实例化Student对象
                   Student stu2 = new Student("李智宽", 22);  // 实例化Student对象
                   Student stu3 = new Student("王强", 22);  // 实例化Student对象
                   System.out.print(stu1.number + " ");
                   System.out.print(stu2.number + " ");
                   System.out.print(Student.number + " ");
                   stu2.quitSchool();
                   System.out.print(Student.number);
               }
   }