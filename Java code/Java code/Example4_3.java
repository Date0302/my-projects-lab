class CColorBox {
       private double length;
       private double width;
        private double height;
        private String color;

               // Setter 方法（遵循Java命名规范，首字母小写）
           public void setLength(double len) {
                   this.length = len;
               }

               public void setWidth(double w) {
                   this.width = w;
               }

               public void setHeight(double h) {
                   this.height = h;
              }

               public void setColor(String color) {
                   this.color = color;
               }

               // 显示盒子信息
               public void showColorBox() {
                   System.out.println("彩色盒子 - 颜色: " + color);
              }

               // 计算体积
               public double volume() {
                   return length * width * height;
               }
   }

           // 主类
           public class Example4_3 {
       public static void main(String[] args) {
                   CColorBox ob1 = new CColorBox();

                   // 设置尺寸
                   ob1.setLength(1);
                   ob1.setWidth(2);  // 修正：原代码三次调用setLength，应该是设置长宽高
                   ob1.setHeight(3);

                   // 设置颜色
                   ob1.setColor("Red");  // 修正：原方法名SetColour改为setColor（美式拼写）
                   ob1.showColorBox();   // 修正：方法名遵循驼峰命名

                   System.out.println("体积: " + ob1.volume());
               }
   }