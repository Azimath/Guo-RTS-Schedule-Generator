#Module to do more robust schedule check
import math, ExtraMath

def measureUtilization(taskSet):
    u = 0
    for t in taskSet:
        u +=  t.utilization()
    return u

def findHyperperiod(taskSet):
    lcm = 1
    for t in taskSet:
        lcm = ExtraMath.lcm(t.period, lcm)

    return lcm

#Takes a list of Task()s and preemption enabled then returns a true or false for schedulability
#Only supports EDF or NP-EDF
def checkSchedule(tasks, preemption):
    u = measureUtilization(tasks)
    if u > 1:
        return False
    elif preemption: #Preemptive EDF can schedule anything with U<1
        return True

    #Check NP-EDF using Jeffay et al 1991

    tasks.sort(key=lambda x: x.period)
    #Check demand, last task should always have the more demand so just check that
    for L in range(1, tasks[-1].period):
        demand = tasks[-1].executionCost
        for t in tasks[:-1]:
            demand += math.floor((L-1)/t.period)*t.executionCost
        
        if demand > L:
            return False

    #NP-EDF check didn't show any problems
    return True
