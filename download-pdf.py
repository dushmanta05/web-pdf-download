import requests
from bs4 import BeautifulSoup
import os
import time
import random
from urllib.parse import urljoin

def download_pdf(url, folder):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': url,
    }

    if not os.path.exists(folder):
        os.makedirs(folder)

    session = requests.Session()

    retries = 3
    while retries > 0:
        try:
            response = session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while accessing the URL: {e}")
            retries -= 1
            if retries == 0:
                print("Max retries reached. Exiting.")
                return
            print(f"Retrying... ({retries} attempts left)")
            time.sleep(random.uniform(1, 3))

    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: href and href.lower().endswith('.pdf'))

    if not pdf_links:
        print("No PDF links found on the page.")
        return

    for link in pdf_links:
        pdf_url = urljoin(url, link.get('href'))
        pdf_name = os.path.basename(pdf_url)
        pdf_path = os.path.join(folder, pdf_name)
        
        print(f"Attempting to download: {pdf_name}")
        
        download_retries = 3
        while download_retries > 0:
            try:
                pdf_response = session.get(pdf_url, headers=headers, timeout=30)
                pdf_response.raise_for_status()
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_response.content)
                print(f"Successfully downloaded: {pdf_name}")
                break
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {pdf_name}: {e}")
                download_retries -= 1
                if download_retries == 0:
                    print(f"Max retries reached for {pdf_name}. Skipping.")
                else:
                    print(f"Retrying download... ({download_retries} attempts left)")
                    time.sleep(random.uniform(1, 3))
        
        time.sleep(random.uniform(2, 5))

# URL of the website containing PDF links
url = "https://example.com/"
# Folder to save the PDFs
download_folder = "downloaded_pdfs"
# Run the function
download_pdf(url, download_folder)