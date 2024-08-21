import os
import requests


def download(url, cookies, save_path):

    # Send a GET request to the URL with cookies
    response = requests.get(url, cookies=cookies)

    # Check if the request was successful
    if response.status_code == 200:
        # Define the output PDF file name
        pdf_file_name = save_path

        # Open a file in binary write mode and write the content
        with open(pdf_file_name, 'wb') as pdf_file:
            pdf_file.write(response.content)

        print(f"PDF downloaded and saved as {pdf_file_name}")
    else:
        print(f"Failed to download the PDF file. Status code: {
              response.status_code}")


if __name__ == '__main__':

    cookies = {
        "_cafe_grader_session": os.getenv('_cafe_grader_session'),
        "uuid": os.getenv('uuid'),
    }

    pdf_url = "https://cedt-grader.nattee.net/problems/1297/get_statement/03_Loop_14.pdf"

    download(pdf_url, cookies, 'test.pdf')
