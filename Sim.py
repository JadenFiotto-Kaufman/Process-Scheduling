from Producer import Producer
from Process import Process
from MinHeap import MinHeap
import os

#Boolean - While true, do the simulation
simulate = True
os.system('cls')
print("Welcome!")
while simulate:
    #Valid Process number input
    while True:
        try:
            ProcessAmount = int(input("Enter the number of processes to simulate:"))
        except ValueError:
            print("That was not a valid integer")
        else:
            if ProcessAmount <= 0:
                print("That was not a positive integer greater than zero")
            else:
                break

    os.system('cls')
    Methods = {"f","sj","sr","p","r"}
    #Valid scheduling algorithm input
    while True:
        print("[f]irst come first serve,[sj]ob first,[sr]emaining time,[p]riority,[r]ound robin")
        Method = input("Choose your scheduling method by entering the characters in brackets for the algorithm:")
        if Method not in Methods:
            input("That was not a valid method, press enter to select another.")
            os.system('cls')
        else:
            break
    #New processes are stored in a min-heap, having the arrival time as the compared value
    Processes = MinHeap()
    #Gather parameters for each process
    for i in range(0, ProcessAmount):
        os.system('cls')
        #Valid PID input
        #PID value is mutually exclusive
        while True:
            try:
                PID = int(input("Enter the PID identifier for this process:"))
            except ValueError:
                print("That was not a valid integer")
            else:
                if PID < 0:
                    print("That was not a positive integer")
                else:
                    if len([s for s in Processes.Heap if s.PID == PID]) == 0:
                        break
                    else:
                        print("A process with that PID has already been added")
        #Valid arrival time input
        while True:
            try:
                AT = int(input("Enter the Arrival Time:"))
            except ValueError:
                print("That was not a valid integer")
            else:
                if AT < 0:
                    print("That was not a positive integer")
                else:
                    break
        #Valid burst time input
        while True:
            try:
                BT = int(input("Enter the Burst Time:"))
            except ValueError:
                print("That was not a valid integer")
            else:
                if BT <= 0:
                    print("That was not a positive integer greater than zero")
                else:
                    break
        P = None
        #Valid priority input
        #Priority values are mutually exclusive
        while Method == 'p':
            try:
                P = int(input("Enter the Priority:"))
            except ValueError:
                print("That was not a valid integer")
            else:
                if P < 0:
                    print("That was not a positive integer")
                else:
                    if len([s for s in Processes.Heap if s.Priority == P]) == 0:
                        break
                    else:
                        print("A process with that priority has already been added")
        #Create the process with the parameters
        _Process = Process(AT,BT,PID,P)
        #Set process value to it's arrival to be organized by the min-heap
        _Process.value = _Process.ArrivalTime
        Processes.add(_Process)

    os.system('cls')
    #Sets a sleep command to sleep for a second every iteration
    realTime = True if input("Simulate in real time? (y/n):") == "y" else False
    os.system('cls')
    #Create the producer with the processes
    _Producer = Producer(Processes)
    #Start passing process to the consumer based on the scheduling method
    _Producer.Begin(Method, realTime)
    #Output of stats
    _Producer.CPUstats()
    #Can repeatedly run the simulation
    simulate = True if input("Would you like to simulate another set of processes? (y/n):") == "y" else False
    os.system('cls')