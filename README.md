project name = fastapi blog

# to run with docker

- docker-compose build --no-cache web
- docker-compose up

# to run simple 

- python -m venv venv
- venv/bin/activate
- python -m pip install -r ./app/requirements.txt
- python.exe ./app/main.py  


# endpoints
http://localhost:8000/docs#

# endpoints public 
- http://localhost:8000/api/blogs/public
- http://localhost:8000/api/blogs/public?status=publish
- http://localhost:8000/api/blogs/public?status=draft


scheduler is set at 1 minute

# example credentials 
- username = admin 
- email = admin@admin.com
- password = admin

# other
- auth = jwt 
- routes =  auth ,blog
- database = sqlite3
