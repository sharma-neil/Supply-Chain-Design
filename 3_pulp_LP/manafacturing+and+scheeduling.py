
import pulp as pl

product1= 25
product2=35

## 25 kg of feather
## 35 for cotton

## it takes 0.3 k f and 0.5 k c to make x1
## it takes 0.5 k f and 0.5 k c to make x2

model = pl.LpProblem('PILLOWS',pl.LpMaximize)

X1= pl.LpVariable('X1',0,None,'Integer')
X2= pl.LpVariable('X2',0,None,'Integer')

##define our objeective function

model += X1 *25 +X2 *35

model += X1* 0.3 +X2 * 0.5 <= 20
model += X1* 0.5 +X2 * 0.5 <= 35

model.solve()

X1.varValue
X2.varValue


import pandas as pd

param=pd.read_excel('/home/neil/repos/Supply-Chain-Design/3_pulp_LP/Production_scheduling.xlsx')

param=param.rename(columns={'Unnamed: 0': 'period'} )
param['Capacity']=5000
param['t']= range(1,13)

param= param.set_index('t')

print(param)

inventory= pl.LpVariable.dicts('inv',[0,1,2,3,4,5,6,7,8,9,10,11,12],0,None,'Integer')
inventory[0]= 200

production=pl.LpVariable.dicts('Prod',[1,2,3,4,5,6,7,8,9,10,11,12],0,None,'Integer')
binary= pl.LpVariable.dicts('binary',[1,2,3,4,5,6,7,8,9,10,11,12],0,None,'Binary')

time= [1,2,3,4,5,6,7,8,9,10,11,12]


model= pl.LpProblem('Production',pl.LpMinimize)

model += pl.lpSum([ inventory[t]* param.loc[t,'storage cost']+ production[t]* param.loc[t,'var']+
                binary[t]* param.loc[t,'fixed cost'] for t in time])


for t in time:
    model+=  production[t]  -  inventory[t]+ inventory[t-1]>= param.loc[t,'demand']
    model +=   production[t]<=        binary[t]* param.loc[t,'Capacity']
    
model.solve()    
for v in model.variables():
    print(v,v.varValue)

for i in production: print(production[i],production[i].varValue)




























