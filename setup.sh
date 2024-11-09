#!/bin/bash

# Create a virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install required packages
pip3 install -r requirements.txt

# Create a .env file with user input for cookies
echo "Creating .env file..."
echo "_cafe_grader_session=" > .env
echo "uuid=" >> .env

# Prompt user for _cafe_grader_session
read -p "Enter _cafe_grader_session: " cafe_grader_session
echo "_cafe_grader_session=$cafe_grader_session" > .env

# Prompt user for uuid
read -p "Enter uuid: " uuid
echo "uuid=$uuid" >> .env

# Run the main Python script
python3 main.py
