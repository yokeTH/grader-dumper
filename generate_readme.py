import os
import requests
from lxml import etree
from dotenv import load_dotenv

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


def clean_name(name: str) -> str:
    return name.strip().replace('&ZeroWidthSpace;', '\u200b')


def extract_problem_info(row, base_url, filter_class: str):
    read_link = row.xpath('.//a[contains(text(), "Read")]')
    problem_name = row.xpath('.//td[2]/strong')
    problem_id = row.xpath('.//div[@class="text-muted font-monospace"]/text()')
    attachment = row.xpath('.//a[contains(text(), "File")]')
    testcase_element = row.xpath('.//a[contains(text(), "Testcases")]')
    class_label_element = row.xpath('.//span[@class="badge"]')
    class_label = class_label_element[0].text if class_label_element else '-'

    # if class_label != filter_class:
    #     return None

    if not read_link or not problem_id:
        return None

    id = clean_name(problem_id[0])
    read_url = read_link[0].get('href')
    attachment_url = attachment[0].get('href') if attachment else ''
    testcase_url = testcase_element[0].get('href') if testcase_element else ''

    def full_url(url):
        return f"{base_url.rstrip('/')}/{url.lstrip('/')}" if url and not url.startswith("http") else url

    return {
        "class": class_label,
        "name": clean_name(problem_name[0].text),
        "id": id,
        "pdf_url": full_url(read_url),
        "attachment_url": full_url(attachment_url),
        "testcase_url": full_url(testcase_url)
    }


def generate_readme(problems, output_path='README.md'):
    lines = [
        "# Problem Index\n",
        "| Class | Problem Name | Problem ID | Testcases |",
        "|-------|--------------|------------|-----------|"
    ]

    for prob in problems:
        class_name = f"{prob['class']}"
        problem_name = f"[{prob['name']}](./{prob['id'].replace(' ', '%20')}/{prob['id'].replace(' ', '%20')}.pdf)"
        problem_id = f"{prob['id']}"
        pdf_link = "PDF" if prob['pdf_url'] else "-"
        testcase_link = f"[Testcases](./{prob['id'].replace(' ', '%20')}/testcases)" if prob['testcase_url'] else "-"

        lines.append(f"| {class_name} | {problem_name} | {problem_id} | {testcase_link} |")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"✓ README.md generated at {output_path}")


def main():
    cookies = setup_cookies()
    major = os.getenv('major')
    base_url = get_base_url(major)
    filter_class = "Algo"

    if not base_url:
        print("Invalid or missing major.")
        return
    if not filter_class:
        print("Please set filter_class in your .env or pass it as an argument.")
        return

    response = requests.get(f"{base_url}/main/list", cookies=cookies, verify=False)
    root = etree.fromstring(response.text, parser=etree.HTMLParser())
    rows = root.xpath('//tr')

    problems = []
    for row in rows:
        info = extract_problem_info(row, base_url, filter_class)
        if info:
            problems.append(info)

    generate_readme(problems, 'index.md')


if __name__ == '__main__':
    main()
