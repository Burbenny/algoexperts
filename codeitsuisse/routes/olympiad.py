import logging
import json

from flask import request, jsonify;
from functools import lru_cache

from codeitsuisse import app;

logger = logging.getLogger(__name__)

import itertools


@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_olympiad():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    books = data.get("books");
    days_og = data.get("days");
    n_books=len(books)
    # n_days=len(days)
    book_shelf=books
    len_bs=len(book_shelf)
    day_lists=list(itertools.permutations(days_og))
    outputs=[]
    cache={}

    def knapsack(books,time):
        if time==0:
            return [0,books]
        overflow=True
        book_arr=[]
        for i in range(len(books)):
            if time-books[i]>=0:
                overflow=False
                if (tuple(books[:i]+books[i+1:]),time-books[i]) not in cache:
                    cache[(tuple(books[:i]+books[i+1:]),time-books[i])]=knapsack(books[:i]+books[i+1:],time-books[i])
                book_arr.append(cache[(tuple(books[:i]+books[i+1:]),time-books[i])])
        if overflow:
            return [time,books]
        
        return min(book_arr,key=lambda x:x[0])

    for days in day_lists:
        res=0
        for time in days:
            _,book_shelf=knapsack(book_shelf,time)
            res+=len_bs-len(book_shelf)
            len_bs=len(book_shelf)
        outputs.append(res)
    


    result={"optimalNumberOfBooks": max(outputs)}
    logging.info("My result :{}".format(result))
    return json.dumps(result);
