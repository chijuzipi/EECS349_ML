import math
def infoGain(List):
 print List
 N = len(List)
 N1 = [] 
 N2 = []
# S = []
 S1 = []
 for i in range(1,N) :
   N1.append( sum(List[0:i]))
   N2.append( sum(List[i:N]))
 #  S.append
#   (i/N*(-N1[i]/i*log(N1[i]/i,2)-(i-N1[i])/i*log((i-N1[i])/i,2))+(N-i)/N*(-N2[i]/(N-i)*log(N2[i]/(N-i),2)-(N-i-N2[i])/(N-i)*log((N-i-N2[i])/(N-i),2)))
   #S1.append(i/N*(-N1[i]/i*log(N1[i]/i,2)-(i-N1[i])/i*log((i-N1[i])/i,2)))
 print N1
 print N2
 

 for i in range(1,N-1) : 
    S1.append(i/N*(entroy(N1[i]/i))  
 #print N1
 #print N2 
 # print S1
 

 
List = [1,0,1,1,1,1,1,0,0,0,1]
infoGain(List)
#return index

 def entropy(p):
  if p == 0:
    iEntropy = 0
  else :
    iEntropy = -p*math.log(p,2)
  return iEntropy
