from gurobipy import *
import numpy as np
import math
import readIn


def solve(full_path_instance):
    
    nBakeryProducts, Timehorizon, l, h, K, a, d, s, st = readIn.readFile(full_path_instance)
    Timehorizon = Timehorizon+1
    
    
    #-Define model variables----------------------------------------------
    
    model = Model("lotSizing")

    # number of pieces of product i available at time t
    x = {}
    for i in range(1,nBakeryProducts+1):
        for t in range(1,Timehorizon):
            x[i,t] = model.addVar(lb=0,vtype=GRB.INTEGER, obj=0, name="x_"+str(i)+"_"+str(t))
            
    # warehousing-costs for each product and timestep
    y = {}
    for i in range(1,nBakeryProducts+1):
        for t in range(Timehorizon):
            y[i,t] = model.addVar(lb=0,vtype=GRB.INTEGER, obj=0, name="y_"+str(i)+"_"+str(t))
            
    # number of each product i in the warehouse at time t
    z = {}
    for i in range(1,nBakeryProducts+1):
        for t in range(Timehorizon):
            z[i,t] = model.addVar(lb=0,vtype=GRB.INTEGER, obj=0, name="z_"+str(i)+"_"+str(t))
         
    # cost for changing currently produced product in the oven
    u = {}
    for t in range(1,Timehorizon):
        u[t] = model.addVar(lb=0,vtype=GRB.INTEGER, obj=0, name="u_"+str(i)+"_"+str(t))
            
    # will product i be produced at time t?       
    v = {}
    for i in range(1,nBakeryProducts+1):
        for t in range(1,Timehorizon):
            v[i,t] = model.addVar(lb=0, ub = 1,vtype=GRB.INTEGER, obj=0, name="v_"+str(i)+"_"+str(t))
            
    # what product will the oven be prepared for at the end of the period?
    w = {}
    for i in range(1,nBakeryProducts+1):
        for t in range(Timehorizon):
            w[i,t] = model.addVar(lb=0, ub = 1,vtype=GRB.INTEGER, obj=0, name="w_"+str(i)+"_"+str(t))
         
        
    model.update()
    
    
    #-Add constraints-----------------------------------------------
    
    # add initial stock to the warehouse
    for i in range(1,nBakeryProducts+1):
        model.addConstr(z[i,0] == l[i-1], name = 'c0')
            
    # write warehousing costs to y
    for t in range(Timehorizon):
        for i in range(1,nBakeryProducts+1):
            model.addConstr(y[i,t] == z[i,t] * h[i-1], name = 'c1')
            
    # add newly produced products to the warehouse(z), and release products the customers demand
    for t in range(1,Timehorizon):
        for i in range(1,nBakeryProducts+1):
            model.addConstr(z[i,t] == z[i,t-1] + x[i,t] - d[i-1][t-1], name = 'c2')
        
    # set x = currently produced products (use the time available to produce products and assign them to x)
    for t in range(1,Timehorizon):
        model.addConstr(quicksum(x[i,t]*a[i-1] for i in range(1,nBakeryProducts+1)) + quicksum(st[i-1][j-1]*v[j,t]*w[i,t-1] for i in range(1,nBakeryProducts+1) for j in range(1,nBakeryProducts+1)) <= (K[t-1]), name = 'c3')
            
    # maximum 2 different products can be produced per timestep
    for t in range(1,Timehorizon):
        model.addConstr(quicksum(v[i,t] for i in range(1,nBakeryProducts+1)) <= 2, name = 'c4')
        
    # only produce products, that may be produced currently (v = 1)
    for t in range(1,Timehorizon):
        for i in range(1,nBakeryProducts+1):
            model.addConstr(x[i,t] == v[i,t]*x[i,t], name = 'c5')
            
    # a product can only be produced, if the oven was prepared for it at the end of the previous period or at the current one
    for t in range(1,Timehorizon):
        for i in range(1,nBakeryProducts+1):
            model.addConstr(v[i,t] == w[i,t-1]+w[i,t], name = 'c6')
        
    # set w = product that the oven is prepared for at the begin of timestep t
    for t in range(Timehorizon):
        model.addConstr(quicksum(w[i,t] for i in range(1,nBakeryProducts+1)) == 1, name = 'c7')
        
    # set u = cost to change product produced in the oven
    for t in range(1,Timehorizon):
        model.addConstr(u[t] == quicksum(w[i,t-1]*s[i-1][j-1]*w[j,t] for i in range(1,nBakeryProducts+1) for j in range(1,nBakeryProducts+1)), name = 'c8')
    
        
    # set the objective to the sum of all costs (warehousing costs + changing product costs + warehousing costs for step 0)
    model.setObjective(quicksum(y[i,t] for i in range(1,nBakeryProducts+1) for t in range(1, Timehorizon)) + quicksum(u[t] for t in range(1, Timehorizon)) + quicksum(l[i-1]*h[i-1] for i in range(1,nBakeryProducts+1)))
            
    model.optimize()
    
    
    
    #-Print result----------------------------------------------
    if model.status == GRB.status.OPTIMAL:
        for i in range(1,nBakeryProducts+1):
            #print('Von Ware %s sind zum Zeitpunkt %s genau %s Teile auf Lager .' % (i,  t, z[i,t].x))
            break

    '''        
    for t in range(1,Timehorizon):
        for i in range(1,nBakeryProducts+1):
            print('x_%s_%s: %s' % (i,t, x[i,t].x))
    '''

    return model
            

# call the method to see the results
solve('lotData1.txt')
