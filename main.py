from lxml import etree
import downloader
import os

from dotenv import load_dotenv
load_dotenv()

cookies = {
    "_cafe_grader_session": os.getenv('_cafe_grader_session'),
    "uuid": os.getenv('uuid'),
}

output_dir = os.getenv('output_dir')

if not output_dir :
    output_dir='Data Struct & Algorithm'

with open('web.html') as f:
    html = f.read()
    root = etree.fromstring(html, parser=etree.HTMLParser())

selected_element = root.xpath('//*[contains(text(), "Read")]')
selected_element_name = root.xpath(
    '//*[@id="main_table"]/tbody/tr/td[2]/strong')

for l, v in zip(selected_element, selected_element_name):
    url = l.get('href')
    name = v.text.strip()

    # save_path = f'{cedt'_'.join(name.split('_')[:2])}/{name}.pdf'
    save_path = f'{output_dir}/{name}.pdf'

    if not os.path.exists('/'.join(save_path.split('/')[:-1])):
        os.makedirs('/'.join(save_path.split('/')[:-1]))

    downloader.download(url, cookies, save_path)
