from enum import Enum
#Identifier for what scheduling methd is being used
class Methods(Enum):
    FCFS = "First Come First Serve"
    SJF = "Shortest Job First"
    SRT = "Shortest Remaining Time"
    PRIORITY = "Priority"
    RNDRBN = "Round-Robin"
#Scheduler takes a process and sets its value based on the scheduling algorith
#Then it lets the magic of the min-heap take over
class Scheduler:
    #Init will have the scheduling method set
    def __init__(self, _Method):
        self.Method = None
        self.CurrentProcess = None
        self.Quantum = None
        self.Fixed = False
        self.TimeSlice = 0
        self.Time = None
        if _Method == "f":
            self.Method = Methods.FCFS
        elif _Method == "sj":
            self.Method = Methods.SJF
        elif _Method == "sr":
            self.Method = Methods.SRT
        elif _Method == "p":
            self.Method = Methods.PRIORITY
        elif _Method == "r":
            self.Method = Methods.RNDRBN
            #Gets valid input for the time quantum if round-robin
            while True:
                try:
                    self.Quantum = int(input("Enter time quantum for round-robin scheduling:"))
                except ValueError:
                    print("That was not a valid integer")
                else:
                    if self.Quantum <= 0:
                        print("That was not a positive integer greater than zero")
                    else:
                        break
            self.Fixed = True if input("Is the quantum a fixed period? (y/n)") == 'y' else False
    #Schedules a procees based on the algorithm
    #May need to know time and current process depending
    def Schedule(self, Queue, _Process, _CurrentProcess, _Time):
        self.CurrentProcess = _CurrentProcess
        self.Time = _Time
        if self.Method == Methods.FCFS:
            return self.FirstComeFirstServe(Queue, _Process)
        elif self.Method == Methods.SJF:
            return self.ShortestJobFirst(Queue, _Process)
        elif self.Method == Methods.SRT:
            return self.ShortestRemainingTime(Queue, _Process)
        elif self.Method == Methods.PRIORITY:
            return self.Priority(Queue, _Process)
        elif self.Method == Methods.RNDRBN:
            return self.RoundRobin(Queue, _Process)
    #For FCFS, the process value is not changed as it is initially set to arrival time
    def FirstComeFirstServe(self, Queue, _Process):
        Queue.add(_Process)
        return False
    #For SJF, the processes value is it's burst time
    def ShortestJobFirst(self, Queue, _Process):
        _Process.value = _Process.BurstTime
        Queue.add(_Process)
        return False
    #Initially SRT starts with having the process value also be the burst time as its inital time remaining == it's burst time
    #When it is re-scheduled, the time remaining is less
    def ShortestRemainingTime(self, Queue, _Process):
        _Process.value = _Process.TimeRemaining
        Queue.add(_Process)
        #If the current process has a greated value than the new one, have the consumer preempt
        if self.CurrentProcess is not None and self.CurrentProcess.TimeRemaining > _Process.TimeRemaining:
            return True
        return False
    #Based on priority attribute
    def Priority(self, Queue, _Process):
        _Process.value = _Process.Priority
        Queue.add(_Process)
        #Similarlly preempt if new procees has a smaller priority than the current process
        if self.CurrentProcess is not None and self.CurrentProcess.Priority > _Process.Priority:
            return True
        return False
    #RR bases the value on the current time
    #When a procees is reschduled, its vlaue is set to the current time so it mus have the max value, putting in in the back of the queue
    def RoundRobin(self, Queue, _Process):
        _Process.value = self.Time
        Queue.add(_Process)
        return False
    #Updates the current time slice and will set preempt flag to true if it has reached 0
    def UpdateTimeSlice(self):
        if self.Quantum is not None and self.TimeSlice > 0:
            self.TimeSlice -= 1
            if self.TimeSlice == 0:
                return True
        return False
    #Sets time slice to quantum
    def CheckTimeSlice(self):
        if not self.Fixed or self.TimeSlice == 0:
            self.TimeSlice = self.Quantum
            return True
        return False