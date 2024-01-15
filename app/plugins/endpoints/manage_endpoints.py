import json
import os
import glob
#todo input sanitization

def create(id): # POST
    os.system("mkdir -p /data/endpoints")
    configpath = "/data/endpoints/{}".format(id)
    if os.path.isfile(configpath) == True:
        return {"error":'Endpoint already exists'}

    else:
        f = open(configpath, "w+")
        content = {"id":id, "ip_address":"-", "hostname":"-", "status":"-", "last_updated":"-", "onboarded":"No"}
        f.write(json.dumps(content))
        f.close()
        return {'ok':'Endpoint created'}

def read(id=False): # GET
    if id == False or id == "": # return all endpoints
        content = []
        for screen_id in glob.glob('/data/endpoints/*'):
            f = open(screen_id, "r")
            screen_content = f.read()
            f.close()
            content += [json.loads(screen_content)]
        return {'table':content}
    else: #return specific screen
        configpath = "/data/endpoints/{}".format(id)
        if os.path.isfile(configpath) == False:
            return {"error":'Endpoint does not exist'}

        else:
            f = open(configpath, "r")
            content = f.read()
            f.close()
            return {'form':json.loads(content)}

def update(id, ip_address, hostname, status, last_updated, onboarded): # PUT
    configpath = "/data/endpoints/{}".format(id)
    if os.path.isfile(configpath) == False:
        return {"error":'Endpoint does not exist'}

    else:
        f = open(configpath, "w+")
        content = {"id":id, "ip_address":ip_address, "hostname":hostname, "status":status, "last_updated":last_updated, "onboarded":onboarded}
        f.write(json.dumps(content))
        f.close()
        return {'ok':'Endpoint config updated'}

def delete(id):
    configpath = "/data/endpoints/{}".format(id)
    if os.path.isfile(configpath) == False:
        return {"error":'Endpoint does not exist'}

    else:
        os.unlink(configpath)
        return {'ok':'Endpoint endpoint deleted'}
