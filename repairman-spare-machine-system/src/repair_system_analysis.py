#Library
import random
from statistics import mean
from statistics import variance
from scipy import stats
import matplotlib.pyplot as plt

#Interval_estimate
def Interval_estimate(data):
  Mean = mean(data)
  S = ((variance(data))**(1/2))/((len(data))**(1/2))
  #alpha = 0.05
  t_critical = stats.t.ppf(1 -  0.05/2, df=len(data)-1)
  return [Mean-(t_critical*S) ,Mean+(t_critical*S) ]

#NumberOfSimulation
N = 1
#TotalNumOfSimulation = int (input('Run the simulation for : ' ))
TotalNumOfSimulation = 10

#Generate Number of workers and mashines

NumOFW = 14 
#NumOfM = int (input('Enter the number of Machines : ' ))
NumOfM = 63
#NumOfMS = int (input('Enter the number of extra machines : ' )) 
NumOfMS = 7

#Define Variables and lists

ListNumFail = []
ListNumFeghdan = []
ListTFeghdan = []
ListTTT = []
ListQMax = []
STime =[]
ServiceTime = []
NumS =[]
NumService =[]
ListNumServedStation = dict ()
ListPercSTSation = dict ()
for u in range (NumOfM+1, NumOfM+NumOFW+1):
    ListNumServedStation[u] = []
    ListPercSTSation[u] = []
AveNumServedStation = dict()
AvePercSTSation = dict()
for u in range (NumOfM+1, NumOfM+NumOFW+1):
    AveNumServedStation[u] = 0
    AvePercSTSation[u] = 0    
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
        x = random.randint(100,200)
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
                LT = random.randint(100, 200)
                FEL +=[[MashMinFeghdan,TNow+LT]]
                del_list = [MashMinFeghdan, T+1]
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
                LT = random.randint(100, 200)
                FEL+=[[code,LT+TNow]]
            else:
                MW -= 1
                NM += 1
                FEL +=[[code,T+1]]
                FEGHDAN += [[code,TNow]]
            TT = random.randint(10, 15)
            TTT +=TT
            FEL += [[200+NF , TT+TNow]]
            
        #پیشامد اتمام تعمیر    
        elif code < 200:
            if MW <NumOfM:
                MW += 1
                TMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[1]
                MashMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[0]
                TFeghdan +=  (TNow - TMinFeghdan)
                TT = random.randint(10, 15)
                TTT += TT
                LT = random.randint(100, 200)
                FEL += [[MashMinFeghdan,TNow+LT+TT]]
                del_list = [MashMinFeghdan, T+1]
                FEL = [j for j in FEL if j!= del_list]
                del_feghdan = [MashMinFeghdan ,TMinFeghdan]
                FEGHDAN = [i for i in FEGHDAN if i!= del_feghdan]
            else:
                TT = random.randint(10, 15)
                TTT += TT
                FEL += [[0-NAS,TNow+TT]]
                NAS += 1
            
            if Q > 0:
                Q -= 1
                RT = random.randint(30, 60)
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
                RT = random.randint(30, 60)
                FEL +=[[i,TNow+RT]]
                statuse[i][0] = 1
                statuse[i][1] += RT
                statuse[i][2] += 1                
    LenFeghdan = len (FEGHDAN)
    for y in range (0,LenFeghdan):
        TFeghdan += (T - FEGHDAN[y][1])

    ListNumFail += [NF]
    ListNumFeghdan += [NM]
    ListTFeghdan += [TFeghdan/60]
    ListTTT += [TTT/60]
    ListQMax += [QMax]
    for key, value in statuse.items():
      STime.append(((value[1])/T)*100 )
    ServiceTime.append(mean(STime))
    for key, value in statuse.items():
      NumS.append((value[2]) )
    NumService.append(mean(NumS))
    for u in range (NumOfM+1, NumOfM+NumOFW+1):
      ListNumServedStation[u] += [statuse[u][2]]
      ListPercSTSation[u]  += [statuse[u][1]/T*100]
    N += 1
    
AveNumFail = mean(ListNumFail)
AveNumFeghdan = mean(ListNumFeghdan)
AveTFeghdan = mean(ListTFeghdan)
AveTTT = mean(ListTTT)
AveQMax = mean(ListQMax)
AveServiceTime = mean(ServiceTime)
AveNumberOfService = mean(NumService)
for u in range (NumOfM+1, NumOfM+NumOFW+1):
    AveNumServedStation[u] = mean(ListNumServedStation[u])
    AvePercSTSation[u] = mean(ListPercSTSation[u])
#Point estimat and Interval_estimate    
#548.13
print ('\nPoint estimat and Interval_estimate Of Fails = ',AveNumFail ,Interval_estimate(ListNumFail))

print ('\nPoint estimat and Interval_estimate Of Number of Lost = ',AveNumFeghdan,Interval_estimate(ListNumFeghdan))
print ('\nPoint estimat and Interval_estimate Of  Lost of Time(hours) = ',AveTFeghdan,Interval_estimate(ListTFeghdan))
print ('\nPoint estimat and Interval_estimate Of  Trans Time (hours)= ', AveTTT,Interval_estimate(ListTTT))
print ('\nPoint estimat and Interval_estimate Of  Queue = ',AveQMax,Interval_estimate(ListQMax))
print ('\nPoint estimat and Interval_estimate Of  Number of cars repaired by repairmans = ',AveNumberOfService,Interval_estimate(NumService))
print ('\nPoint estimat and Interval_estimate Of Employment percentage of repairmans = ',AveServiceTime,Interval_estimate(ServiceTime))
for u in range (NumOfM+1, NumOfM+NumOFW+1):
    print ('\nPoint estimat and Interval_estimate Of Num Mash RepairStation %d = ' %(u-NumOfM), AveNumServedStation[u],Interval_estimate(ListNumServedStation[u]))
    print ('\nPoint estimat and Interval_estimate Of RepairStation %d = '%(u-NumOfM), AvePercSTSation[u],Interval_estimate(ListPercSTSation[u]))

# Plotting Box Plots
def plot_boxplot(title, data):
    plt.figure()
    plt.boxplot(data)
    plt.title(title)
    plt.xlabel('Estimate')
    plt.ylabel('Value')
    plt.show()

# Plotting estimates
plot_boxplot('Number of Failures', ListNumFail)
plot_boxplot('Total Lost Time  (hours)', ListTFeghdan)
plot_boxplot('Total Number of Lost  ', ListNumFeghdan)
plot_boxplot('Total Time in Transitions (hours)', ListTTT)
plot_boxplot('Maximum Queue Length', ListQMax)
plot_boxplot('Number of Machines Repaired by Repairmen', NumService)
plot_boxplot('Employment Percentage of Repairmen', ServiceTime)

for u in range(NumOfM+1, NumOfM+NumOFW+1):
    plot_boxplot(f'Number of Machines Served by RepairStation {u-NumOfM}', ListNumServedStation[u])
    plot_boxplot(f'Employment Percentage of RepairStation {u-NumOfM}', ListPercSTSation[u])

# Plotting Bar Plot for Repair Workers
def plot_barplot(title, x_labels, data):
    x = range(len(x_labels))
    plt.figure()
    plt.bar(x, data)
    plt.title(title)
    plt.xlabel('Repair Worker')
    plt.ylabel('Average Number of Machines Repaired')
    plt.xticks(x, x_labels, rotation=45, ha='right')  # Rotate x-axis labels by 45 degrees
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.show()

# Creating a list of repair workers' labels (e.g., 'Worker 1', 'Worker 2', ...)
repair_worker_labels = ['Worker {}'.format(i - NumOfM) for i in range(NumOfM + 1, NumOfM + NumOFW + 1)]

# Plotting Bar Plot for average number of cars repaired by repair workers
plot_barplot('Average Number of Machines Repaired by Repairman', repair_worker_labels, AveNumServedStation.values())



# Obtain the data for the graph
repair_stations =   ['Overall'] + [f'Repair Station {u-NumOfM}' for u in range(NumOfM+1, NumOfM+NumOFW+1)]
employment_percentage = [AveServiceTime] + [AvePercSTSation[u] for u in range(NumOfM+1, NumOfM+NumOFW+1)]

# Create the figure and axes for the graph
fig, ax = plt.subplots(figsize=(8, 6))

# Line graph for employment percentage
ax.plot(repair_stations, employment_percentage, marker='o')
ax.set_xlabel('Repair Station')
ax.set_ylabel('Employment Percentage')

# Set the title
ax.set_title('Employment Percentage of Repair Workers')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the graph
plt.show()