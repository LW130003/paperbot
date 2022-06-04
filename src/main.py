from google_scholar.search_engine import SearchEngine
query = "Machine Learning"
url = SearchEngine(query).get_url(0)
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}
html = requests.get(url, headers=headers)
from google_scholar.html_parser import GoogleScholarHTMLParser
papers = GoogleScholarHTMLParser().parse(html.text)
from google_scholar.downloader import PaperDownloader
save_dir = r"C:\Users\LW\Desktop\TEST"
PaperDownloader(save_dir).download(papers[0])