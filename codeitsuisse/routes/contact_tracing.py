import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def compareStrings(str1, str2):
    # handle the case where one string is longer than the other
    maxlen = len(str2) if len(str1) < len(str2) else len(str1)
    dif = 0
    nonSilentCount = 0
    isNonSilent = False


    # loop through the characters
    for i in range(maxlen):
        # use a slice rather than index in case one string longer than other
        letter1 = str1[i:i + 1]
        letter2 = str2[i:i + 1]
        # create string with differences
        if letter1 != letter2:
            dif += 1
            # Check for start of instruction
            if i % 4 == 0:
                nonSilentCount +=1

    if nonSilentCount >1:
        isNonSilent = True


    return dif, isNonSilent

@app.route('/contact-tracing', methods=['POST'])
def evaluateContactTracing():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input");
    # result = inputValue * inputValue


    infected = data.get("infected")
    origin = data.get("origin")
    clusterList = data.get("cluster")


    nodesList = []
    nodesList.extend(clusterList)
    nodesList.append(origin)

    # print('clusterLIst', clusterList)
    # print('nodeLIst', nodesList)

    allRoutes = []
    queue = []
    queue.append({'node': infected, 'unvisited': nodesList.copy(), 'result':infected.get('name')})

    while queue:
        curr = queue.pop()
        currGenome = curr.get('node').get('genome')
        print('currGenome', currGenome)
        print('currUnvisited', curr.get('unvisited'))

        #for one node, i managed to fins the minTaget, target with lowest distance
        minDif = float('inf')
        minTargets = []
        for target in curr.get('unvisited'):
            targetGenome = target.get('genome')
            dif, isNonSilent = compareStrings(currGenome, targetGenome)

            print('dif', dif)
            if dif == minDif:
                minTargets.append({'target':target,'isNonSilent':isNonSilent})
            elif dif < minDif:
                minDif = dif
                minTargets=[{'target':target,'isNonSilent':isNonSilent}]

        print('minTargets', minTargets)

        endOfTrace = False
        tempQueue = []

        for pair in minTargets:

            minTarget = pair.get('target')
            isNonSilent = pair.get('isNonSilent')

            if minTarget == origin:
                endOfTrace = True

            newUnvisited = curr.get("unvisited").copy()
            newUnvisited.remove(minTarget)

            newResult = curr.get("result")
            if isNonSilent:
                newResult += "*"
            newResult += ' -> '
            newResult += minTarget.get('name')
            newCurr = minTarget

            tempQueue.append({'node': newCurr, 'unvisited': newUnvisited, 'result': newResult})

            # if not endOfTrace:
            #     queue.append({'node':newCurr, 'unvisited':newUnvisited, 'result' : newResult})
        if not endOfTrace:
            queue.extend(tempQueue)
        else:
            allRoutes.append(newResult)

            #if it contains origin, i dont have to add anything to queue
            # take out from unvisitedunvisited
            # update result
            # change 'node' to itself
            # add to queue



        #check every node and compute its distance from current node
        # if ther eare multiple nodes with same distance,add it to queue, and add it to result
        #pop queue and do the same thing again
        # if the current poped node is origin or is a node with saem distance from origin, end the loop



    logging.info("My result :{}".format(allRoutes))
    return jsonify(allRoutes);



