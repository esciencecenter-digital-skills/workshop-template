### Run this script inside the files/ folder to download all screenshots
### and other images that were dumped in the collaborative document.
### Be sure to specify the names of the collaborative documents
### as well as the URL of the collaborative document server at the bottom.

import re
import requests
import os

def create_screenshot_dir():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

def download_png(url, response):
    filename = url.split('/')[-1]
    filename = f"screenshots/{filename}"
    with open(filename, 'wb') as image_file:
        image_file.write(response.content)

def replace_content(fname, markdown_content, markdown_url):
    pattern = rf'({re.escape(markdown_url)})/'
    replacement = r'screenshots/'
    replaced_content = re.sub(pattern, replacement, markdown_content)

    with open(fname, 'w') as file:
        file.write(replaced_content)

def extract_screenshots(fname, markdown_url):
    create_screenshot_dir()

    with open(fname, 'r') as file:
        markdown_content = file.read()

    pattern = rf'!\[\]\(({re.escape(markdown_url)}/[^)]+\.png)\)'
    matches = re.findall(pattern, markdown_content)

    for url in matches:
        response = requests.get(url)
        if response.status_code == 200:
            download_png(url, response)

    replace_content(fname, markdown_content, markdown_url)

if __name__ == "__main__":
    col1 = "collaborative_document_day1.md"
    col2 = "collaborative_document_day2.md"
    col3 = "collaborative_document_day3.md"
    col4 = "collaborative_document_day4.md"

    # do not include the final / in the URLs below
    markdown_url = "https://codimd.carpentries.org/uploads"
    #markdown_url = "https://hackmd.io/_uploads"

    extract_screenshots(col1, markdown_url)
    extract_screenshots(col2, markdown_url)
    extract_screenshots(col3, markdown_url)
    extract_screenshots(col4, markdown_url)

