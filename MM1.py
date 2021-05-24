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

def Report():
    global NumCustsDelayed
    AvgDelayInQ = TotalOfDelays/NumCustsDelayed
    AvgNumInQ = AreaNumInQ/Time
    AvgNumInSys = AreaNumInS/Time
    AvgTimeInSys = AvgDelayInQ+1/MeanService
    ServerUtilization = AreaServerStatus/Time
    # print("Promedio de espera en la cola: ",round(AvgDelayInQ,3)," minutos.")
    # print("Promedio de largo de la cola: ",round(AvgNumInQ,3)," clientes.")
    # print("Utilización del servidor: ",round(ServerUtilization,3))
    # print("Tiempo de finalización: ",round(Time,3))
    return [AvgNumInQ,AvgDelayInQ, ServerUtilization, AvgNumInSys,AvgTimeInSys, ArrayCantClientesEnCola, AreaQArray]


def Initialize():
    global MeanInterarrival, Time,TotTime, TimeNextEvent,AreaNumInS, ServerStatus, NumCustsDelayed, TotalOfDelays, AreaNumInQ, AreaServerStatus, NextEventType, NumDelaysRequired, NumInQ, MeanService, TimeLastEvent, TimeArrival, NumInSys, AreaQArray, TiemposArray, ArrayCantClientesEnCola
    Time = 0

    ServerStatus = IDLE

    #variables enteras
    NextEventType = 0
    NumCustsDelayed = 0
    NumInQ = 0 #número de clientes en cola
    ServerStatus = 0
    NumInSys = 0 #nùmero de clientes en el sistema

    ArrayCantClientesEnCola = []

    AreaQArray=[]
    TiemposArray=[]

    #variables reales
    AreaNumInQ = 0 #área debajo de la función número de clientes en cola
    AreaNumInS = 0
    AreaServerStatus = 0
    Time = 0
    TotTime = 0
    TimeLastEvent = 0 #tiempo del último evento que cambió el número en cola
    TotalOfDelays = 0 #número de clientes que completaron sus demoras

    #arrays
    TimeArrival = np.zeros([NumDelaysRequired+1])
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
    global ServerStatus,TimeArrival, TotalOfDelays, NumCustsDelayed, TimeNextEvent, NumInQ, MeanService, NumInSys 
    TimeNextEvent[1] = Time + funExpon(1/MeanInterarrival)
    NumInSys += 1
    #print("arribo")
    if ServerStatus == BUSY:    
        NumInQ += 1   
        TimeArrival[NumInQ] = Time
        
    else:
        Delay = 0
        TotalOfDelays = TotalOfDelays + Delay
    
        NumCustsDelayed = NumCustsDelayed + 1

        ServerStatus = BUSY

        TimeNextEvent[2] = Time + funExpon(1/MeanService)
    
def Depart():
    global NumInQ, TotalOfDelays,NumCustsDelayed, ServerStatus, TimeNextEvent, Time, TimeArrival, NumInSys
    NumInSys -= 1 
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
    global TimeLastEvent, AreaNumInQ, AreaNumInS, AreaServerStatus, Time,TotTime, NumInSys, AreaQArray
    TotTime += TimeLastEvent
    TimeSinceLastEvent = Time - TimeLastEvent
    TimeLastEvent = Time

    AreaNumInQ = AreaNumInQ + NumInQ * TimeSinceLastEvent
    AreaNumInS = AreaNumInS + NumInSys * TimeSinceLastEvent
    AreaServerStatus = AreaServerStatus + ServerStatus * TimeSinceLastEvent

    if len(AreaQArray) <= 100:
        AreaQArray.append(NumInQ)
        TiemposArray.append(TimeLastEvent)

    ArrayCantClientesEnCola.append(NumInQ)

def ExecuteSimulation():
    global NumCustsDelayed, NumDelaysRequired
    Initialize()
    while(NumCustsDelayed < NumDelaysRequired):
        Timing()
        UpdateTimeAvgStats()
        #print(NumCustsDelayed)
        if (NextEventType == 1):
            Arrive()
        elif (NextEventType == 2):
            Depart()
        else:
            print ("Error in NextEventType, Value =  ",NextEventType)

    return Report()

if __name__ == '__main__':
    global MeanInterarrival, MeanService, NumDelaysRequired
    list_MeanInterarrival = [25,50,75] #tiempo medio de llegada **lambda
    MeanService = 100 #tiempo medio de servicio **MU
    NumDelaysRequired = 10000 #número total de clientes cuyas demoras serán observadas

    '''print("Mean Interarrival")
    MeanInterarrival = float(input())
    print("Mean Service")
    MeanService = float(input())
    print("Number delays Required")
    NumDelaysRequired = float(input())'''

    # print("Mean Interarrival: ",MeanInterarrival,"Mean Service: ",MeanService,"Number delays Required (cuantas personas  ): ", NumDelaysRequired)

    for MeanInterarrival in list_MeanInterarrival:
        #Valores teóricos
        promedio_clientes_en_cola = (MeanInterarrival**2)/(MeanService*(MeanService-MeanInterarrival))
        promedio_demora_en_cola = MeanInterarrival/(MeanService*(MeanService-MeanInterarrival))
        promedio_utilizacion_servidor = MeanInterarrival/MeanService
        promedio_clientes_en_sistema = MeanInterarrival/(MeanService-MeanInterarrival)
        promedio_tiempo_cliente_sistema = 1/(MeanService-MeanInterarrival)

        print(promedio_clientes_en_cola, "  ",promedio_demora_en_cola, "  ", promedio_utilizacion_servidor,"  ",promedio_clientes_en_sistema,"  ",promedio_tiempo_cliente_sistema)

        clientes_en_cola = []
        demora_en_cola = []
        utilizacion_servidor = []
        clientes_en_sistema = []
        tiempo_prom_en_sistema = []
        cant_clientes_en_cola = []

        n = 10
        for i in range(n):
            rta = ExecuteSimulation()
            clientes_en_cola.append(rta[0])
            demora_en_cola.append(rta[1])
            utilizacion_servidor.append(rta[2])
            clientes_en_sistema.append(rta[3])
            tiempo_prom_en_sistema.append(rta[4])
            cant_clientes_en_cola.append(rta[5])

        lista_clientes_en_cola = []
        lista_demora_en_cola = []
        lista_utilizacion_servidor = []
        lista_clientes_en_sistema = []
        lista_tiempo_prom_en_sistema = []


        '''for i in range(n):
            clientes_en_cola_i = statistics.mean(clientes_en_cola[:i+1])
            lista_clientes_en_cola.append([i,clientes_en_cola_i])
            demora_promedio_i = statistics.mean(demora_en_cola[:i+1])
            lista_demora_en_cola.append([i,demora_promedio_i])
            utilizacion_servidor_i = statistics.mean(utilizacion_servidor[:i+1])
            lista_utilizacion_servidor.append([i,utilizacion_servidor_i])
            clientes_en_sistema_i = statistics.mean(clientes_en_sistema[:i+1])
            lista_clientes_en_sistema.append([i,clientes_en_sistema_i])
            tiempo_prom_en_sistema_i=statistics.mean(tiempo_prom_en_sistema[:i+1])
            lista_tiempo_prom_en_sistema.append([i,tiempo_prom_en_sistema_i])
        
        plt.title('Número promedio de clientes en cola \n con tasa de arribo del '+str(MeanInterarrival)+'%') 
        x1, y1 = zip(*[m for m in lista_clientes_en_cola])
        p1 = plt.plot(x1, y1, markersize=1, lw=1,color='r')
        plt.plot([promedio_clientes_en_cola for i in range(n)], linestyle='dashed', color='blue')
        plt.grid(True)
        plt.savefig('promedio de clientes en cola_'+str(MeanInterarrival)+'.png')
        plt.show()

        x, y = zip(*[m for m in lista_demora_en_cola])
        plt.title('Número promedio de demora en cola \n con tasa de arribo del '+str(MeanInterarrival)+'%') 
        plt.plot(x, y, markersize=1, lw=1,color='b')
        plt.plot([promedio_demora_en_cola for i in range(n)], linestyle='dashed', color='blue')
        plt.grid(True)
        plt.savefig('promedio de demora en cola_'+str(MeanInterarrival)+'.png')
        plt.show()

        x, y = zip(*[m for m in lista_utilizacion_servidor])
        plt.title('Utilización promedio del servidor \n con tasa de arribo del '+str(MeanInterarrival)+'%') 
        plt.plot(x, y, markersize=1, lw=1,color='g')
        plt.plot([promedio_utilizacion_servidor for i in range(n)], linestyle='dashed', color='blue')
        plt.grid(True)
        plt.savefig('Utilización promedio del servidor_'+str(MeanInterarrival)+'.png')
        plt.show()

        x, y = zip(*[m for m in lista_clientes_en_sistema])
        plt.title('Promedio de clientes en el sistema \n con tasa de arribo del '+str(MeanInterarrival)+'%') 
        plt.plot(x, y, markersize=1, lw=1,color='g')
        plt.plot([promedio_clientes_en_sistema for i in range(n)], linestyle='dashed', color='blue')
        plt.grid(True)
        plt.savefig('Promedio de clientes en el sistema_'+str(MeanInterarrival)+'.png')
        plt.show()

        x, y = zip(*[m for m in lista_tiempo_prom_en_sistema])
        plt.title('Tiempo promedio de clientes en el sistema \n con tasa de arribo del '+str(MeanInterarrival)+'%') 
        plt.plot(x, y, markersize=1, lw=1,color='g')
        plt.plot([promedio_tiempo_cliente_sistema for i in range(n)], linestyle='dashed', color='blue')
        plt.grid(True)
        plt.savefig('Tiempo promedio de clientes en el sistema_'+str(MeanInterarrival)+'.png')
        plt.show()'''


        #Grafica de cantidad promedio de clientes en cola
        k = 11
        prob_cant_clientes_i = []
        for i in range(0,k):         
            prob_cant_clientes_i.append(cant_clientes_en_cola[0].count(i)/len(cant_clientes_en_cola[0]))

        plt.title('Probabilidad de encontrar n clientes en la cola')
        plt.bar(range(0,k),(prob_cant_clientes_i))
        plt.ylabel("Probabilidad")
        plt.xlabel("Cantidad de clientes en cola")
        plt.ylim(0,max(prob_cant_clientes_i)*1.2)
        plt.xlim(-1,k)   
        plt.savefig('Probabilidad de n clientes en cola_'+str(MeanInterarrival)+'.png')
        plt.show()
                
        #Grafica de cantidad de clientes en cada intervalo de tiempo (no finalizada)
        '''plt.title('Clientes') 
        plt.grid(True)
        plt.plot(TiemposArray, AreaQArray, color='b')
        plt.show()'''