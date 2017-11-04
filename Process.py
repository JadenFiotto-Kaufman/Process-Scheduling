#Class abstraction of a process
class Process:
    def __init__(self,_ArrivalTime,_BurstTime,_PID, _Priority):
        self.ArrivalTime = _ArrivalTime
        self.BurstTime = _BurstTime
        self.PID = _PID
        self.Priority = _Priority
        self.TimeRemaining = self.BurstTime
        self.TurnAroundTime = None
        self.WaitTime = 0
        #Value allows the min-heap to work for multiple parameters
        self.value = None
    #Simple calculation of turn around time and wait time for a process
    def Calculate(self, Time):
        self.TurnAroundTime = Time - self.ArrivalTime
        self.WaitTime = Time - self.ArrivalTime - self.BurstTime