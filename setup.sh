#!/bin/bash

# Create a virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install required packages
pip3 install -r requirements.txt

# Create a .env file with user input for cookies
echo "Creating .env file..."

# Get major
while true; do
    echo
    echo "=== Select your course or major ==="
    echo "1) Com Prog"
    echo "2) CP"
    echo "3) CEDT"
    echo "4) ISE"
    echo "==================================="
    read -p "Enter your choice (1-4): " major_choice
    
    case $major_choice in
        1)
            major="ComProg"
            break
            ;;
        2)
            major="CP"
            break
            ;;
        3)
            major="CEDT"
            break
            ;;
        3)
            major="ISE"
            break
            ;;
        *)
            echo "Invalid input. Please select 1, 2, 3 or 4."
            echo
            ;;
    esac
done

echo "Selected course or major: $major"
echo

# Write to .env file
echo "major=$major" > .env

# Prompt user for _cafe_grader_session
read -p "Enter _cafe_grader_session: " cafe_grader_session
echo "_cafe_grader_session=$cafe_grader_session" >> .env

# Prompt user for uuid
read -p "Enter uuid: " uuid
echo "uuid=$uuid" >> .env

# Promt user for Output Directory
read -p "Enter your preferred output directory name (press Enter for default): " output_dir
echo "output_dir=$output_dir" >> .env

# Run the main Python script
python3 main.py
