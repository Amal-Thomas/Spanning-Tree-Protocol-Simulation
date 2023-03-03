class Bridge():
    def __init__(self, LANs, NumLANs, i, trace_flag):
        self.LANs = LANs              #A 1/0 list of 26 entries to denote if a LAN is connected to a bridge or not
        self.NumLANs = NumLANs        #Number of connected LANs
        self.i = i                    #Bridge index
        self.trace_flag = trace_flag  #Storing the trace flag
        self.rootbridge = i           #Initializing itself as Root Bridge
        self.Status = ["DP"]*26       #Initializing all its ports as Designated Ports
        self.SendBuffer = [0]*26      #Buffer to store the messages to send
        self.ReceiveBuffer = [0]*26   #Buffer to keep received messages
        self.best_config = [i,0,i]    #Initializing its best configuration message, i.e., it thinks itself as RP
        self.port_best_config = -1    #To store the port number where the best configuration came from. Here, Port number is same as the LAN ID 
        
        for j in range(26):
            if self.LANs[j]:
                self.SendBuffer[j]=[]
        #Initializing Send buffers on the basis of whether a LAN is connected or not
                
        for j in range(26):
            if self.LANs[j]:
                self.ReceiveBuffer[j]=[]
        #Initializing Receive buffers on the basis of whether a LAN is connected or not
                
    def Change_Status(self, j, port_type):  #Function to change the status of a port
        if port_type == "RP":   #Changing all others ports(except NP) to DP before changing status of itself as RP
            for k in range(26):
                if self.Status[k]!="NP":
                    self.Status[k] = "DP"
            self.Status[j] = "RP"
        if port_type == "NP":   #Port changed to NP only if it was a DP.
            if self.Status[j] == "DP":
                self.Status[j] = "NP"
            
                        
    def Check_if_DP(self,j):
        if self.Status[j] == "DP": #To check if a port is DP or not
            return True
        return False
        
    def send(self,t):  #Member function to send configuration messages and print traces if needed
        for j in range(26):
            if self.LANs[j] and self.Check_if_DP(j): #Messages are only sent to Designated Ports
                a=self.best_config[:]
                self.SendBuffer[j]=[a]
                if self.trace_flag=='1' and t==0:
                    print(f'{t}  s  B{self.i+1}  (B{a[0]+1},{a[1]},B{a[2]+1})  |||  Initialization, send on P{a[2]+1}{chr(65+j)}  |||  B{a[0]+1} is root, port to {chr(65+j)} is DP')
                elif self.trace_flag=='1' and t>0:
                    print(f'{t}  s  B{self.i+1}  (B{a[0]+1},{a[1]},B{a[2]+1})  |||  message send on port P{a[2]+1}{chr(65+j)}     |||  B{a[0]+1} is root, port to {chr(65+j)} is DP')


    def receive(self,t):  #Member function to process configuration messages and print traces if needed
        for j in range(len(self.ReceiveBuffer)):
            if self.ReceiveBuffer[j] != 0:
                if len(self.ReceiveBuffer[j])>0:
                    for k in range(len(self.ReceiveBuffer[j])): 
                        Message_to_process_a = self.ReceiveBuffer[j].pop(0)

                        if Message_to_process_a[2]==self.i:  #The Bridge ignores the message sent by itself
                            continue

                        Message_to_process = Message_to_process_a.copy() #Obtaining the message to be processed

                        if self.trace_flag=='1':
                            print(f'{t}  r  B{self.i+1}  (B{Message_to_process[0]+1},{Message_to_process[1]},B{Message_to_process[2]+1})  |||  message reaching port P{self.i+1}{chr(65+j)}    |||  ',end= "") 
                        
                        dist=Message_to_process[1]+1 #Distance of the root bridge from the configuration message to the current bridge

                        if Message_to_process[0]<self.best_config[0]:     #It identifies a root with a smaller ID
                            self.best_config[0]=Message_to_process[0]
                            self.best_config[1]=dist
                            self.best_config[2]=Message_to_process[2]
                            self.Change_Status(j, "RP")
                            self.port_best_config = j

                        elif Message_to_process[0]==self.best_config[0] and dist<self.best_config[1]:     #It identifies a root with an equal ID but with a shorter distance
                            self.best_config[0]=Message_to_process[0]
                            self.best_config[1]=dist
                            self.best_config[2]=Message_to_process[2]
                            self.Change_Status(j, "RP")
                            self.Change_Status(self.port_best_config, "NP")
                            self.port_best_config = j

                        elif Message_to_process[0]==self.best_config[0] and dist==self.best_config[1]+1:   #Tie-breaker for the connected LAN. The LAN chooses to be connected with the DP of bridge with smaller ID
                            if Message_to_process[2]<self.i:
                                self.Change_Status(j, "NP")

                        elif Message_to_process[0]==self.best_config[0] and dist>self.best_config[1]+1:    #The LAN chooses to be connected with the DP of bridge which is closer to Root Bridge
                            self.Change_Status(j, "NP")

                        elif Message_to_process[0]==self.best_config[0] and dist==self.best_config[1] and Message_to_process[2]<self.best_config[2]:    #The root ID and distance are equal, but the sending bridge has a smaller ID
                            self.best_config[0]=Message_to_process[0]
                            self.best_config[1]=dist
                            self.best_config[2]=Message_to_process[2]
                            self.Change_Status(j, "RP")
                            self.Change_Status(self.port_best_config, "NP")
                            self.port_best_config = j

                        elif Message_to_process[0]==self.best_config[0] and dist==self.best_config[1] and Message_to_process[2]>self.best_config[2]:    #The root ID and distance are equal, but the sending bridge has a larger ID
                            self.Change_Status(self.port_best_config, "RP")
                            self.Change_Status(j, "NP")

                        elif Message_to_process[0]==self.best_config[0] and dist==self.best_config[1] and Message_to_process[2]==self.best_config[2]:   #Tie breaker. The Bridge chooses the LAN based on the LAN ID
                            if self.port_best_config > j:
                                self.Change_Status(j, "RP")
                                self.Change_Status(self.port_best_config, "NP")
                                self.port_best_config = j
                            elif self.port_best_config < j:
                                self.Change_Status(self.port_best_config, "RP")
                                self.Change_Status(j, "NP")

                        if self.trace_flag=='1':
                            print(f'B{self.best_config[0]+1} is root, port to {chr(65+j)} is {self.Status[j]}')   

                        DP_flag=0 
                        for k in range(26): #To check if there are any DPs in the bridge
                            if self.LANs[k]:
                                if self.Status[k] == "DP":
                                    DP_flag=DP_flag+1
                        if DP_flag==0:      #If there are no DPs, i.e., only RPs and NPs, all ports are changed to NP
                            not_sent=False      
                            for k in range(26):
                                if self.Status[k] == "RP":
                                    a=chr(65+k)
                                    not_sent=True
                                self.Status[k] = "NP"
                            if self.trace_flag=='1' and not_sent:
                                print(f'Further since no port is DP, P{self.i+1}{a} is also changed to NP. No message will be sent from this Bridge as no port is DP.')
                        
                self.ReceiveBuffer[j].clear()
        self.best_config[2]=self.i     #Configuration message updated to accomodate the bridge ID of the current bridge

    
class ExtendedLAN():
    def __init__(self, Bridges, NumBridges, j,B):
        self.Bridges = Bridges               #Each LAN is aware to which bridge it is connected
        self.NumBridges = NumBridges         #Number of Bridges to which the LAN is connected
        self.j=j                             #ID of each LAN. Values 0,1,2,3...24,25 represents A,B,C,D...Y,Z respectively
        self.B=B                             #Objects of Bridge class
        self.incoming = []                   #Buffer to store incoming message to LAN

    def transmit_packets(self):              #Packets transmitted from connected Bridges to incoming buffer of LAN
        for i in range(int(self.NumBridges)):
            if self.Bridges[i]: 
                a=self.B[i].SendBuffer[self.j].copy()
                self.B[i].SendBuffer[self.j].clear()
                c = self.incoming + a
                self.incoming = c[:]