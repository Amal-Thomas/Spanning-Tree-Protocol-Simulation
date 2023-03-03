from bridge import Bridge, ExtendedLAN

trace_flag = input()
Num_Bridges = input()
B = [] #Objects of Bridge Class
L = [] #Objects of ExtendedLAN Class
for i in range(int(Num_Bridges)):
    LANs_= []
    LANs_= input().split()[1:]
    NumLANs = len(LANs_) 
    LANs=[] #A 1/0 list of 26 entries to denote if a LAN is connected to a bridge or not
    for j in range(26):
        LANs.append(0)
    for j in range(len(LANs_)):
        LANs[ord(LANs_[j])-65] = 1
    B.append(Bridge(LANs, NumLANs, i,trace_flag))
#Initializing the Bridge Objects

Bridges = [[1 for i in range(int(Num_Bridges))] for j in range(26)]
for i in range(int(Num_Bridges)):
    for j in range(26):
        Bridges[j][i]=B[i].LANs[j]
#Creating a Network Graph, i.e., A 1/0 matrix of LANs x Bridges

for j in range(26):
    L.append(ExtendedLAN(Bridges[j], Num_Bridges, j,B))
#Initializing the ExtendedLAN Objects

t=0 #time is set as zero
for i in range(int(Num_Bridges)): 
    B[i].send(t)
#Packets placed in the Send Buffers of each Bridge
        
for i in range(26):
    L[i].transmit_packets()
#Packets reaching the LANs
        
for i in range(int(Num_Bridges)):
    for j in range(26):
        if B[i].LANs[j]==1:
            if B[i].Status[j]!="NP":
                B[i].ReceiveBuffer[j]=B[i].ReceiveBuffer[j]+L[j].incoming    
#Packets placed in the Receive Buffers of each Bridge
    
for j in range(26):
    L[j].incoming.clear()
#Clearing the messages in the incoming buffer of each LAN after successful transmission

previous_best_config_copy=[]
for i in range(int(Num_Bridges)):
    r=B[i].best_config.copy()
    previous_best_config_copy.append(r[0])
    previous_best_config_copy.append(r[1])
    previous_best_config_copy.append(r[2])
previous_best_config = previous_best_config_copy.copy()  
#Storing the best configuration messages of each bridge in a single list
#This list is then compared with the best configuration messages after the processing of the messages

t=1   #Initialized messages reach the respective Bridges after 1s

while True:        
    for i in range(int(Num_Bridges)):
        B[i].receive(t)
    #After Receiving the messages, they are checked by each Bridge to find a better configuration message
       
    for i in range(int(Num_Bridges)):
        for j in range(26):
            if B[i].LANs[j]:
                B[i].ReceiveBuffer[j].clear()
    #The Receive Buffer of each Bridge is cleared
                
    for j in range(26):
        L[j].incoming.clear()
    #Clearing the messages in the incoming buffer of each LAN in every iteration
        
    for i in range(int(Num_Bridges)):
        B[i].send(t)
    #Packets placed in the Send Buffers of each Bridge
        
    for i in range(26):
        L[i].transmit_packets()
    #Packets reaching the LANs
        
    for i in range(int(Num_Bridges)):
        for j in range(26):
            A=L[j].incoming[:]
            if B[i].LANs[j]==1:
                if B[i].Status[j]!="NP":
                    B[i].ReceiveBuffer[j]=B[i].ReceiveBuffer[j]+A
    #Packets placed in the Receive Buffers of each Bridge

    current_best_config_copy = []                
    for i in range(int(Num_Bridges)):
        s=B[i].best_config.copy()
        current_best_config_copy.append(s[0])
        current_best_config_copy.append(s[1])
        current_best_config_copy.append(s[2])
    current_best_config = current_best_config_copy.copy()
    #Storing the best configuration messages of each bridge in a single list
    #This list is then compared with the best configuration messages before the processing of the messages

    if current_best_config == previous_best_config:
        break
    #The simulation ends when there is no change in any of the best configuration messages of any bridge

    previous_best_config = current_best_config.copy() 
    
    t = t + 1  #time incremented
    
    
for i in range(int(Num_Bridges)):
    print(f'B{i+1}:', end = " ")
    for j in range(26):
        if B[i].LANs[j]:
            print(f'{chr(65+j)}-{B[i].Status[j]}', end = " ")
    print('\n', end='')
#Printing the final status of each port of all the bridges