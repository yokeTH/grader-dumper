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

rows = root.xpath('//tr')
# selected_element = root.xpath('//*[contains(text(), "Read")]')
# selected_element_name = root.xpath(
#     '//td/div[@class="text-muted font-monospace"]')

for row in rows:
    read_link = row.xpath('.//a[contains(text(), "Read")]')
    problem_name = row.xpath('.//div[@class="text-muted font-monospace"]/text()')
    
    if not read_link or not problem_name:
        continue
    
    base_url = "https://grader.nattee.net"  # for CPs
    url = read_link[0].get('href')
    name = problem_name[0].strip().replace('&ZeroWidthSpace;', '\u200b')
    
    if not url:
        print(f"Skipping {name}: URL is missing.")
        continue

    if not url.startswith(("http://", "https://")):
        url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"

    # save_path = f'{cedt'_'.join(name.split('_')[:2])}/{name}.pdf'
    save_path = f'{output_dir}/{name}.pdf'

    if not os.path.exists('/'.join(save_path.split('/')[:-1])):
        os.makedirs('/'.join(save_path.split('/')[:-1]))

    try:
        downloader.download(url, cookies, save_path)
    except Exception as e:
        print(f"Failed to download {name} from {url}: {e}")