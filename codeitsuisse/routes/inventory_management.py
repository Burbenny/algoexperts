import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

# edit this function to include the operations
def minDistance(word1, word2,cache ={}):
    if not word1 and not word2:
        return [0,""]
    if not word1 : # return the leftover length of the item word as insert operations
        res=["+"+c for c in word2]
        return [len(word2),"".join(res)]
    if not word2:
        res=[]
        for c in word1:
            res.append("-")
            res.append(c)
        return [len(word1),"".join(res)] # return the leftover length of the search word as delete operations
    if word1[0].lower()==word2[0].lower(): # if the char is the same, no operation
        return [minDistance(word1[1:],word2[1:])[0],word1[0]+minDistance(word1[1:],word2[1:])[1]]
    if (word1,word2) not in cache:
        inserted = [1+ minDistance(word1,word2[1:])[0], "+"+word2[0]+minDistance(word1,word2[1:])[1]] #samsung+a ,samsunga
        deleted  = [1+ minDistance(word1[1:],word2)[0],"-"+word1[0]+minDistance(word1[1:],word2)[1]] # -amsung,msng
        replaced = [1+minDistance(word1[1:],word2[1:])[0],word2[0]+minDistance(word1[1:],word2[1:])[1]] #umsung,amsung
        cache[(word1,word2)]= min(inserted,deleted,replaced,key=lambda x:x[0]) # try all possible combinations, caching all substrings as well
        # build the op string as well
    return cache[(word1,word2)]

@app.route('/inventory-management', methods=['POST'])
def evaluate_inventory_management():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result=[]
    for testcase in data:
        search = testcase.get("searchItemName")
        items = testcase.get('items')
        res=[]
        for item in items:
            res.append(minDistance(search,item))

        res.sort(key=lambda x:(x[0],x[1]))
        res=res[:10]
        res=[record[1] for record in res]
        
        result.append({"searchItemName":search,"searchResult":res})
    logging.info("My result :{}".format(result))
    return json.dumps(result);

# if __name__ == "__main__":
#     print(evaluate_inventory_management([{"searchItemName":"Samsung Aircon","items":["Smsng Auon","Amsungh Aircon","Samsunga Airon"]}])) # 5,2,2