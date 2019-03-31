#A module to generate plausible random schedules with basic utilization check
#Also tries to limit hyperperiod

from Items import Job, Task
from ExtraMath import gcd, lcm
import random

#Take a list of tasks and return a list of the same tasks with the execution costs scaled by some factor
#fixedCost is any cost like preemption that is always the same
#Restrict to integer time for now
def scaleTaskCosts(taskSet, costScaleFactor, fixedCost=0):
    return [Task(t.phase, t.period, int(((t.executionCost-fixedCost)*costScaleFactor)+fixedCost), t.relativeDeadline) for t in taskSet]

#Create a list of n tasks which has a utilization less than 1 and integer periods/costs
def createRandomTasks(nTasks, LCMEffort=40, minCost=1):
    tasks = []
    
    #Create first task
    taskPeriod = random.randrange(max(minCost, 10), 10000, 2)
    taskCost = random.randrange(minCost, taskPeriod)
    totalUtilization = taskCost/taskPeriod

    tasks.append(Task(0, taskPeriod, taskCost, taskPeriod)) #0 phase, implicit deadline

    currentHyperPeriod = taskPeriod

    while len(tasks) < nTasks:
        
        #Try to pick a new period that keeps the hyperperiod to a minimum
        taskPeriod = min([p for p in [random.randrange(10, 10000, 2) for _ in range(LCMEffort)]], key = lambda p: lcm(p, currentHyperPeriod))

        while((1-totalUtilization)*taskPeriod<minCost): #Make other tasks shorter to make sure the new task has at least 1 time to execute
            shorten = random.randrange(0, len(tasks))
            totalUtilization -= tasks[shorten].utilization()
            tasks[shorten].executionCost -= 1 #Should be enough to squeeze in a new task but we can try again if we need
            totalUtilization += tasks[shorten].utilization()

        taskCost = random.randrange(minCost, min(int(taskPeriod*(1-totalUtilization))+1,taskPeriod)) #Ensure the task can't make the utilization more than 1

        totalUtilization +=  taskCost/taskPeriod

        tasks.append(Task(0, taskPeriod, taskCost, taskPeriod))

    return tasks

if __name__ == "__main__": #Run the task creation a bunch of times and see if it works
    for x in range(1000):
        tasks=createRandomTasks(5)
        l = 1
        for t in tasks:
            l = lcm(l, t.period)

        print(l)