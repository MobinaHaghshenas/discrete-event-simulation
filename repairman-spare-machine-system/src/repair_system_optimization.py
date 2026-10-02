# Library
import random
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt

# Generate Random number
def RNG(a, m, X0, c):
    return (a * X0 + c) % m

def Congruential_Method(a, m, X0, c):
    randnum = [X0]
    flag = True
    
    while flag:
        r = RNG(a, m, randnum[-1], c)
        # Check whether we entered the loop or not
        if r != X0: 
            randnum.append(r)
        else:
            flag = False
    # Scaling random numbers
    randnum = np.array(randnum) / m 
    randnum = list(randnum)
    return randnum

randnum = Congruential_Method(5,2**21,5009,0)
list_random = random.sample(list(randnum),7)[0]

# Uniform Function
def uniform_inverse_one(random_number,alpha,beta):
    return (beta-alpha)*random_number+alpha

# Generate Number of workers
NumOFW = 1
#NumOfM = int (input('Enter the number of Machines : ' ))
NumOfM = 63
#NumOfMS = int (input('Enter the number of extra machines : ' )) 
NumOfMS = 7
#CostOfFEghdan = int (input('Enter the cost of Feghdan : ' ))
CostOfFEghdan = 10
#CostOfRepairman = int (input('Enter the cost of Repairman : ' ))
CostOfRepairman = 1

# Initialize minimum total cost
total_cost_min = float('inf') 
 # Initialize optimal option
optimal_option = None  
total_cost_values = []  
options = []  

while NumOFW <= 20:
    # Reset NumOfMS after inner loop
    NumOfMS = 7  
    
    while NumOfMS <= 100:
        TTFeghdan = []
        STime = []
        ServiceTime = []
        TotalNumOfSimulation = 10
        N = 1

        while N <= TotalNumOfSimulation:
            # Define Variables and lists
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
            FEL = []
            FEGHDAN = []
            NAS = 0
            TFeghdan = 0

            for i in range(1, NumOfM + 1):
                x = int(uniform_inverse_one(list_random, 100, 200))
                FEL.append([i, x])

            statuse = dict()
            for i in range(NumOfM + 1, NumOfM + NumOFW + 1):
                statuse[i] = [0, 0, 0]

            while TNow <= T:
                TNow = min(FEL, key=lambda x: x[1])[1]
                code = min(FEL, key=lambda x: x[1])[0]
                del_list = [code, TNow]
                FEL = [i for i in FEL if i != del_list]

                if code <= 0:
                    if MW < NumOfM:
                        MW += 1
                        TMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[1]
                        MashMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[0]
                        TFeghdan += (TNow - TMinFeghdan)
                        LT = int(uniform_inverse_one(list_random, 100, 200))
                        FEL += [[MashMinFeghdan, TNow + LT]]
                        del_list = [MashMinFeghdan, T + 500]
                        FEL = [j for j in FEL if j != del_list]
                        del_feghdan = [MashMinFeghdan, TMinFeghdan]
                        FEGHDAN = [i for i in FEGHDAN if i != del_feghdan]
                    else:
                        MS += 1

                elif code <= NumOfM:
                    NF += 1
                    if MS > 0:
                        MS -= 1
                        LT = int(uniform_inverse_one(list_random, 100, 200))
                        FEL += [[code, LT + TNow]]
                    else:
                        MW -= 1
                        NM += 1
                        FEL += [[code, T + 500]]
                        FEGHDAN += [[code, TNow]]
                    TT = int(uniform_inverse_one(list_random, 10, 15))
                    TTT += TT
                    FEL += [[200 + NF, TT + TNow]]

                elif code < 200:
                    if MW < NumOfM:
                        MW += 1
                        TMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[1]
                        MashMinFeghdan = min(FEGHDAN, key=lambda x: x[1])[0]
                        TFeghdan += (TNow - TMinFeghdan)
                        TT = int(uniform_inverse_one(list_random, 10, 15))
                        TTT += TT
                        LT = int(uniform_inverse_one(list_random, 100, 200))
                        FEL += [[MashMinFeghdan, TNow + LT + TT]]
                        del_list = [MashMinFeghdan, T + 500]
                        FEL = [j for j in FEL if j != del_list]
                        del_feghdan = [MashMinFeghdan, TMinFeghdan]
                        FEGHDAN = [i for i in FEGHDAN if i != del_feghdan]
                    else:
                        TT = int(uniform_inverse_one(list_random, 10, 15))
                        TTT += TT
                        FEL += [[0 - NAS, TNow + TT]]
                        NAS += 1

                    if Q > 0:
                        Q -= 1
                        RT = int(uniform_inverse_one(list_random, 30, 60))
                        FEL += [[code, TNow + RT]]
                        statuse[code][0] = 1
                        statuse[code][1] += RT
                        statuse[code][2] += 1
                    else:
                        statuse[code][0] = 0

                else:
                    if all(value[0] == 1 for value in statuse.values()):
                        Q += 1
                        if Q > QMax:
                            QMax = Q
                    else:
                        i = random.choice([k for k, v in statuse.items() if v[0] == 0])
                        RT = int(uniform_inverse_one(list_random, 30, 60))
                        FEL += [[i, TNow + RT]]
                        statuse[i][0] = 1
                        statuse[i][1] += RT
                        statuse[i][2] += 1

            LenFeghdan = len(FEGHDAN)
            for y in range(0, LenFeghdan):
                TFeghdan += (T - FEGHDAN[y][1])

            TTFeghdan.append(TFeghdan)
            for key, value in statuse.items():
              STime.append((value[1]) )
            ServiceTime.append(mean(STime))
            N += 1

        total_cost = (((mean(TTFeghdan)))  * CostOfFEghdan) + (T*NumOFW* CostOfRepairman)
        
        # Update minimum total cost and optimal option if a new minimum is found
        if total_cost < total_cost_min:
            total_cost_min = total_cost
            optimal_option = (NumOFW, NumOfMS)
        
        # Store the total cost and the combination of repairmen and spare cars
        total_cost_values.append(total_cost)
        options.append((NumOFW, NumOfMS))

        NumOfMS += 1

    NumOFW += 1

# Plot the results
x = np.arange(len(total_cost_values))
y = total_cost_values

plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b')
plt.xticks(x, options, rotation='vertical')
plt.xlabel('Number of Repairmen and Spare Cars')
plt.ylabel('Total Cost')
plt.title('Total Cost vs. Number of Repairmen and Spare Cars')
plt.grid(True)
plt.tight_layout()
plt.show()

print("Optimal Option: Number of Repairmen =", optimal_option[0], ", Number of Spare Cars =", optimal_option[1])
print("Minimum Total Cost:", total_cost_min)