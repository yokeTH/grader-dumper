#!/bin/bash

# Create a virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install required packages
pip3 install -r requirements.txt

# Create a .env file with user input for cookies
echo "Creating .env file..."

# Prompt user for _cafe_grader_session
read -p "Enter _cafe_grader_session: " cafe_grader_session
echo "_cafe_grader_session=$cafe_grader_session" > .env

# Prompt user for uuid
read -p "Enter uuid: " uuid
echo "uuid=$uuid" >> .env

# Promt user for Output Directory
read -p "Enter your preferred output directory name (press Enter for default): " output_dir
echo "output_dir=$output_dir" >> .env

# Run the main Python script
python3 main.py
