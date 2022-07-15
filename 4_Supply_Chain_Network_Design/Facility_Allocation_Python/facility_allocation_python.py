"""
@author: Neil Sharma
"""
import pandas as pd
import pulp as pl

dist = pd.read_excel('/mnt/c/Users/ns86s/repos/Supply-Chain-Design/4_Supply_Chain_Network_Design/Facility_Allocation_Python/warehouse_city.xlsx')
#dist= pd.read_excel('/home/neil/repos/Supply-Chain-Design/4_Supply_Chain_Network_Design/Facility_Allocation_Python/warehouse_city.xlsx')
dist= dist.set_index('Warehouse')
print(dist)

#demand for every customer
demand=[10000,20000,33000,9000,60000,2500,35000]

#setting row headers as potential warehouse location and columns as every customer
warehouse= dist.index
customers= dist.columns

#maps every warehouse location to every customer location
keys= [(w,c) for w in warehouse for c in customers]

# attaches distance for every warehouse location to customer location
dist_dict= { (w,c): dist.loc[w,c] for w in warehouse for c in customers}

#creates a decision variable for whether the route from a warehouse to customer location has been opened
flows= pl.LpVariable.dicts('flows',keys,cat='Binary')
#creates a decision variable whether to open a warehouse or not
open_w= pl.LpVariable.dicts('open_w',warehouse,cat='Binary')

demand_dict= dict(zip(customers,demand))

#creating minimization objective function
model= pl.LpProblem('w_alloc',pl.LpMinimize)

#sum product the demand dictionary with the flows (warehouse to customer) and the distances
model+= pl.lpSum([demand_dict[(c)]* flows[(w,c)]* dist_dict[(w,c)] for c in customers for w in warehouse])


#sum of flows should only equal 1 (city should only have one warehouse supplying it)
for c in customers:
    model+= pl.lpSum([flows[(w,c)] for w in warehouse])== 1
    
#only require 3 warehouses
model+= pl.lpSum([open_w[(w)] for w in warehouse])==3



for w in warehouse:
    model+= open_w[(w)]>= flows[(w,'city 1')]
    model+= open_w[(w)]>= flows[(w,'city 2')]
    model+= open_w[(w)]>= flows[(w,'city 3')]
    model+= open_w[(w)]>= flows[(w,'city 4')]
    model+= open_w[(w)]>= flows[(w,'city 5')]
    model+= open_w[(w)]>= flows[(w,'city 6')]
    model+= open_w[(w)]>= flows[(w,'city 7')]

model.solve()

for i in open_w:
    print(open_w[i],open_w[i].varValue)

flows_names= ['{} to {}'.format(w, c) for w in warehouse for c in customers]
flows_quantity= [flows[(w,c)].varValue for w in warehouse for c in customers]
flows_dict= dict(zip(flows_names,flows_quantity))

average_distance= pl.value(model.objective)/sum(demand)
n_warehouses_opened= sum([open_w[(w)].varValue for w in warehouse])

#### a simulation for distance Vs No of warhouses

def pulp_model(n):

   
   model1= pl.LpProblem('w_alloc',pl.LpMinimize)

   model1+= pl.lpSum([demand_dict[(c)]* flows[(w,c)]* dist_dict[(w,c)] for c in customers for w in warehouse])


   for c in customers:
       model1+= pl.lpSum([flows[(w,c)] for w in warehouse])== 1
    

   model1+= pl.lpSum([open_w[(w)] for w in warehouse])== n


   for w in warehouse:
      model1+= open_w[(w)]>= flows[(w,'city 1')]
      model1+= open_w[(w)]>= flows[(w,'city 2')]
      model1+= open_w[(w)]>= flows[(w,'city 3')]
      model1+= open_w[(w)]>= flows[(w,'city 4')]
      model1+= open_w[(w)]>= flows[(w,'city 5')]
      model1+= open_w[(w)]>= flows[(w,'city 6')]
      model1+= open_w[(w)]>= flows[(w,'city 7')]

   model1.solve()
   average_distance= pl.value(model1.objective)/sum(demand)
   n_warehouses_opened= sum([open_w[(w)].varValue for w in warehouse])
   avg_warehouse_distance= {n_warehouses_opened: average_distance}
   return avg_warehouse_distance

empty_dict= list(dict())

n_warehouses= [1,2,3,4,5,6,7]

for n in n_warehouses:
     model1= pulp_model(n)
     empty_dict.append(model1)
empty_dict







