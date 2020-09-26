import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def optimal_hedge_ratio(corr,sd_s,sd_f):
    return corr*(sd_s/sd_f)

def num_fc(opt_hr,portfolio_val,futures_cs):
    return opt_hr*portfolio_val/futures_cs

@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_opt_port():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    inputs = data.get("inputs");
    final=[]
    for portfolio in inputs:
        portfolio_val = portfolio.get("Portfolio").get("Value")
        sd_s = portfolio.get("Portfolio").get("SpotPrcVol")
        idx_futures=portfolio.get("IndexFutures")
        res=[]
        for future in idx_futures:
            name=future.get("Name")
            corr=future.get("CoRelationCoefficient")
            sd_f=future.get("FuturePrcVol")
            futures_price=future.get("IndexFuturePrice")
            notional=future.get("Notional")
            futures_cs=futures_price*notional
            opt_hr=round(optimal_hedge_ratio(corr,sd_s,sd_f),3)
            num_fut_c=round(num_fc(opt_hr,portfolio_val,futures_cs))
            # sort in opt_hr,sd_f and num_fc
            # just try sort without heapify
            res.append([name,opt_hr,sd_f,num_fut_c])
        
        res.sort(key=lambda x:(x[1],x[2],x[3]))
        final.append({"HedgePositionName":res[0][0],"OptimalHedgeRatio":res[0][1], "NumFuturesContract":res[0][3]})
    result={"outputs": final}
    logging.info("My result :{}".format(result))
    return json.dumps(result);