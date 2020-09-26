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
        streetIdx = 0
        while streetIdx <= (len(street)-n):



            # Check if any value in the n-window == "X"
            for checkX in reversed(range(n)):
                toCheck = streetIdx + checkX
                if toCheck > len(street)-1:
                    continue
                elif street[toCheck] == "X":
                    streetIdx += checkX+1
                    break

            if streetIdx + n > len(street)-1:
                break

            neighbourSum = 0
            for k in range(streetIdx, streetIdx + n ):
                print("im here")
                neighbourSum += int(street[k])

            print('neighbour sum is ', neighbourSum)
            if neighbourSum < res:
                res = neighbourSum

            streetIdx += 1


    if res == float('inf'):
        res = 0

    resDict = {"result": res}

    logging.info("My result :{}".format(resDict))
    return jsonify(resDict);



