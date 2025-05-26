import os
import requests
from lxml import etree
import urllib3
import downloader
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings()
load_dotenv()


def get_base_url(major: str) -> str:
    return {
        "ComProg": "https://comprog.nattee.net",
        "CP": "https://grader.nattee.net",
        "CEDT": "https://cedt-grader.nattee.net",
        "ISE": "https://2190101.nattee.net"
    }.get(major, "")


def setup_cookies():
    return {
        "_cafe_grader_session": os.getenv('_cafe_grader_session'),
        "uuid": os.getenv('uuid'),
    }


def create_dir(path: str):
    os.makedirs(path, exist_ok=True)


def clean_name(name: str) -> str:
    return name.strip().replace('&ZeroWidthSpace;', '\u200b')


def download_problem_pdf(name: str, url: str, cookies: dict, problem_dir: str):
    pdf_path = os.path.join(problem_dir, f"{name}.pdf")
    print(f"Downloading PDF for {name}...")
    downloader.download(url, cookies, pdf_path)


def download_attachment(attachment_url: str, cookies: dict, problem_dir: str):
    try:
        actual_filename = downloader.file_download(attachment_url, cookies, problem_dir)
        if actual_filename:
            print(f"✓ Downloaded attachment: {actual_filename}")
    except Exception as e:
        print(f"❌ Failed to download attachment from {attachment_url}: {e}")


def download_testcases(testcase_url: str, base_url: str, cookies: dict, name: str, problem_dir: str):
    try:
        full_url = f"{base_url.rstrip('/')}/{testcase_url.lstrip('/')}"
        resp = requests.get(full_url, cookies=cookies, verify=False)
        testcase_root = etree.HTML(resp.text)
        testcase_divs = testcase_root.xpath('//a[starts-with(@data-bs-target, "#tc")]')

        print(f"Found {len(testcase_divs)} testcase entries for {name}")

        for idx, div in enumerate(testcase_divs, 1):
            testcase_id = div.get('data-bs-target', '').lstrip('#tc')
            if not testcase_id:
                print(f"Skipping testcase {idx}: missing ID")
                continue

            input_url = f"{base_url}/testcases/{testcase_id}/download_input"
            output_url = f"{base_url}/testcases/{testcase_id}/download_sol"

            testcase_dir = os.path.join(problem_dir, "testcases", str(idx))
            create_dir(testcase_dir)

            try:
                input_file = downloader.file_download(input_url, cookies, problem_dir)
                if input_file:
                    os.rename(os.path.join(problem_dir, input_file), os.path.join(testcase_dir, 'input.txt'))

                output_file = downloader.file_download(output_url, cookies, problem_dir)
                if output_file:
                    os.rename(os.path.join(problem_dir, output_file), os.path.join(testcase_dir, 'output.txt'))

                print(f"Downloaded testcase {idx} (ID: {testcase_id})")
            except Exception as e:
                print(f"Error downloading testcase {idx} (ID: {testcase_id}): {e}")

    except Exception as e:
        print(f"Failed to fetch testcase list from {testcase_url}: {e}")

def row_process(base_url, cookies,output_dir,row):
    read_link = row.xpath('.//a[contains(text(), "Read")]')
    problem_name = row.xpath('.//div[@class="text-muted font-monospace"]/text()')
    attachment = row.xpath('.//a[contains(text(), "File")]')
    testcase_element = row.xpath('.//a[contains(text(), "Testcases")]')
    class_label_element = row.xpath('.//span[@class="badge"]')
    class_label = 'undefined'
    if class_label_element:
        class_label = class_label_element[0].text

    if not read_link or not problem_name:
        return

    name = clean_name(problem_name[0])
    url = read_link[0].get('href')
    if not url:
        print(f"Skipping {name}: URL is missing.")
        return

    if not url.startswith(("http://", "https://")):
        url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"

    problem_dir = os.path.join(output_dir, class_label, name)
    create_dir(problem_dir)

    try:
        download_problem_pdf(name, url, cookies, problem_dir)
    except Exception as e:
        print(f"❌ Failed to download PDF for {name}: {e}")

    if attachment:
        attachment_url = attachment[0].get('href')
        if attachment_url and not attachment_url.startswith(("http://", "https://")):
            attachment_url = f"{base_url.rstrip('/')}/{attachment_url.lstrip('/')}"
        download_attachment(attachment_url, cookies, problem_dir)

    if testcase_element:
        testcase_url = testcase_element[0].get('href')
        if testcase_url:
            download_testcases(testcase_url, base_url, cookies, name, problem_dir)

def main():
    cookies = setup_cookies()
    major = os.getenv('major')
    base_url = get_base_url(major)
    output_dir = os.getenv('output_dir') or 'Data Struct & Algorithm'

    if not base_url:
        print("Invalid or missing major.")
        return

    response = requests.get(f"{base_url}/main/list", cookies=cookies, verify=False)
    root = etree.fromstring(response.text, parser=etree.HTMLParser())
    rows = root.xpath('//tr')

    tasks = []
    max_workers = 5

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for row in rows:
            task = executor.submit(row_process, base_url, cookies, output_dir, row)
            tasks.append(task)

        for task in tasks:
            task.result()



if __name__ == '__main__':
    main()
