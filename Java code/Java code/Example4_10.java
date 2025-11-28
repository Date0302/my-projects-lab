package CH4.example.xmj;
    class Animal {
       public void move() {
                    System.out.println("我可以移动...");  // 修正：move→移动
                }
   }
   // 定义Bird类继承Animal类
           class Bird extends Animal {
       @Override
       public void move() {
                   System.out.println("我在天空飞翔...");
               }

               public void singing() {
                   System.out.println("鸟儿会清脆地歌唱...");  // 修正：歌噌→歌唱
               }
   }
   // 定义Fish类继承Animal类（调整缩进）
          class Fish extends Animal {
       @Override
       public void move() {
                   System.out.println("我在水里游泳...");
               }
   }

           // 定义测试类
           public class Test {
       public static void main(String[] args) {
                   Animal a1 = new Animal();
                   a1.move();

                   Animal a2 = new Bird();
                   a2.move();

                   Animal a3 = new Fish();
                   a3.move();

                  if (a2 instanceof Bird) {
                           ((Bird) a2).singing();
                       }
               }
   }