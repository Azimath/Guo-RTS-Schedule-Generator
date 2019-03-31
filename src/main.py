from ScheduleGenerator import createRandomTasks, scaleTaskCosts
from ScheduleValidator import checkSchedule, measureUtilization

def findAverageBreakdown(preemption, preemptCost):
    if not preemption:
        preemptCost = 0 #If we can't preempt there isn't a cost

    breakdownUtilizations = []
    for i in range(10):
        taskSet = createRandomTasks(5, extraCost = preemptCost)
        while not checkSchedule(taskSet, preemption):
            taskSet = createRandomTasks(5, extraCost = preemptCost)

        smallCostScale = 1
        largeCostScale = 2

        #Find some breakdown scale above the actual
        while checkSchedule(scaleTaskCosts(taskSet, largeCostScale, preemptCost), preemption):
            largeCostScale *= 2

        #Iterate a few times to find w (binary search between w>1 and w<2^x)
        #Iterating means we can find w for any scheduler we can check schedulability for (currently just EDF and NP-EDF)
        for _ in range(30):
            if checkSchedule(scaleTaskCosts(taskSet, (smallCostScale + largeCostScale)/2, preemptCost), preemption):
                smallCostScale = (smallCostScale + largeCostScale)/2
            else:
                largeCostScale = (smallCostScale + largeCostScale)/2

        breakdownUtilizations.append(measureUtilization(scaleTaskCosts(taskSet, smallCostScale, preemptCost)))
        print(i)

    return sum(breakdownUtilizations)/len(breakdownUtilizations)

if __name__ == "__main__":
    print(findAverageBreakdown(False, 60))