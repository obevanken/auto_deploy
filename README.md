# auto_deploy
  Deploy for GitLab

# Application

Create **repo_settings.json** file in project root :

 ```
 {
   "project_id": 1111111,
   "repo_name": "deploy_test",
   "token": "tokent_token_123",
   "events": [
     "Push Hook",
     "Merge Hook"
   ],
   "branch": "master",
   "path": "path/to/project/auto_deploy/commands.sh"
 }
```
install requirements: ```pip install -r requirements.txt```
