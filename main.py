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
    '//td/div[@class="text-muted font-monospace"]')

for l, v in zip(selected_element, selected_element_name):
    base_url = "https://grader.nattee.net"  # for CPs
    url = l.get('href')
    
    if not url:
        print(f"Skipping {v.text.strip()}: URL is missing.")
        continue

    if not url.startswith(("http://", "https://")):
        url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"
        
    name = v.text.strip().replace('&ZeroWidthSpace;', '\u200b')

    # save_path = f'{cedt'_'.join(name.split('_')[:2])}/{name}.pdf'
    save_path = f'{output_dir}/{name}.pdf'

    if not os.path.exists('/'.join(save_path.split('/')[:-1])):
        os.makedirs('/'.join(save_path.split('/')[:-1]))

    try:
        downloader.download(url, cookies, save_path)
    except Exception as e:
        print(f"Failed to download {name} from {url}: {e}")