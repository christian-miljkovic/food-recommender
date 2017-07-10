#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4)) #this is where the post from API.ai sends us the json

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    
    r = make_response(jsonify(res))
    r.headers['Content-Type'] = 'application/json'
    
    return r


def processRequest(req):
    if req.get("result").get("action") != "get.restaurant":
        return {}

    data = []
    param = req.get("result").get("parameters")
    data.append(param.get("food-type"),param.get("neighborhood"))

    res = makeWebhookResult(data) #this is an array of the json file
    return res



def makeWebhookResult(data):
    
    food = data[0]
    neighborhood = data[1]

    rec = {'Soho':{'pizza':'Prince Street Pizza','Italian':'Osteria Morini','Mexican':'La Esquina','Japense':'Ato'},
       'Greenwich':{'pizza':'Joe\'s Pizza','Italian':'','Mexican':'','Japense':''}}

    speech = "Check out " + str(rec[neighborhood][food])



    return {
        "speech": speech,
        "displayText": speech,
        "data": data,
        "contextOut": req['results']['contexts'],
        "source": "food-recommender"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
