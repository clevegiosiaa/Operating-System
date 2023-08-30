from threading import Thread, Lock
from time import sleep
import random
import numpy as np

lock = Lock()
nProcessesRan = 0

# GET SAFE SEQUENCE
def getSafeSeq(safeSeq):
    tempRes = np.array(resources)
    
    finished = []
    for i in range(nProcesses):
        finished.append(False)
    finished = np.array(finished)
    
    nFinished = 0
    while (nFinished < nProcesses):
        safe = False
        for i in range(nProcesses):
            if finished[i] == False:
                possible = True
                for j in range(nResources):
                    if need[i][j] > tempRes[j]:
                        possible = False
                        break
                if possible:
                    for j in range(nResources):
                        tempRes[j] += allocated[i][j]
                    safeSeq.append(i)
                    finished[i] = True
                    nFinished += 1
                    safe = True

        if safe == False:
            for k in range(nProcesses):
                safeSeq.append(-1)
            return False, safeSeq # no safe sequence found

    return True, safeSeq # safe sequence found

# PROCESS CODE
def processCode(p, lock):
    global nProcessesRan

    # ACQUIRE RESOURCE
    lock.acquire()

    # PROCESS
    print("--> Process", p+1)
    allocated_list = []
    for i in range(nResources):
        allocated_list.append(allocated[p][i])
    print("\tAllocated : ", *allocated_list)

    needed_list = []
    for i in range(nResources):
        needed_list.append(need[p][i])
    print("\tNeeded    : ", *needed_list)

    available_list = []
    for i in range(nResources):
        available_list.append(resources[i],)
    print("\tAvailable : ", *available_list)
    sleep(1)
    print("\tResource Allocated!")
    sleep(1)
    print("\tProcess Code Running...")
    sleep(random.randint(1, 5))
    print("\tProcess Code Completed...")
    sleep(1)
    print("\tProcess Releasing Resource...")
    sleep(1)
    print("\tResource Released!")

    for i in range(nResources):
        resources[i] += allocated[p][i]

    now_available_list = []
    for i in range(nResources):
        now_available_list.append(resources[i])
    print("\tNow Available : ", *now_available_list)
    print("\n")

    sleep(1)

    nProcessesRan += 1
    lock.release()


if __name__ == '__main__':
    nProcesses = int(input("\nNumber of processes? "))
    nResources = int(input("\nNumber of resources? "))

    resources = [int(i) for i in input("\nCurrently Available resources (R1 R2 ...)? ").split()]

    # ALLOCATED
    print()
    allocated = []
    for i in range(nProcesses):
        allocated.append([int(j) for j in input(f"\nResource allocated to process {i+1} (R1 R2 ...)? ").split()])
    allocated = np.array(allocated)
    print()

    # MAXIMUM REQUIRED RESOURCES
    maxRequired = []
    for i in range(nProcesses):
        maxRequired.append([int(j) for j in input(f"\nMaximum resource required by process {i+1} (R1 R2 ...)? ").split()])
    maxRequired = np.array(maxRequired)
    print()

    # CALCULATE NEED MATRIX
    need = maxRequired - allocated

    # CHECK SAFE STATE
    safeSeq = [] 
    getSafeSeq, safeSeq = getSafeSeq(safeSeq)

    # NOT SAFE
    if getSafeSeq == False:
        print("\nUnsafe State! The processes leads the system to a unsafe state.\n")
        exit()
    
    # SAFE
    safe_seq_list = []
    for i in range(nProcesses):
        safe_seq_list.append(safeSeq[i]+1)
    print("\nSafe Sequence Found : ", *safe_seq_list)
        
    print("\nExecuting Processes...\n\n")
    sleep(1)

    processNumber = np.array(nProcesses)

    # CREATE & RUN THREADS
    for p in range(processNumber):
        thread = Thread(target=processCode, args = (p, lock))
        thread.start()
    
    # JOIN THREAD
    thread.join()

    print("All Processes Finished\n")