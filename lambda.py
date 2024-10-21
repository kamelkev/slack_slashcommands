import json, urllib3, re
from urllib import parse

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    r = http.request('GET', "https://raw.githubusercontent.com/kamelkev/slack_slashcommands/main/general.json")
    
    if r.status == 200:
        params = dict(parse.parse_qsl(event['body']))
        username = params['user_name']
        command = params['text']
        
        response_text = r.data.decode('utf-8')
        response_text = re.sub('{username}', username, response_text)
        response_text = re.sub('{command}', command, response_text)

        slashcommands = json.loads(response_text)
        
        print(slashcommands.keys())
        
        if command in slashcommands.keys():
    	    blocks = slashcommands[command]
        else:
    	    blocks = slashcommands['_']
          
        return {"statusCode": 200, "body": json.dumps(blocks) }
    else:
        return {"statusCode": 400 }
