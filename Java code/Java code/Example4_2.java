public static void main(String[] args){
        class CBox{
        private double length;
       private double width;
        private double height;
        public void SetLength(double len){
                      length=len;
                   }
       public void SetWidth(double w){
                       width=w;
                   }
       public void SetHeight(double h){
                       height=h;
                   }
       public double Volume(){
                       return length*width*height;
                   }
       public void ShowBox(){
                      System.out.println("长度:"+length+"宽度:"+width+"高度:"+height);
                  }
   }
}
}