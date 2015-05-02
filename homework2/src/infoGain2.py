import math
import sys
def entropy(p):
 iEntropy = []
 if p == 0.00:
  iEntropy = 0.00
 else :
  iEntropy = -p*math.log(p,2)
 return iEntropy


def infoGain(List):
 N = len(List)
 N1 = [] 
 N2 = []
 S1 = []
 S2 = []
 for i in range(1,N):
  N1.append( sum(List[0:i]))
  N2.append( sum(List[i:N]))
  print N1
  print N2

 for i in range(1,N):
  S1.append(float(i)/N*(entropy(N1[i-1]/i))+float(i)/N*entropy((i-N1[i-1])/i)) 
  S2.append(float(N-i)/N*(entropy(N2[len(N2)-/(N-1-i))+entropy(N-1-i-)/(N-1-i)))
  print float(i)
  print N1[i-1]
 # print N
  print float(i)/N
  print S1
 
 for i in range (1,)

# print S2
List=[]
List.append(1.00)
List.append(1.00)
List.append(1.00)
List.append(0.00)
List.append(1.00)
List.append(0.00)

infoGain(List)

