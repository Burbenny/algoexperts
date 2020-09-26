import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def geometry_eval():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    shapeCoordinates = data.get("shapeCoordinates")
    lineCoordinates = data.get("lineCoordinates")
    result = geometry_solve(shapeCoordinates,lineCoordinates)
    logging.info("My result :{}".format(result))
    return jsonify(result)

#shapCoordinates is a array of dictionary, each dict is a pair of coordinates, all linked to form a shape
#lineCoordinates is a array of dictoinary, each dict is a pair of coordinates, each pair is a line 
#returns the array of intersection
def geometry_solve(shapeCoordinates, lineCoordinates):
    # Naive approach is to check all sides and lines
        #given a n sided polygon, there will be total of n sides,
        #for each side, check if each lines interesects with side by calculating the line equation and solving the equations

    sol = []
    ## find the line equation
    a,m,c = helper_line_eqn(lineCoordinates[0]['x'],lineCoordinates[0]['y'],lineCoordinates[1]['x'],lineCoordinates[1]['y'])

    
    # if n ==1 
    if (len(shapeCoordinates) == 1):
        if (a*shapeCoordinates[0]['y'] == m*shapeCoordinates[0]['x']+c):
            # the point is on the line, 
            sol.append({"x":shapeCoordinates[0]['x'],"y":shapeCoordinates[0]['y']})
            return sol
    # if n == 2
    if (len(shapeCoordinates) == 2):
        x1=shapeCoordinates[1]['x']
        y1= shapeCoordinates[1]['y']

        x2,y2 = shapeCoordinates[0]['x'], shapeCoordinates[0]['y']

        #eqn of the line between the two coordinates
        a2,m2,c2 =helper_line_eqn(x1,y1,x2,y2)
        temp = helper_get_intersect(a,m,c,a2,m2,c2,x1,y1,x2,y2)
        if bool(temp):
            sol.append(temp)
        return sol
    # if n >=3
    for i in range(len(shapeCoordinates)):
        if len(sol) == 2:
            return sol
        x1=shapeCoordinates[i]['x']
        y1= shapeCoordinates[i]['y']
        if i == len(shapeCoordinates) -1 :
            x2,y2 = shapeCoordinates[0]['x'], shapeCoordinates[0]['y']
        else :
            x2,y2 = shapeCoordinates[i+1]['x'], shapeCoordinates[i+1]['y']
        #eqn of the line between the two coordinates

        a2,m2,c2 =helper_line_eqn(x1,y1,x2,y2)
 
 
        temp = helper_get_intersect(a,m,c,a2,m2,c2,x1,y1,x2,y2)

        if bool(temp):
            sol.append(temp)

    
    return sol


# find s the ay= mx+C eqn and return m and c 
def helper_line_eqn(x1,y1,x2,y2):
    if x2-x1 == 0 :
        c = -x1
        a=0
        m = 1
    elif y2-y1 == 0:
        m=0
        c = y1
        a=1
    else :
        m = (y2 - y1) / (x2 - x1)
        c = y1 - (m*x1)
        a=1
    return a,m,c

#assuming no pure x or pure y lines
def helper_get_intersect(a1,m1,c1,a2,m2,c2,x1,y1,x2,y2):
    intercept = {}
    #either both is pure X or pure Y
    if (a1 == 0 and a2 == 0) or (m1 == 0 and m2 == 0):
        return {}
    # if a==0 solve for x straight 
    if (a1==0 or a2 == 0):
        if (a1 == 0):
            x = -c1/m1
            y = (m2*x +c2)/a2
        elif (a2 == 0):
            x = -c2/m2
            y= (m1*x +c1)/a1
    # if m== 0 solve for y straight 
    elif (m1==0 or m2 == 0):
        if (m1 == 0):
            y = c1/a1
            x = (a2 * y - c2 )/m2
        elif (m2 == 0):
            y = c2/a2
            x = (a1 * y - c1 )/m1
    else :    
        x = (a1*c2-c1*a2)/(a2*m1-a1*m2)
        y= (m1*x + c1)/a1

    if (x2 <= x <= x1) or (x1 <= x <= x2) :
        intercept['x']= round(x,2)
    else:
        return {}

    if (y2 <= y <= y1) or (y1 <= y <= y2) :
        intercept['y']= round(y,2)
    else:
        return {}
    return intercept