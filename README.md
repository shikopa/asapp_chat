# Asapp Chat

Basic realtime chat service

# REQUIREMENTS
* Python 2.7
* PIP
* VirtualEnv
* Redis

# To Launch Application
* Launch Redis Server on port 6379 (default port)
* `redis_server`
* In root folder
* `bash deploy.sh`
* `. virtpy/bin/activate`
* `python manage.py runserver`
* Navigate to: http://localhost:8000/
* Enter an existing username from: chat/management/commands/load_data.py
* Enter any random username.