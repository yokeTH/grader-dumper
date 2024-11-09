# grader-dumper
dump all pdf from natee's grader

## Setup and Run

1. **Clone or Download the Project**: Clone this repository or download the files to your local machine.

2. **Make the Setup Script Executable**: 
   Open a terminal in the project directory and run the following command to grant execute permissions to the setup script:
   ```bash
   chmod +x setup.sh
   ```
3. **Run the Setup Script**:
   Execute the setup script to create a virtual environment, install dependencies, set up the `.env` file, and start the program:
   ```bash
   ./script.sh
   ```
4. **Enter Cookie Information**
   copy cookies from the actual site while logging in
   During setup, you’ll be prompted to provide the following information:
   - `_cafe_grader_session`: Your session cookie
   - `uuid`: Your unique user identifier

   Enter these values when prompted. The script will store them in the `.env` file.

## Notes

- The cookies provided to this program are only valid for a short period of time. If you want to use the program again later, run script.sh and enter new cookies.
