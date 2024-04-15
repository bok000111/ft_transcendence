#!/bin/bash

# Set python venvironment
python3 -m venv ./venv
source ./venv/bin/activate && pip3 install --upgrade pip 

# Install requirements
pip3 install -r requirements.txt

echo run 'source ./venv/bin/activate' to activate the virtual environment
echo run 'deactivate' to deactivate the virtual environment
echo run 'pip freeze > requirements.txt' to update the requirements.txt file
echo run 'python3 -m venv --clear ./venv' to clear the virtual environment
echo run 'python manage.py makemigrations' to make migrations
echo run 'python manage.py migrate' to apply migrations
echo run 'python manage.py runserver' to start the server
