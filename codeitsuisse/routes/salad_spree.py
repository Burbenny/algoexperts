import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluateSaladSpree():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input");
    # result = inputValue * inputValue

    n = data.get("number_of_salads")
    streetMap = data.get("salad_prices_street_map")

    res = float('inf')

    for street in streetMap:
        for streetIdx in range(len(street)- n +1):
            neighbourSum = 0
            updateRes = True
            for k in range(streetIdx, streetIdx + n ):

                if street[k] == "X":
                    updateRes = False
                    break
                neighbourSum += int(street[k])
            if updateRes and neighbourSum < res:
                res = neighbourSum

    if res == float('inf'):
        res = 0

    resDict = {"result": res}

    # for street in streetMap:
    #     streetIdx = 0
    #     # 0 -2 out of 5
    #     while streetIdx <= (len(street)-n):
    #
    #
    #
    #         #Check if any value in the n-window == "X"
    #         moveToNextIdx = False
    #         for checkX in reversed(range(n)):
    #             toCheck = streetIdx + checkX
    #             if toCheck > len(street)-1:
    #                 continue
    #             elif street[toCheck] == "X":
    #                 streetIdx += checkX+1
    #                 moveToNextIdx = True
    #                 break
    #
    #         if streetIdx + n-1 > len(street)-1 or moveToNextIdx:
    #             break
    #
    #         neighbourSum = 0
    #         print("street", street)
    #         for k in range(streetIdx, streetIdx + n ):
    #             print("im here")
    #             neighbourSum += int(street[k])
    #
    #         if neighbourSum < res:
    #             res = neighbourSum
    #
    #         streetIdx += 1
    #
    #
    # if res == float('inf'):
    #     res = 0
    #
    # resDict = {"result": res}

    logging.info("My result :{}".format(resDict))
    return jsonify(resDict);



