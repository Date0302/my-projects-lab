public class Example4_11 {
       public abstract class Door {
           protected boolean isOpen; // 定义boolean变量
           // public void setOpen(boolean isOpen) {
                            this.isOpen = isOpen; // 设置门状态
                       }
          public boolean getOpen() {
                           return this.isOpen; // 判断门状态
                      }
           public void state() {//判断门是否打开
                           if (isOpen) {
                                   System.out.println("门已经打开");
                              } else {
                                   System.out.println("门已经关闭");
                               }
                       }
           public abstract void setOpenMethod(int num); // 抽象方法：定义开门方式
       }
       public class GuardDoor extends Door { // 防盗门
          public void setOpenMethod(int num) {//实现抽象方法
                           if (num == 8) { // 按 8 次开门
                                   this.isOpen = true;
                               }
                       }
      }
      public class AutoDoor extends Door { // 自动门
           public void setOpenMethod(int num) {
                           if (num == 1) { // 按 1 次开门
                                   this.isOpen = true;
                               }
                       }
       }
   }
