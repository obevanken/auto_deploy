from flask import Flask, request, abort
import os
import json
import logging


logging.basicConfig(level="INFO")
app = Flask(__name__)

@app.route('/push', methods=['POST'])
def push_event():
    data = request.get_json()
    branch = data["ref"].split('/')[2]
    repo_name = data['repository']["name"]
    with open('labhook.json') as f:
        file_data = json.load(f)
    
    if file_data['repo_name'] != repo_name:
        logging.warning('repositories do not match, check "repo_name" in file')
        return abort(500)

    if branch == file_data['branch']:
        path = file_data['path']
        os.chdir(path)
        if not file_data['commands']: 
            logging.warning("Commands is empty") 
            return abort(500)
        [os.system(command) for command in file_data['commands']]
    else:
        logging.warning("Not this branch")
        return abort(500)
    
    logging.info("OK")  
    return 'OK', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337)