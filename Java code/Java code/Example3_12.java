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
                   return "我是:" + name + "，年龄:" + age;
               }
       static void quitSchool() {
                   System.out.println("有学生退学了");
                  number--;
               }
      public void printNumber() {
                   System.out.println(number);
               }
   }