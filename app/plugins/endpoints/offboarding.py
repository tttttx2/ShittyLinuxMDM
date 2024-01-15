import json
import os
import glob


#todo input sanitization

def read(id=False): # GET
    content = []
    for screen_id in glob.glob('/data/endpoints/*'):
        f = open(screen_id, "r")
        screen_content = f.read()
        f.close()
        screen_content = json.loads(screen_content)
        if (screen_content['onboarded']) == "No":
            continue
        content += [{'id':screen_content['id'], 'onboarded':screen_content['onboarded'], 'offboarding_command':'curl \'http://localhost:8080/plugins/scripts/manage_scripts?offboarding_id='+screen_content['id']+'\' | sudo bash -' } ]
    if content == []:
        return {"error":'No endpoints onboarded, there is nothing to offboard!'}
    return {'table':content, 'readonly':True}
