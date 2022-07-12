#Neil Sharma

import pulp as pl

#profit price per feather, cotton, and silk respectively
feather = 33
cotton = 40
silk = 34

# x1 req 0.4 feather, 0.2 cotton and 0.3 silk
# x2 req 0.7 feather, 0.5 cotton and 0.3 silk
# x3 req 0.4 feather, 0.6 cotton and 0.2 silk
# available supply for feather is 40, cotton is 30 and silk is 35

model = pl.LpProblem('Maximum Profit',pl.LpMaximize)

X1= pl.LpVariable('X1',0,None,'Integer')
X2= pl.LpVariable('X2',0,None,'Integer')
X3 = pl.LpVariable('X3',0,None,'Integer')

model += (X1*feather)+(X2*cotton)+(X3*silk)

model += (X1*0.4)+(X2*0.7)+(X3*0.4)<=40
model += (X1*0.2)+(X2*0.5)+(X3*0.6)<=40
model += (X1*0.3)+(X2*0.3)+(X3*0.2)<=40

model.solve()

X1.varValue
X2.varValue
X3.varValue


