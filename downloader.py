import os
import requests
import re

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
    else:
        print(f"Failed to download the PDF file. Status code: {
              response.status_code}")

def file_download(url, cookies, save_dir):
    response = requests.get(url, cookies=cookies, verify=False)

    if response.status_code == 200:
        filename = ''
        if 'Content-Disposition' in response.headers:
            content_disposition = response.headers['Content-Disposition']

            filename_match = re.search(r"filename\*=UTF-8''(.+?)($|;)", content_disposition)
            if filename_match:
                filename = filename_match.group(1)
            else:
                filename_match = re.search(r'filename="?([^";]+)', content_disposition)
                if filename_match:
                    filename = filename_match.group(1)

        if not filename:
            filename = os.path.basename(url)

        filename = filename.strip('"').strip("'")
        filename = requests.utils.unquote(filename)

        save_path = os.path.join(save_dir, filename)

        with open(save_path, 'wb') as file:
            file.write(response.content)

        return filename
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return None

if __name__ == '__main__':

    cookies = {
        "_cafe_grader_session": os.getenv('_cafe_grader_session'),
        "uuid": os.getenv('uuid'),
    }

    pdf_url = "https://cedt-grader.nattee.net/problems/1297/get_statement/03_Loop_14.pdf"

    download(pdf_url, cookies, 'test.pdf')
