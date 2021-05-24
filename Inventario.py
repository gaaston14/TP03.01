import  random as rd
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
    inv_level += amount
    time_next_event[1] = 10**30

def demand():
    inv_level -= random_integer(prob_distrib_demand)
    time_next_event[2] = sim_time + expon(mean_interdemand)

def evaluate():
    if(inv_level < smalls):
        amount = bigs - inv_level
        total_ordering_cost +=setup_cost + incremental_cost * amount
        tome_next_event[1] = sim_time + uniform(minlag, maxlag)
    time_next_event[4] = sim_time + 1.0

def report():
    avg_ordering_cost = total_ordering_cost / num_months
    avg_holding_cost = holding_cost * area_holding / num_months
    aux=avg_ordering_cost+avg_holding_cost+avg_shortage_cost
    print(smalls, bigs, aux, avg_ordering_cost, avg_holding_cost, avg_shortage_cost)

def update_time_avg_stats():
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time
    if(inv_level < 0):
        area_shortage -= inv_level * time_since_last_event
    elif (inv_level > 0):
        area_holding += inv_level * time_since_last_event

def random_integer(prob_distrib):
    u=rd.uniform(0,1)
    for i in prob_distrib[i]:

def unirform(a,b):
    return a + rd.uniform(0,1) - (b-a)

if __name__ == '__main__':
    num_events = 4
