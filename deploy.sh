#!/bin/sh


# create virtualenv and run requirements
#pushd .

# If old virtual env exists, replace it
if [[ -d "virtpy" ]]; then
  rm -rf virtpy
fi

#if [[ ! -d "virtpy" ]]; then
virtualenv virtpy
#fi

if [[ -f "db.sqlite3" ]]; then
  rm -f tmp.db db.sqlite3
fi

# Activate virtualenv
. virtpy/bin/activate

# Install requirements
pip install -r requirements.txt

# Delete migrations
if [[ -d "chat/migrations" ]]; then
  rm -rf chat/migrations
fi

python manage.py makemigrations chat

# Sync DB
python manage.py migrate

# Load DB
python manage.py load_data

deactivate

# To Run Django on localhost:8000
# . virtpy/bin/activate
# redis_server
# python manage.py runserver

# Navigate to http://localhost:8000/