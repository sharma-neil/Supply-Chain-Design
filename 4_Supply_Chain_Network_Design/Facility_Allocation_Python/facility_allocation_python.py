#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:43:18 2020

@author: haythamomar
"""
import pandas as pd
from pulp import *

dist= pd.read_excel('warehouse_city.xlsx')

dist= dist.set_index('Warehouse')


demand=[10000,20000,33000,9000,60000,2500,35000]
warehouse= dist.index
customers= dist.columns

keys= [(w,c) for w in warehouse for c in customers]

dist_dict= { (w,c): dist.loc[w,c] for w in warehouse for c in customers}


flows= LpVariable.dicts('flows',keys,cat='Binary')
open_w= LpVariable.dicts('open_w',warehouse,cat='Binary')

demand_dict= dict(zip(customers,demand))

model= LpProblem('w_alloc',LpMinimize)

model+= lpSum([demand_dict[(c)]* flows[(w,c)]* dist_dict[(w,c)] for c in customers for w in warehouse])


for c in customers:
    model+= lpSum([flows[(w,c)] for w in warehouse])== 1
    

model+= lpSum([open_w[(w)] for w in warehouse])==3



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

average_distance= value(model.objective)/sum(demand)
n_warehouses_opened= sum([open_w[(w)].varValue for w in warehouse])

#### a simulation for distance Vs No of warhouses

def pulp_model(n):

   
   model1= LpProblem('w_alloc',LpMinimize)

   model1+= lpSum([demand_dict[(c)]* flows[(w,c)]* dist_dict[(w,c)] for c in customers for w in warehouse])


   for c in customers:
       model1+= lpSum([flows[(w,c)] for w in warehouse])== 1
    

   model1+= lpSum([open_w[(w)] for w in warehouse])== n


   for w in warehouse:
      model1+= open_w[(w)]>= flows[(w,'city 1')]
      model1+= open_w[(w)]>= flows[(w,'city 2')]
      model1+= open_w[(w)]>= flows[(w,'city 3')]
      model1+= open_w[(w)]>= flows[(w,'city 4')]
      model1+= open_w[(w)]>= flows[(w,'city 5')]
      model1+= open_w[(w)]>= flows[(w,'city 6')]
      model1+= open_w[(w)]>= flows[(w,'city 7')]

   model1.solve()
   average_distance= value(model1.objective)/sum(demand)
   n_warehouses_opened= sum([open_w[(w)].varValue for w in warehouse])
   avg_warehouse_distance= {n_warehouses_opened: average_distance}
   return avg_warehouse_distance

empty_dict= list(dict())

n_warehouses= [1,2,3,4,5,6,7]

for n in n_warehouses:
     model1= pulp_model(n)
     empty_dict.append(model1)
empty_dict







