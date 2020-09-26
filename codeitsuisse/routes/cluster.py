import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/cluster', methods=['POST'])
def evaluate_cluster():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    grid=data

    cache={}
    def dfs(r,c,infected):
        cache[(r,c)]=True
        # check vertically
        # print(r,c,grid[r][c])
        if r+1<len(grid):
            if grid[r+1][c]=="1" and (r+1,c) not in cache:
                infected=True
                infected = dfs(r+1,c,infected)
            if grid[r+1][c]=="0" and (r+1,c) not in cache:
                infected = dfs(r+1,c,infected)
        if r-1>=0:
            if grid[r-1][c]=="1" and (r-1,c) not in cache:
                infected=True
                infected = dfs(r-1,c,infected)
            if grid[r-1][c]=="0" and (r-1,c) not in cache:
                infected = dfs(r-1,c,infected)
        if c+1<len(grid[0]):
            if grid[r][c+1]=="1" and (r,c+1) not in cache:
                infected=True
                infected = dfs(r,c+1,infected)
            if grid[r][c+1]=="0" and (r,c+1) not in cache:
                infected = dfs(r,c+1,infected)
        if c-1>=0:
            if grid[r][c-1]=="1" and (r,c-1) not in cache:
                infected=True
                infected = dfs(r,c-1,infected)
            if grid[r][c-1]=="0" and (r,c-1) not in cache:
                infected = dfs(r,c-1,infected)
        # diagonal up
        if c+1 <len(grid[0]) and r+1<len(grid):
            if grid[r+1][c+1]=="1" and (r+1,c+1) not in cache:
                infected=True
                infected = dfs(r+1,c+1,infected)
            if grid[r+1][c+1]=="0" and (r+1,c+1) not in cache:
                infected = dfs(r+1,c+1,infected)
        # down left
        if c-1>=0 and r-1>=0:
            if grid[r-1][c-1]=="1" and (r-1,c-1) not in cache:
                infected=True
                infected = dfs(r-1,c-1,infected)
            if grid[r-1][c-1]=="0" and (r-1,c-1) not in cache:
                infected = dfs(r-1,c-1,infected)
        #up right
        if c-1>=0 and r+1<len(grid):
            if grid[r+1][c-1]=="1" and (r+1,c-1) not in cache:
                infected=True
                infected = dfs(r+1,c-1,infected)
            if grid[r+1][c-1]=="0" and (r+1,c-1) not in cache:
                infected = dfs(r+1,c-1,infected)
        # up left
        if c+1<len(grid[0]) and r-1>=0:
            if grid[r-1][c+1]=="1" and (r-1,c+1) not in cache:
                infected=True
                infected = dfs(r-1,c+1,infected)
            if grid[r-1][c+1]=="0" and (r-1,c+1) not in cache:
                infected = dfs(r-1,c+1,infected)
        return infected

        
    num=0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c]=="1":
                if (r,c) not in cache:
                    infected=True
                    dfs(r,c,infected)
                    num+=1
            elif grid[r][c]=="0":
                if (r,c) not in cache:
                    infected=False
                    infected=dfs(r,c,infected)
                    if infected:
                        num+=1
                

    result={"answer":num}
    logging.info("My result :{}".format(result))
    return json.dumps(result);


# if __name__ == '__main__':
#     print(evaluate_cluster([["1", "0", "*", "*"],["0", "1", "0", "0"],["*", "0", "1", "0"]]))
    

