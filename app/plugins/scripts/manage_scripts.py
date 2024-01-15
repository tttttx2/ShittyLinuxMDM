import json
import os
import glob
#todo input sanitization

def create(id): # POST
    os.system("mkdir -p /data/screens")
    configpath = "/data/screens/{}".format(id)
    if os.path.isfile(configpath) == True:
        return {"error":'Script already exists'}

    else:
        f = open(configpath, "w+")
        content = {"id":id, "script":""}
        f.write(json.dumps(content))
        f.close()
        return {'ok':'Script created'}

def read(id=False, onboarding_id=False): # GET
    if onboarding_id!=False:
        return """cat <<'EOF' | tee /opt/mdm.sh
#!/bin/bash

URL=\""""+os.environ["MDM_URL"]+"""\"
ID=\""""+onboarding_id+"""\"

data=$(curl -s "$URL/plugins/scripts/manage_scripts" | jq -c '.table'|jq -c '.[].script')

RESULT=0
while read i; do
    eval $i
    RESULT=$(($RESULT + $?))
done < <(echo $data)

STATUS="ERROR"
if [ "$RESULT" -eq "0" ]; then
   STATUS="OK";
fi

curl -s -X PUT "$URL/plugins/endpoints/manage_endpoints?hostname=$(hostname)&ip_address=$(curl ifconfig.me)&last_updated=$(date +'%FT%T')&onboarded=Yes&status=$STATUS&id=$ID"
EOF

chmod +x /opt/mdm.sh
crontab -l -u root > mycron
echo "*/5 * * * * /opt/mdm.sh" >> mycron
crontab -u root mycron
        """

    if id == False or id == "": # return all screens
        content = []
        for screen_id in glob.glob('/data/screens/*'):
            f = open(screen_id, "r")
            screen_content = f.read()
            f.close()
            content += [json.loads(screen_content)]
        return {'table':content}
    else: #return specific screen
        configpath = "/data/screens/{}".format(id)
        if os.path.isfile(configpath) == False:
            return {"error":'Script does not exist'}

        else:
            f = open(configpath, "r")
            content = f.read()
            f.close()
            return {'form':json.loads(content)}

def update(id, script): # POST
    configpath = "/data/screens/{}".format(id)
    if os.path.isfile(configpath) == False:
        return {"error":'Script does not exist'}

    else:
        f = open(configpath, "w+")
        content = {"id":id, "script":script}
        f.write(json.dumps(content))
        f.close()
        return {'ok':'Script config updated'}

def delete(id):
    configpath = "/data/screens/{}".format(id)
    if os.path.isfile(configpath) == False:
        return {"error":'Script does not exist'}

    else:
        os.unlink(configpath)
        return {'ok':'Script endpoint deleted'}
