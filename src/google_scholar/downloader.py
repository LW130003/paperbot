import requests
import os
import numpy as np
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

def check_file_size_in_mb(pdf_link: str):
    head = requests.head(pdf_link)
    mb_to_b = 1024 * 1024
    return int(np.ceil(int(head.headers['content-length']) / mb_to_b))

def is_file_big(pdf_link:str):
    file_size = check_file_size_in_mb(pdf_link)
    if file_size > 10:
        return True
    else:
        return False
    
def save_file_small(pdf_link: str, save_path: str):
    response = requests.get(pdf_link, headers=headers)
    with open(save_path, 'wb') as f:
        f.write(response.content)
        
def save_file_big(pdf_link: str, save_path: str):
    response = requests.get(url, headers=headers)
    chunk_size = 10 * 1024 * 1024
    with open(save_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size):
            f.write(chunk)
    
class PDFDownloader:
    
    def __init__(self, save_dir: str):
        self.save_dir = save_dir
    
    def download(self, pdf_link: str, filename: str):
        save_path = os.path.join(self.save_dir, filename)
        if is_file_big(pdf_link):
            save_file_big(pdf_link, save_path)
        else:
            save_file_small(pdf_link, save_path)

class PaperDownloader:

    def __init__(self, save_dir: str):
        self.save_dir = save_dir
        self.downloader = PDFDownloader(self.save_dir)

    def download(self, paper):
        pdf_link = paper.pdf_link
        filename = paper.get_file_name()
        self.downloader.download(pdf_link, filename)
        