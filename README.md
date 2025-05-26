# grader-dumper
Dump all PDFs and attachments from Nattee's grader

## Setup and Run

1. **Clone or Download the Project**: Clone this repository or download the files to your local machine.

2. **Download HTML from the Grader Website**:
   - Log in to the grader website.
   - Download the HTML page and save it as `web.html`.
   - Place the file into this directory, replacing any existing `web.html`.

3. **Make the Setup Script Executable**:
   Open a terminal in the project directory and run the following command to grant execute permissions to the setup script:
   ```bash
   chmod +x setup.sh
   ```

4. **Run the Setup Script**:
   Execute the setup script to create a virtual environment, install dependencies, set up the `.env` file, and start the program:
   ```bash
   ./script.sh
   ```

5. **Enter Prompted Information**:
   - Enter your major or course
     - `1` 2110101 Computer Programming (First year) `comprog.nattee.net`
     - `2` CP: Data Structures or Algorithm `grader.nattee.net`
     - `3` CEDT `cedt-grader.nattee.net`
     - `4` ISE `2190101.nattee.net`
   - During setup, you’ll be prompted to provide the following cookies:
     - Copy the cookies from the grader website while logged in.
        - `_cafe_grader_session`: Your session cookie
        - `uuid`: Your unique user identifier

   ![Cookies Example](cookies.png)

   - Enter your preferred name for the output directory. (Press `enter` for default name, `Data Structures & Algorithm`)

   Enter these values when prompted. The script will store them in the `.env` file.

7. **Output Location**:
   - All files will be downloaded to the folder with the name you entered after the script is executed. If you left that field blank, the files will be saved in the default folder, `Data Struct & Algorithm`.

## Output file structure
   - Save PDFs directly in output directory if no attachment
   - Create subdirectory with PDF and attachment if present

   ```
   Data Structures & Algorithm
   ├── d57_​q0_​histogram.pdf      # no attachment
   ├── d57_​q0_​remove_​even.pdf    # no attachment
   ├── d57_​q1_​dense              # with attachment
   │   ├── d57_​q1_​dense.pdf      # pdf
   │   └── dense_project.zip     # attachment
   ...
   ```

## Notes

- The cookies provided to this program are only valid for a short period of time. If you want to use the program again later, try running `main.py` with `python3 main.py`. If it doesn’t work, update the cookies in `.env` and try execute `source env/bin/activate` or simply run `./script.sh` again and enter new cookies.

- Alternatively use [UV](https://docs.astral.sh/uv/) (recommended)

## Windows Users

If you’re using Windows, you’ll need to figure out how to run this program on your own :)
Hint: read `setup.sh`
