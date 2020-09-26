import logging
import json

from flask import request, jsonify;
from functools import lru_cache

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/social_distancing', methods=['POST'])
def evaluate_soc_dist():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests");
    res={}
    cache={}

    def get_ways(seats,people,spaces,num):
        if people==0:
            return 1
        if people==1 and seats>0:
            return seats
        if people>0 and seats<=0:
            return 0
        for i in range(seats):
            if (people-1*spaces)>seats-i:
                break
            # when exceeds the seats just return 1 for each seat the passenger can sit down on
            seats_left=seats-(i+spaces+1)
            if (seats_left,people-1,spaces) not in cache:
                cache[(seats_left,people-1,spaces)]=get_ways(seats_left,people-1,spaces,0)
            num+= cache[(seats_left,people-1,spaces)]
        return num

    for k in tests:
        seats = tests[k].get("seats")
        people = tests[k].get("people")
        spaces = tests[k].get("spaces")
        num=0
        if people>0 and seats>0:
            num=get_ways(seats,people,spaces,num)
        res[k]=num

    result = {"answers": res }
    logging.info("My result :{}".format(result))
    return json.dumps(result);



