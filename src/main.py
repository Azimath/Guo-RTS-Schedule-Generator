from ScheduleGenerator import createRandomTasks, scaleTaskCosts
from ScheduleValidator import checkSchedule, measureUtilization

def findAverageBreakdown(preemption, preemptCost, numIterations, workerNumber=0):
    if not preemption:
        preemptCost = 0 #If we can't preempt there isn't a cost

    breakdownUtilizations = []
    for i in range(numIterations):
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

        print("Worker {} is {}/{}".format(workerNumber, i, numIterations))

        breakdownUtilizations.append(measureUtilization(scaleTaskCosts(taskSet, smallCostScale, preemptCost)))

    return sum(breakdownUtilizations)/len(breakdownUtilizations)

if __name__ == "__main__":

    import multiprocessing
    from itertools import product
    #Some magic to make multiprocessing work
    def breakdownUnpack(args):
        return findAverageBreakdown(*args[0], workerNumber=args[1])

    #Use multiprocessing to make workers that each do some trials
    num_workers = 7
    trials_per_worker = 20
    pool = multiprocessing.Pool(num_workers)
    results = pool.map(breakdownUnpack, product([(False, 60, trials_per_worker)]*num_workers, range(num_workers)))

    print(sum(results)/len(results)) #Average together results from all worker processes