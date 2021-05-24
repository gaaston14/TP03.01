import sys
import numpy as np
import statistics
import matplotlib.pyplot as plt

from MM1Utiles import funExpon

#README
#Criterio de estabilidad MM1: la tasa de servicio debe ser mayor que la tasa de llegada

NumEvents = 2 #Defimos número de tipos de eventos (usamos 2: arribos y llegadas)

#Constantes a usar para entender mejor el código
BUSY = 1 
IDLE = 0

#QLIMIT = 10**5 #Hay que probar cambiando

def Report():
    global NumCustsDelayed, NumRejected
    return NumRejected/NumArrivals



def Initialize():
    global MeanInterarrival, Time, TimeNextEvent, ServerStatus, NumCustsDelayed, TotalOfDelays, \
        AreaNumInQ, AreaServerStatus, NextEventType, NumDelaysRequired, NumInQ, MeanService, TimeLastEvent, TimeArrival, NumRejected, NumArrivals
    Time = 0

    ServerStatus = IDLE

    #variables enteras
    NextEventType = 0
    NumCustsDelayed = 0
    NumInQ = 0 #número de clientes en cola
    ServerStatus = 0
    NumRejected = 0
    NumArrivals = 0

    #variables reales
    AreaNumInQ = 0 #área debajo de la función número de clientes en cola
    AreaServerStatus = 0
    Time = 0
    TimeLastEvent = 0 #tiempo del último evento que cambió el número en cola
    TotalOfDelays = 0 #número de clientes que completaron sus demoras

    #arrays
    TimeArrival = np.zeros([QLIMIT+1])
    TimeNextEvent = np.zeros([NumEvents+1]) #arreglo que contiene el tiempo del próximo evento I en la posición TimeNextEvent[I]


    TimeNextEvent[1] = Time + funExpon(1/MeanInterarrival)
    TimeNextEvent[2] = 10**30

def Timing():
    global Time, NextEventType

    MinTimeNextEvent = 10**29
    NextEventType = 0

    for i in range(1,NumEvents+1):
        if TimeNextEvent[i] < MinTimeNextEvent:
            MinTimeNextEvent = TimeNextEvent[i]
            NextEventType = i

    if (NextEventType > 0):
        Time = TimeNextEvent[NextEventType]
    else:
        print("La lista de eventos está vacía en el momento: ", Time, " NextEventType == 0, error en timing")
        sys.exit()
        
def Arrive():
    global ServerStatus,TimeArrival, TotalOfDelays, NumCustsDelayed, TimeNextEvent, NumInQ, MeanService, NumRejected, NumArrivals
    TimeNextEvent[1] = Time + funExpon(1/MeanInterarrival)
    NumArrivals += 1
    if ServerStatus == BUSY:    
        NumInQ += 1   
        if NumInQ > QLIMIT:
            #print(NumRejected)
            NumInQ -= 1
            NumRejected += 1
        else:
            TimeArrival[NumInQ] = Time
        
    else:
        Delay = 0
        TotalOfDelays = TotalOfDelays + Delay
    
        NumCustsDelayed = NumCustsDelayed + 1

        ServerStatus = BUSY

        TimeNextEvent[2] = Time + funExpon(1/MeanService)
    
def Depart():
    global NumInQ, TotalOfDelays,NumCustsDelayed, ServerStatus, TimeNextEvent, Time, TimeArrival
    if (NumInQ == 0):
        ServerStatus = IDLE
        TimeNextEvent[2] = 10**30
    else:
        NumInQ = NumInQ - 1

        Delay = Time - TimeArrival[1]
        TotalOfDelays = TotalOfDelays + Delay

        NumCustsDelayed += 1
        TimeNextEvent[2] = Time + funExpon(1/MeanService)

        for I in range(1,NumInQ+1):
            TimeArrival[I] = TimeArrival[I+1]

def UpdateTimeAvgStats():
    global TimeLastEvent, AreaNumInQ, AreaServerStatus, Time
    TimeSinceLastEvent = Time - TimeLastEvent
    TimeLastEvent = Time

    AreaNumInQ = AreaNumInQ + NumInQ * TimeSinceLastEvent

    AreaServerStatus = AreaServerStatus + ServerStatus * TimeSinceLastEvent

def ExecuteSimulation():
    global NumCustsDelayed, NumDelaysRequired
    Initialize()
    while(NumCustsDelayed < NumDelaysRequired):
        Timing()
        UpdateTimeAvgStats()
        if (NextEventType == 1):
            Arrive()
        elif (NextEventType == 2):
            Depart()
        else:
            print ("Error in NextEventType, Value =  ",NextEventType)

    return Report()


if __name__ == '__main__':
    global MeanInterarrival, MeanService, NumDelaysRequired, QLIMIT
    MeanInterarrival = 2.5 #tiempo medio de llegada **lambda
    MeanService = 10 #tiempo medio de servicio **MU
    NumDelaysRequired = 10000 #número total de clientes cuyas demoras serán observadas

    print("Mean Interarrival: ",MeanInterarrival,"Mean Service: ",MeanService,"Number delays Required (cuantas personas  ): ", NumDelaysRequired)


    lista_media_arribos = [2.5, 5, 7.5, 10, 12.5]
    lista_limites_cola = [0, 2, 5, 10, 50]
    lista_conjunto = []

    
    for limiteCola in reversed(lista_limites_cola):
        lista_individual = []
        for mediaArribo in reversed(lista_media_arribos):
            MeanInterarrival = mediaArribo
            QLIMIT = limiteCola
            n = 10
            lista_recahzados = []
            for i in range(n):
                rta = ExecuteSimulation()
                lista_recahzados.append(rta)
            lista_individual.append([mediaArribo,round(statistics.mean(lista_recahzados),4)])
            print(round(MeanInterarrival*MeanService,0), "\% & ", QLIMIT , " & ", round(statistics.mean(lista_recahzados),4), "\\\\")
        lista_conjunto.append([limiteCola, lista_individual])

    for limiteCola, lista_individual in lista_conjunto:
        print(limiteCola,lista_individual)
        lista_relacion = []
        lista_probDenegado = []
        for i,j in lista_individual:
            lista_relacion.append(i*10)
            lista_probDenegado.append(j)
        plt.title('probabilidad de denegación de \nservicio con limite de cola = '+ str(limiteCola)) 
        plt.plot(lista_relacion, lista_probDenegado, markersize=1, lw=1,color='r')
        plt.grid(True)
        plt.xlabel('Porcentaje de arribo con respecto al servicio')
        plt.ylabel('Probabilidad de denegación')
        plt.savefig('Prob_denegación_'+str(limiteCola)+'.png')
        plt.show()

    
    

    


