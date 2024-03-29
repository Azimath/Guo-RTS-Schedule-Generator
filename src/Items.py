#Module that defines some classes useful in simulating real time systems
import math

class Task:
    def __init__(self, phase, period, executionCost, relativeDeadline, extraCost):
        self.phase = phase
        self.period = period
        self.executionCost = executionCost
        self.relativeDeadline = relativeDeadline
        self.extraCost = extraCost

    def createJobs(self, startTime, endTime): #Return a list of all jobs that release in a certain window
        currentRelease = self.period*math.floor((startTime-self.phase)/self.period) #Determine when the first job releases
        jobsReleased = []

        while currentRelease < endTime:
            jobsReleased.append(Job(currentRelease, currentRelease+self.relativeDeadline, self.executionCost+self.extraCost))
            currentRelease += self.period

        return jobsReleased

    def rawUtilization(self): #Simple global utilization
        return self.executionCost/self.period
    
    def preemptUtilization(self): #Global utilization including preempt cost
        return (self.executionCost+self.extraCost)/self.period

    def timeRequired(self):
        return (self.executionCost+self.extraCost)

    def __repr__(self):
        return "Task({},{},{},{})".format(self.phase, self.period, self.executionCost, self.relativeDeadline)

    def __str__(self):
        return self.__repr__()
        
        

class Job:
    def __init__(self, releaseTime, deadline, executionCost):
        self.releaseTime = releaseTime
        self.deadline = deadline
        self.executionCost = executionCost
        self.timeExecuted = 0

    def canExecute(self, time): #Job can execute any time after release and if it has work to do
        return self.releaseTime < time and not self.isDone()

    def executeForTime(self, time): #Keep track of how much work has been done
        self.timeExecuted += time

    def isDone(self):
        return self.timeExecuted >= self.executionCost

    def isLate(self, time):
        return time > self.deadline and not self.isDone()

    def __repr__(self):
        return "Job(^{}  v{}, {}/{})".format(self.releaseTime, self.deadline, self.timeExecuted, self.executionCost)

    def __str__(self):
        return self.__repr__()