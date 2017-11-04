import threading
import time
#Consumer extends thread meaning it can run independent of the process that called it
#It shares the data of its calling producer by having the producer passed to it
#This allows the consumer to update the time for it and its parent producer
#It also shared all other variables, mainly the waiting queue
class Consumer(threading.Thread):
    def __init__(self, _Producer, realTime):
        threading.Thread.__init__(self)
        #Variable indicating the current process in the CPU
        self.CurrentProcess = None
        #When this boolean flag is set, the consumer knows to perform a preempt
        self.PreemptFlag = False
        self.Producer = _Producer
        self.timeStep = 1 if realTime else .001
    #Method to called when the thread has start() called on it
    def run(self):
        while True:
                #For real time
                time.sleep(self.timeStep)
                #At the beginnig of each iteration, the consumer has the scheduler update the time slice
                #This only matters for round-robin scheduling
                #If the time slice has expired, it will flip the preempt flag to true
                if self.Producer._Scheduler.UpdateTimeSlice():
                    self.PreemptFlag = True
                #Second operation for the consumer to perform for each iteration
                #For when the CPU is not empty
                if self.CurrentProcess is not None:
                    #Decrease the time remaining of the current process
                    self.CurrentProcess.TimeRemaining -= 1
                    #If the process is complete
                    if self.CurrentProcess.TimeRemaining == 0:
                        print("Time:",self.Producer.Time,"- Process", self.CurrentProcess.PID, "has finished")
                        #Calulate wait time and turn around time
                        self.CurrentProcess.Calculate(self.Producer.Time)
                        self.Producer.FinalProcesses.append(self.CurrentProcess)
                        #Set CPU to be empty
                        self.CurrentProcess = None
                    #Otherwise, if the preempt flag was set
                    #This is an else if because if the current processes ended, you aren't preempting anything
                    elif self.PreemptFlag:
                        print("Time:",self.Producer.Time,"- Process", self.CurrentProcess.PID, "has been preempted")
                        #Schedule the current process back into the queue
                        self.Producer._Scheduler.Schedule(self.Producer.Queue, self.CurrentProcess, self.CurrentProcess, self.Producer.Time)
                        #Set CPU to be empty
                        self.CurrentProcess = None
                #Third step per iteration, if the CPU is now empty
                if self.CurrentProcess is None:
                    #If there are processes waiting in the queue
                    #Also if the time slice is expired (only prevelent for fixed round-robin)
                    #Sets current process to min process in the queue
                    if not self.Producer.Queue.isEmpty() and self.Producer._Scheduler.CheckTimeSlice():
                        self.CurrentProcess = self.Producer.Queue.pop()
                        print("Time:",self.Producer.Time,"- Process", self.CurrentProcess.PID, "has begun")
                    #Otherwise if there are no waiting processes and the producer has set the exit flag, end the consusmer
                    elif self.Producer.Queue.isEmpty() and self.Producer.ExitFlag:
                        break
                    #Finally, if none of that was relevent, the CPU must be idle
                    #This can happen when the wait queue is empty, but there are still new processes yet to be added
                    #Or the time slice for fixed round-robin has not expired
                    else:
                        print("Time:", self.Producer.Time,"- CPU is Idle")
                        self.Producer.IdleTime += 1
                #Flip back the preempt flag
                self.PreemptFlag = False
                #Increment the time
                self.Producer.Time += 1
