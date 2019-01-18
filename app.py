from flask import Flask, request, abort
import json
import logging
import subprocess

logging.basicConfig(level="INFO")
application = Flask(__name__)


@application.route('/push', methods=['POST'])
def push_event():
    data = request.get_json()

    # Headers
    event = request.headers.get('X-Gitlab-Event')
    token = request.headers.get('X-Gitlab-Token')

    # Data
    branch = data["ref"].split('/')[2]
    repo_name = data['repository']["name"]
    project_id = data['project']['id']

    with open('repo_settings.json') as f:
        file_data = json.load(f)

    if file_data['token'] != token or event not in file_data['events']:
        logging.warning('invalid token or forbidden event')
        return abort(500)

    if file_data['repo_name'] != repo_name:
        logging.warning('repositories do not match, check "repo_name" in file')
        return abort(500)

    if file_data['project_id'] != project_id:
        logging.warning('invalid project_id')
        return abort(500)

    if file_data['branch'] != branch:
        logging.warning('invalid branch')
        return abort(500)

    logging.info("OK")

    process = subprocess.call(file_data['path'])
    for line in process.stdout:
        print(line.decode().strip())

    return 'OK', 200
#
