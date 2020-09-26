import logging
import json

from flask import request, jsonify;
from functools import lru_cache

from codeitsuisse import app;

logger = logging.getLogger(__name__)

# @lru_cache()
# def knapsack(books,time,cache={}):
#     books=list(books)
#     if time==0:
#         return (time,tuple(books))

#     book_arr=[]
#     overflow=True
#     for i in range(len(books)):
#         if time-books[i]>=0:
#             overflow=False
#             book_arr.append(knapsack(tuple(books[:i]+books[i:]),time-books[i]))
#     if overflow:
#         return (time,tuple(books))
#     # if all too big return books, get minum remainder
#     return min(book_arr,key=lambda x:x[0])

def knapsack(books,time):
    if time==0:
        return [0,books]
    overflow=True
    book_arr=[]
    for i in range(len(books)):
        if time-books[i]>=0:
            overflow=False
            book_arr.append(knapsack(books[:i]+books[i+1:],time-books[i]))
    if overflow:
        return [time,books]
    
    return min(book_arr,key=lambda x:x[0])


@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_olympiad():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    books = data.get("books");
    days = data.get("days");
    n_books=len(books)
    # n_days=len(days)
    res=0
    book_shelf=books
    len_bs=len(book_shelf)
    for time in days:
        _,book_shelf=knapsack(book_shelf,time)
        print(book_shelf)
        res+=len_bs-len(book_shelf)
        len_bs=len(book_shelf)


    result={"optimalNumberOfBooks": res}
    logging.info("My result :{}".format(result))
    return json.dumps(result);
