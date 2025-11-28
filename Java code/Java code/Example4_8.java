package ch4.example.xmj;
    class Person{
        String namw;
        int age;
       public Person(String name,int age){
                    this.name=name;
                  this.age=age;
                   System.out.println("*****父类构造:1.publicPerson()");
               }
   }
   class Student extends Person{
       String school;
       public Student(String name,int age,String school){

                   super(name, age);
                  this.school=school;
                  System.out.println("#####子类构造:2.public Student()");
               }
   }
   public class Example4_8 {
       public static void main(String[] args){
                   Student student=new Student("张海",20,"郑州中学");
               }
   }