'''
1.等级划分标准：
  等级    高         中           低
  科研经费 20以上    20-5        5以下
  人数     10以上    10-5        5以下
  作品数   30以上    30-10       10以下
  获奖数   15以上    15-5        5以下
2.隶属度函数f(x)：
   高：f(x)^(0.5)
   中：min(f(x),1-f(x))
   低：(1-f(x))^0.5

 3.推理规则：
   if  科研经费低 and 人数高 and 作品数低 and 获奖数低 then 评价差   3 15 5 3  0.99999
   if  科研经费高 and 人数低 and 作品数低 and 获奖数高 then 评价高    22 3 5 20  2.99999
   if  科研经费中 and 人数中 and 作品数中 and 获奖数中 then 评价中   15 8 20 10  1.5
   if  科研经费高 and 人数高 and 作品数低 and 获奖数低 then 评价差    22 20 5 3  0.999
   评价等级高、中、低分别用3, 2, 1表示
'''
import math
W={}
MIN={}
MUL={}
jf=0
rs=0
zp=0
hj=0
pj={}
class T_S:

    def fun1(m):#科研经费隶属度函数
        if m<=5:
            return 0
        if m>5 and m<=20:
            return ((m-5)/15)*((m-5)/15)
        if m>20:
            return 1
    def fun2(m):#人数隶属度函数
        if m<=5:
            return 0
        if m>5 and m<=10:
            return ((m-5)/5)*((m-5)/5)
        if m>10:
            return 1
    def fun3(m):#作品数隶属度函数
        if m<=10:
            return 0
        if m>10 and m<=30:
            return ((m-10)/20)*((m-10)/20)
        if m>30:
            return 1
    def fun4(m):#获奖数隶属度函数
        if m<=5:
            return 0
        if m>5 and m<=15:
            return ((m-5)/10)*((m-5)/10)
        if m>15:
            return 1
    def rule1(self):
        W[0]=math.sqrt(1-T_S.fun1(jf))
        W[1] = math.sqrt(T_S.fun2(rs))
        W[2] = math.sqrt(1 - T_S.fun3(zp))
        W[3] = math.sqrt(1 - T_S.fun4(hj))
        pj[0]=1
        for i in range(4):
            if(W[i]<0.0000000001):
                W[i]=0
        minTemp=999#取小法
        for i in range(4):
            if(W[i]!=999):
                minTemp=min(minTemp,W[i])
        MIN[0]=minTemp
        mulTemp=1#乘积法
        for i in range(4):
            if(W[i]!=999):
                mulTemp=mulTemp*W[i]
        MUL[0]=mulTemp


    def rule2(self):
        W[0] = math.sqrt(T_S.fun1(jf))
        W[1] = math.sqrt(1-T_S.fun2(rs))
        W[2] = math.sqrt(1-T_S.fun3(zp))
        W[3] = math.sqrt(T_S.fun4(hj))
        pj[1]=3
        for i in range(4):
            if(W[i]<0.0000000001):
                W[i]=0
        minTemp=999#取小法
        for i in range(4):
            if(W[i]!=999):
                minTemp=min(minTemp,W[i])
        MIN[1]=minTemp
        mulTemp=1
        for i in range(4):
            if(W[i]!=999):
                mulTemp=mulTemp*W[i]
        MUL[1]=mulTemp

    def rule3(self):
        W[0] = min(T_S.fun1(jf),1-T_S.fun1(jf))
        W[1] = min(T_S.fun2(rs),1-T_S.fun2(rs))
        W[2] = min(T_S.fun3(zp),1-T_S.fun3(zp))
        W[3] = min(T_S.fun4(hj),1-T_S.fun4(hj))
        pj[2]=2
        for i in range(4):
            if(W[i]<0.0000000001):
                W[i]=0
        minTemp=999#取小法
        for i in range(4):
            if(W[i]!=999):
                minTemp=min(minTemp,W[i])
        MIN[2]=minTemp
        mulTemp=1
        for i in range(4):
            if(W[i]!=999):
                mulTemp=mulTemp*W[i]
        MUL[2]=mulTemp

    def rule4(self):
        W[0] = math.sqrt(T_S.fun1(jf))
        W[1] = math.sqrt(T_S.fun2(rs))
        W[2] = math.sqrt(1-T_S.fun3(zp))
        W[3] = math.sqrt(1-T_S.fun4(hj))
        pj[3]=1
        for i in range(4):
            if(W[i]<0.0000000001):
                W[i]=0
        minTemp=999#取小法
        for i in range(4):
            if(W[i]!=999):
                minTemp=min(minTemp,W[i])
        MIN[3]=minTemp
        mulTemp=1
        for i in range(4):
            if(W[i]!=999):
                mulTemp=mulTemp*W[i]
        MUL[3]=mulTemp


if __name__ == '__main__':
    jf=int(input("经费："))
    rs=int(input("人数："))
    zp=int(input("作品："))
    hj=int(input("获奖："))
    T_S.rule1("")
    T_S.rule2("")
    T_S.rule3("")
    T_S.rule4("")

    MINEVA=0
    MULEVA=0
    min_sum1 = min_sum2 = mul_sum1 = mul_sum2 = 0
    for i in range(4):
        min_sum1+=MIN[i]*pj[i]
        min_sum2+=MIN[i]
        mul_sum1+=MUL[i]*pj[i]
        mul_sum2+=MUL[i]
    MINEVA=min_sum1/(min_sum2+0.000000001)
    MULEVA=mul_sum1/(mul_sum2+0.000000001)
    print("取小法评价："+str(MINEVA))
    print("乘积法评价：" +str(MULEVA))
    if(MINEVA>=0 and MINEVA<=1.5):
        print("评价差")
    elif (MINEVA>1.5 and MINEVA<=2.5):
        print("评价中")
    elif (MINEVA>2.5):
        print("评价高")