#Library
import random
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
#Generate Random number
#a=multiplier , m=modulus, X0=seed , c=constant
def RNG(a,m,X0,c):
    return (a*X0+c)%m

def Congruential_Method(a,m,X0,c):
    randnum=[X0]
    flag=True
    
    while(flag):
        r = RNG(a,m,randnum[-1],c)
        if(r != X0): #Check whether we entered the loop or not
            randnum.append(r)
        else:
            flag = False
    randnum = np.array(randnum)/(m) #Scaling random numbers
    randnum = list(randnum)
    return randnum

randnum = Congruential_Method(5,2**21,5009,0)
list_random = random.sample(list(randnum),7)[0]

def uniform_inverse_one(random_number,alpha,beta):
    return (beta-alpha)*random_number+alpha
#For plotting
NumOFW_values = []
Mean_TFeghdan_values = []
Mean_ServiceTime_values = []

# Generate Number of workers
NumOFW = 1
#NumOfM = int (input('Enter the number of Machines : ' ))
NumOfM = 63
#NumOfMS = int (input('Enter the number of extra machines : ' )) 
NumOfMS = 7
while NumOFW <= 20:
  TTFeghdan = []
  STime = []
  ServiceTime =[]
  #TotalNumOfSimulation = int (input('Enter the number of simulation : ' ))
  TotalNumOfSimulation = 10
  N = 1
  while N <= TotalNumOfSimulation :
    
      #Define Variables and lists
      TNow = 0
      T = 40 * 60
      MW = NumOfM
      MS = NumOfMS
      Q = 0
      QMax = 0
      TT = 0
      TTT = 0
      NM = 0
      NF = 0
      FEL=[]
      FEGHDAN = []
      NAS = 0
      TFeghdan = 0
      
      for i in range(1,NumOfM+1):
          x = int(uniform_inverse_one(list_random,100,200))
          FEL.append([i,x])
      
      #statuse = {'i' :(SR(j),TSR(j),F(j))}
      statuse = dict()
      for i in range(NumOfM+1,NumOfM+NumOFW+1):
          statuse[i] = [0,0,0]
      
      #Main loop for each simulation
      while TNow <= T :
          TNow = min(FEL, key=lambda x: x[1])[1]
          code = min(FEL, key=lambda x: x[1])[0]
          #Delete from FEL
          del_list = [code, TNow]
          FEL = [i for i in FEL if i!= del_list]
          
          #پیشامد رسیدن ماشین به یدکی
          if code <= 0:
              if MW < NumOfM:
                  MW += 1
                  TMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[1]
                  MashMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[0]
                  TFeghdan +=  (TNow - TMinFeghdan)
                  LT = int(uniform_inverse_one(list_random,100,200))
                  FEL +=[[MashMinFeghdan,TNow+LT]]
                  del_list = [MashMinFeghdan, T+500]
                  FEL = [j for j in FEL if j!= del_list]
                  del_feghdan = [MashMinFeghdan ,TMinFeghdan]
                  FEGHDAN = [i for i in FEGHDAN if i!= del_feghdan]
              else :
                  MS += 1
                  
          #پیشامد خرابی ماشین    
          elif code <= NumOfM:
              NF += 1
              if MS > 0:
                  MS -= 1
                  LT = int(uniform_inverse_one(list_random,100,200))
                  FEL+=[[code,LT+TNow]]
              else:
                  MW -= 1
                  NM += 1
                  FEL +=[[code,T+500]]
                  FEGHDAN += [[code,TNow]]
              TT = int(uniform_inverse_one(list_random,10,15))
              TTT +=TT
              FEL += [[200+NF , TT+TNow]]
              
          #پیشامد اتمام تعمیر    
          elif code < 200:
              if MW <NumOfM:
                  MW += 1
                  TMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[1]
                  MashMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[0]
                  TFeghdan +=  (TNow - TMinFeghdan)
                  TT = int(uniform_inverse_one(list_random,10,15))
                  TTT += TT
                  LT = int(uniform_inverse_one(list_random,100,200))
                  FEL += [[MashMinFeghdan,TNow+LT+TT]]
                  del_list = [MashMinFeghdan, T+500]
                  FEL = [j for j in FEL if j!= del_list]
                  del_feghdan = [MashMinFeghdan ,TMinFeghdan]
                  FEGHDAN = [i for i in FEGHDAN if i!= del_feghdan]
              else:
                  TT = int(uniform_inverse_one(list_random,10,15))
                  TTT += TT
                  FEL += [[0-NAS,TNow+TT]]
                  NAS += 1
              
              if Q > 0:
                  Q -= 1
                  RT = int(uniform_inverse_one(list_random,30,60))
                  FEL +=[[code,TNow+RT]]
                  statuse[code][0] = 1
                  statuse[code][1] += RT
                  statuse[code][2] += 1
              else:
                  statuse[code][0] = 0

          #پیشامد رسیدن ماشین به تعمیرگاه
          else:
              #If all the workers are busy, the machine will be added to the queue
              if all(value[0] == 1 for value in statuse.values()):
                  Q += 1
                  if Q > QMax : 
                      QMax = Q
              else :
                  i = random.choice([k for k, v in statuse.items() if v[0] == 0])
                  RT = int(uniform_inverse_one(list_random,30,60))
                  FEL +=[[i,TNow+RT]]
                  statuse[i][0] = 1
                  statuse[i][1] += RT
                  statuse[i][2] += 1                
      LenFeghdan = len (FEGHDAN)
      for y in range (0,LenFeghdan):
          TFeghdan += (T - FEGHDAN[y][1]) 

      TTFeghdan.append(TFeghdan)
      for key, value in statuse.items():
          STime.append((value[1] / T) * 100)
      ServiceTime.append(mean(STime))

      N += 1
  print('For %d Repairmen:' % NumOFW)
  print('Mean TFeghdan:', (mean(TTFeghdan)) / 60)
  print('Mean Service Time:', mean(ServiceTime))
  NumOFW_values.append(NumOFW)
  Mean_TFeghdan_values.append(mean(TTFeghdan) / 60)
  Mean_ServiceTime_values.append(mean(ServiceTime))
  NumOFW += 1
# Plotting Mean TFeghdan and Mean Service Time together
plt.plot(NumOFW_values, Mean_TFeghdan_values, label='Mean TFeghdan')
plt.plot(NumOFW_values, Mean_ServiceTime_values, label='Mean Service Time')
plt.xlabel('Number of Repairmen')
plt.ylabel('Time (minutes) / Service Time')
plt.title('Mean TFeghdan and Mean Service Time vs. Number of Repairmen')
plt.legend()
