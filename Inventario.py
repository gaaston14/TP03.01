import random as rd
import math
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
    global inv_level,time_last_event,total_ordering_cost,area_holding,area_shortage
    sim_time = 0.0
    inv_level= initial_inv_level
    time_last_event = 0.0
    total_ordering_cost = 0.0
    area_holding = 0.0
    area_shortage = 0.0
    time_next_event[1] = 10**30
    time_next_event[2] = sim_time + expon(mean_interdemand)
    time_next_event[3] = num_months
    time_next_event[4] = 0.0

def order_arrival():
    global inv_level
    inv_level =inv_level + amount
    time_next_event[1] = 10**30

def demand():
    global inv_level
    inv_level =(inv_level) - random_integer(prob_distrib_demand)
    time_next_event[2] = sim_time + expon(mean_interdemand)

def evaluate():
    global total_ordering_cost,sim_time
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
    print(smalls, bigs,aux , avg_ordering_cost, avg_holding_cost, avg_shortage_cost)

def update_time_avg_stats():
    global time_last_event,area_shortage,area_holding
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time
    if(inv_level < 0):
        area_shortage =area_shortage-(inv_level * time_since_last_event)
    elif (inv_level > 0):
        area_holding =area_holding+inv_level * time_since_last_event

def random_integer(prob_distrib:list):
    a=0.0
    u=rd.uniform(0,1)
    for i in prob_distrib:
        if u>=i:
            a=i
    return a


def uniform(a,b):
    return ((a + rd.uniform(0,1)) * (b-a))

def expon(mean):
    U = rd.uniform(0,1)
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
    if (next_event_type <0):
        print('Event list empty at time') #aca va el sim_time pero no me lo toma
    sim_time=min_time_next_event



if __name__ == '__main__':
    smallsArreglo=20
    bigsArreglo=40
    num_events = 4
    initial_inv_level=60
    num_months=120
    num_policies=1
    num_values_demand=4
    mean_interdemand=0.10
    setup_cost=32
    incremental_cost=3
    holding_cost=1
    shortage_cost=5*4
    minlag=0.5
    maxlag=1
    prob_distrib_demand=[0.167,0.500,0.833,1.00]
    #Run the simulation varying the invetory policy
    for i in range(num_policies):
        smalls = smallsArreglo
        bigs = bigsArreglo
        initialize()
        while (next_event_type!=3) :
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


