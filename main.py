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
major = os.getenv('major')
base_url = ""
if major == "ComProg":
    base_url = "https://comprog.nattee.net"
elif major == "CP" :
    base_url = "https://grader.nattee.net"
elif major == "CEDT":
    base_url = "https://cedt-grader.nattee.net"
elif major == "ISE":
    base_url = "https://2190101.nattee.net"

if not output_dir :
    output_dir='Data Struct & Algorithm'

with open('web.html') as f:
    html = f.read()
    root = etree.fromstring(html, parser=etree.HTMLParser())

rows = root.xpath('//tr')

for row in rows:
    read_link = row.xpath('.//a[contains(text(), "Read")]')
    problem_name = row.xpath('.//div[@class="text-muted font-monospace"]/text()')
    attachment = row.xpath('.//a[contains(text(), "File")]')
    
    if not read_link or not problem_name:
        continue
    
    url = read_link[0].get('href')
    name = problem_name[0].strip().replace('&ZeroWidthSpace;', '\u200b')
    
    if not url:
        print(f"Skipping {name}: URL is missing.")
        continue

    if not url.startswith(("http://", "https://")):
        url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"
        
    if not attachment:
        save_path = os.path.join(output_dir, f"{name}.pdf")
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        try:
            print(f"Downloading PDF for {name}...")
            downloader.download(url, cookies, save_path)
        except Exception as e:
            print(f"Failed to download PDF {name} from {url}: {e}")
        continue

    problem_dir = os.path.join(output_dir, name)
    if not os.path.exists(problem_dir):
        os.makedirs(problem_dir)

    pdf_path = os.path.join(problem_dir, f"{name}.pdf")
    try:
        print(f"Downloading PDF for {name}...")
        downloader.download(url, cookies, pdf_path)
    except Exception as e:
        print(f"Failed to download PDF {name} from {url}: {e}")

    file_url = attachment[0].get('href')
    if file_url and not file_url.startswith(("http://", "https://")):
        file_url = f"{base_url.rstrip('/')}/{file_url.lstrip('/')}"
    
    try:
        print(f"Downloading attachment for {name}...")
        actual_filename = downloader.file_download(file_url, cookies, problem_dir)
        if actual_filename:
            print(f"Successfully downloaded attachment: {actual_filename}")
    except Exception as e:
        print(f"Failed to download attachment for {name} from {file_url}: {e}")