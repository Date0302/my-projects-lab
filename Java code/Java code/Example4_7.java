package ch4.example.xmj;
    class Person{
        String namw;
        int age;
        public Person(){
                    System.out.println("*****父类构造:1.publicPerson()");
               }
   }
   class Student extends Person{
       String school;
       public Student(){
                   //super();
                   System.out.println("#####子类构造:2.public Student()");
               }
   }
   public class Example4_7 {
       public static void main(String[] args){
                  Student student=new Student();
               }
   }