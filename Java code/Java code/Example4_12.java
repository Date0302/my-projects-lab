public class Example4_12 {
    package ch4.example.xmj; // 扑克类
        class Card { // 扑克牌类
            String color; // 花色
            // String num;   // 点数

                   public Card(String color, String num) {//构造方法
                           this.color = color;
                          this.num = num;
                       }

                  @Override
          public String toString() {
                          return color + num;
                       }
       } // 修复：补全Card类的右括号

               public class Demo {
           public static void main(String[] args) {
                           Card[] poker = new Card[52]; // 修正变量名拼写
                           String[] colors = {"黑桃", "红桃", "梅花", "方块"};
                           String[] nums = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};

                           int index = 0;
                           for (String num : nums) {
                                   for (String color : colors) {
                                           poker[index++] = new Card(color, num);                   }
                               }

                           // 输出扑克牌
                           for (int i = 0; i < poker.length; i++) {
                                   System.out.print(" " + poker[i]);

                                   // 每13张换行
                               if ((i + 1) % 13 == 0) {
                                           System.out.println();
                                       }
                               }
                           System.out.println("牌数: " + poker.length); // 显示牌数
                      }
      }
   }
