from MyThread import Consumer
from Scheduler import Scheduler
from MinHeap import MinHeap
#The producer is given a min-heap of processes and when the min processes' arrival time is the current time, it adds it
#To the queue to be gathered by the consumer
class Producer:
    def __init__(self, _NewProcesses):
        #Keeps track of the current time
        self.Time = 0
        #Keeps track of the idle time
        self.IdleTime = 0
        #Min-heap of all processes currently waiting to have CPU time
        self.Queue = MinHeap()
        #Place to store processes when they complete to view their metrics
        self.FinalProcesses = []
        #Boolean flag to inform the consumer when to finish
        self.ExitFlag = False
        self.NewProcesses = _NewProcesses

    def Begin(self, Method, realTime):
        #Created the scheduler and sets what algortihm to schedule by
        self._Scheduler = Scheduler(Method)
        #Creates the consumer which will increment the global time and "run" the processes
        _Consumer = Consumer(self, realTime)
        #Consumer extends thread whcih is started with the start() function call
        _Consumer.start()
        #Producer looks to add to the queue while processes still exist in the new processes min-heap
        while not self.NewProcesses.isEmpty():
            #If a process has the arrival time of the current time, it gets popped from the holding min-heap, and is added to the shared queue min-heap
            if self.NewProcesses.peek().ArrivalTime == self.Time:
                print("Time:",self.Time,"- Process", self.NewProcesses.peek().PID, "has been added")
                #The new procees is scheduled into the min-heap based on the scheduling method
                #This also can set the preemt flag of the consumer deping on the situation
                _Consumer.PreemptFlag = self._Scheduler.Schedule(self.Queue, self.NewProcesses.pop(), _Consumer.CurrentProcess, self.Time)
        #When the producer has no more processes to give, sets the exit flag as to tell the consumer there are no more processes to be added
        self.ExitFlag = True
        #Thread type call to wait for the consumer thread to finish before continuing
        _Consumer.join()
    #Method to output the data about the processes and the simulation
    def CPUstats(self):
        print("      -----------")
        print("      |CPU stats|")
        print("      -----------")
        print("Algorithm:", self._Scheduler.Method.value)
        if self._Scheduler.Method.name == "RNDRBN":
            print("  Quantum length:", self._Scheduler.Quantum)
            print("  Fixed quantum:", self._Scheduler.Fixed)
        WaitTotal = 0
        TATTotal = 0
        for _Process in self.FinalProcesses:
            print("PID:",_Process.PID)
            print("    Arrival Time:",_Process.ArrivalTime,"-- Burst Time:",_Process.BurstTime)
            print("    Turn Around Time:",_Process.TurnAroundTime,"-- Wait Time:",_Process.WaitTime)
            WaitTotal += _Process.WaitTime
            TATTotal += _Process.TurnAroundTime
        print("Average Turn Around Time:",TATTotal / len(self.FinalProcesses),"-- Average Wait Time:",WaitTotal / len(self.FinalProcesses))
        print("Idle time:", self.IdleTime)
        print("------------------------------")
