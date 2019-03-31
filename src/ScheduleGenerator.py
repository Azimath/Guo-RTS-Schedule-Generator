#A module to generate plausible random schedules with basic utilization check
#Also tries to limit hyperperiod

from Items import Job, Task
from ExtraMath import gcd, lcm
import random

#Take a list of tasks and return a list of the same tasks with the execution costs scaled by some factor
#fixedCost is any cost like preemption that is always the same
#Restrict to integer time for now
def scaleTaskCosts(taskSet, costScaleFactor, fixedCost=0):
    return [Task(t.phase, t.period, int(t.executionCost*costScaleFactor), t.relativeDeadline, t.extraCost) for t in taskSet]

#Create a list of n tasks which has a utilization less than 1 and integer periods/costs
def createRandomTasks(nTasks, LCMEffort=40, extraCost=0, maxExecutionCost=100, utilizationScale=1):
    tasks = []
    
    #Create first task
    
    taskCost = random.randrange(10, maxExecutionCost)
    taskPeriod = random.randrange(utilizationScale*(taskCost+1)+extraCost, 100*(utilizationScale*(taskCost+1)+extraCost), 2)
    tasks.append(Task(0, taskPeriod, taskCost, taskPeriod, extraCost)) #0 phase, implicit deadline
    totalUtilization = tasks[-1].preemptUtilization()

    currentHyperPeriod = taskPeriod

    while len(tasks) < nTasks:
        
        taskCost = random.randrange(10, 10000)
        #Try to pick a new period that keeps the hyperperiod to a minimum
        taskPeriod = min([p for p in [random.randrange(utilizationScale*(taskCost+1)+extraCost, 100*(utilizationScale*(taskCost+1)+extraCost), 2) for _ in range(LCMEffort)]], key = lambda p: lcm(p, currentHyperPeriod))
        currentHyperPeriod = lcm(taskPeriod, currentHyperPeriod)
        tasks.append(Task(0, taskPeriod, taskCost, taskPeriod, extraCost))

        totalUtilization +=  tasks[-1].preemptUtilization()

        shortenAttempts = 0
        while(totalUtilization > 1) and shortenAttempts < LCMEffort*10: #Make other tasks shorter to make sure the new task has at least 1 time to execute
            shortenAttempts += 1 #If we can't shorten tasks enough, stop trying
            shorten = random.randrange(0, len(tasks))
            if tasks[shorten].executionCost > 20:
                totalUtilization -= tasks[shorten].preemptUtilization()
                tasks[shorten].executionCost -= 20
                totalUtilization += tasks[shorten].preemptUtilization()

    return tasks

if __name__ == "__main__": #Run the task creation a bunch of times and see if it works
    for x in range(1000):
        tasks=createRandomTasks(5)
        l = 1
        for t in tasks:
            l = lcm(l, t.period)

        print(l)