#!/usr/bin/env python

import urllib
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
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "get.restaurant":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    neighborhood = parameters.get("neighborhood")
    food = parameters.get("food-type")



    recommendation = {'SoHo':{'pizza':'Prince Street Pizza','Italian':'Osteria Morini','Mexican':'La Esquina','Japenese':'Ato','Indian':'Hampton Chutney','Thai':'Lan Larb Soho'}, 
    'Midtown':{'pizza':'','Italian':'','Mexican':'','Japenese':'','Indian':'','Thai':''}, 
    'Lower East Side':{'pizza':'','Italian':'','Mexican':'','Japenese':'','Indian':'','Thai':''}, 
    'Tribeca':{'pizza':'','Italian':'','Mexican':'','Japenese':'','Indian':'','Thai':''},
     'Chelsea':{'pizza':'','Italian':'','Mexican':'','Japenese':'','Indian':'','Thai':''}, 
     'East Village':{'pizza':'','Italian':'','Mexican':'','Japenese':'','Indian':'','Thai':''}, 
     'West Village':{'pizza':'','Italian':'','Mexican':'','Japenese':'','Indian':'','Thai':''}, 
     'Greenwich Village':{'pizza':'','Italian':'','Mexican':'','Japenese':'','Indian':'','Thai':''}, 
     'Gramercy':{'pizza':'','Italian':'','Mexican':'','Japenese':'','Indian':'','Thai':''}, 
     'West Village':{'pizza':'','Italian':'','Mexican':'','Japenese':'','Indian':'','Thai':''}}

    speech = "Check out" + str(recommendation[neighborhood[food]])

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
