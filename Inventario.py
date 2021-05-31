import random as rd
import math
import sys
import numpy as np

#Seteo de variables enteras
amount=0
bigs=0
initial_inv_level=0
inv_level=0
next_event_type=0
num_events = 0
num_months=0
num_values_demand=0
smalls=0
avg_shortage_cost=0
#Seteo de variables flotantes
area_holding=0.0
area_shortage=0.0
holding_cost=0.0
incremental_cost=0.0
maxlag=0.0
mean_interdemand=0.0
minlag=0.0
setup_cost=0.0
shortage_cost=0.0
sim_time=0.0
time_last_event=0.0
total_ordering_cost=0.0

#seteo de listas flotantes
prob_distrib_demand=[]
for i in range(26):
    prob_distrib_demand.append(0.0)
time_next_event=[]
for i in range(5):
    time_next_event.append(0.0)

def initialize():
    global inv_level,time_last_event,total_ordering_cost,area_holding,area_shortage,sim_time,time_next_event,next_event_type
    sim_time = 0.0
    inv_level= initial_inv_level
    time_last_event = 0.0
    total_ordering_cost = 0.0
    area_holding = 0.0
    area_shortage = 0.0
    next_event_type=0
    time_next_event[1] = 10**30
    time_next_event[2] = sim_time + expon(mean_interdemand)
    time_next_event[3] = num_months
    time_next_event[4] = 0.0

def order_arrival():
    global inv_level,time_last_event,amount
    inv_level =inv_level + amount
    time_next_event[1] = 10**30

def demand():
    global inv_level,time_next_event
    sizedemand=random_integer(prob_distrib_demand)
    inv_level =inv_level - sizedemand
    time_next_event[2] = sim_time + expon(mean_interdemand)

def evaluate():
    global total_ordering_cost,sim_time,time_next_event,amount
    if(inv_level < smalls):
        amount = bigs - inv_level
        total_ordering_cost = total_ordering_cost+ setup_cost + incremental_cost * amount
        time_next_event[1] = sim_time + uniform(minlag, maxlag)
    time_next_event[4] = sim_time + 1.0

def report():
    avg_ordering_cost = total_ordering_cost / num_months
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_shortage_cost = shortage_cost*area_shortage/num_months
    aux=avg_ordering_cost+avg_holding_cost+avg_shortage_cost
    print(c)
    print(smalls, bigs,aux , avg_ordering_cost, avg_holding_cost, avg_shortage_cost)

def update_time_avg_stats():
    global time_last_event,area_shortage,area_holding
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time
    if(inv_level < 0):
        area_shortage =area_shortage-inv_level * time_since_last_event
    elif (inv_level > 0):
        area_holding =area_holding+inv_level * time_since_last_event

def random_integer(prob_distrib:list):
    b=1
    u=np.random.uniform(0,1)
    for a,i in enumerate(prob_distrib):
        if u>=i:
            b=b+a
    return b


def uniform(a,b):
    return (a + np.random.uniform(0,1) * (b-a))

def expon(mean):
    U = np.random.uniform(0,1)
    return -(mean)*math.log(U)

def timing():
    global sim_time,next_event_type
    min_time_next_event= 10**29
    next_event_type =0
    '''for i in range(1,num_events,1):
        if time_next_event[i]<min_time_next_event:
            min_time_next_event= time_next_event[i]
            next_event_type = i'''
    for i in range(1,num_events+1):
        if time_next_event[i]<min_time_next_event:
            min_time_next_event=time_next_event[i]
            next_event_type=i
    if (next_event_type ==0):
        print('Event list empty at time') #aca va el sim_time pero no me lo toma
        sys.exit()
    sim_time=min_time_next_event



if __name__ == '__main__':
    smallsArreglo=[20,20,20,20,40,40,40,60,60]
    bigsArreglo=[40,60,80,100,60,80,100,80,100]
    num_events = 4
    initial_inv_level=60
    num_months=120
    num_policies=9
    num_values_demand=4
    mean_interdemand=0.10
    setup_cost=32
    incremental_cost=3.0
    holding_cost=1.0
    shortage_cost=5*4
    minlag=0.5
    maxlag=1
    prob_distrib_demand=[0.167,0.500,0.833,1.00]
    #Run the simulation varying the invetory policy
    for a,i in enumerate(smallsArreglo):
        smalls = i
        bigs = bigsArreglo[a]
        initialize()
        while (next_event_type!=3) :
            c=c+1
            timing()
            update_time_avg_stats()
            if(next_event_type==1):
                order_arrival()
            elif(next_event_type==2):
                demand()
            elif(next_event_type==3):
                report()
            elif(next_event_type==4):
                evaluate()


