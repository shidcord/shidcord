from flask import Flask
from flask_cors import CORS
from flask import request
from flask import Response
import json, random, datetime, time
from snowflake import get_snowflake

supports_credentials=True
  
def newMessage(msg):
    global data
    message =    {
        "id":str(get_snowflake()),
        "type":0,
        "content":msg,
        "channel_id":"845928619343478787",
        "author":{
            "id":"687918465788542999",
            "username":"LegitJeff",
            "avatar":"d95ec18eaf680fd235bd4d4d789528f3",
            "discriminator":"0972",
            "public_flags":576
        },
        "attachments":[
         
        ],
        "embeds":[
         
        ],
        "mentions":[
         
        ],
        "mention_roles":[
         
        ],
        "pinned":False,
        "mention_everyone":False,
        "tts":False,
        "timestamp":str(datetime.datetime.now().isoformat()),
        "edited_timestamp":None,
        "flags":0,
        "components":[
         
        ]
    }
    print(message)
    data.append(message)
    print(data)
    with open('disc_msgs.txt', 'w') as outfile:
        json.dump(data, outfile)
    

with open('disc_msgs.txt') as json_file:
    data = json.load(json_file)

app = Flask(__name__)
CORS(app)

@app.route('/<path:dummy>',methods = ['GET','POST'])
def fallback(dummy=None,methods = ['GET','POST']):
    #print(request.headers)
    #print(request.method)
    if request.method == 'POST':
        msg = json.loads(request.data)["content"]
        print("MSG SENT:", msg)
        newMessage(msg)
        response = app.response_class(
            status=200
        )
        return response
    else:
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response