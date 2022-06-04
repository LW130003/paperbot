from bs4 import BeautifulSoup
import re


def tag_is_not_book(tag):
    # not book -> is paper
    return True not in [span.text == "[B]" for span in tag.findAll(
        "span", class_="gs_ct2")]

class PaperMetadataTemplate:
    def get(self):
        template = {
            'title': None,
            'link': None,
            'cites': None,
            'pdf_link': None,
            'year': None,
            'authors': None    
        }        
        return template
    
def get_title_and_link(tag):
    for h3 in tag.findAll("h3", class_="gs_rt"):
        found = False
        title, link = None, None    
        for a in h3.findAll("a"):
            if not found:
                title = a.text
                link = a.get('href')
                found = True
            if found:
                break
    return title, link

def get_citation_and_pdf_link(tag):
    cites, pdf_link = None, None
    for a in tag.findAll("a"):
        if "Cited by" in a.text:
            cites = int(a.text[8:])
        if "[PDF]" in a.text:
            pdf_link = a.get('href')
    return cites, pdf_link

def get_authors_and_year(tag):
    authors, year = None, None
    for div in tag.findAll("div", class_="gs_a"):
        try:
            authors, source_and_year, source = div.text.replace('\u00A0', ' ').split(" - ")
            found = True
        except ValueError:
            continue
        
        if not authors.strip().endswith('\u2026'):
            # There is no ellipsis at the end so we know the full list of authors
            authors = authors.replace(', ', ';')
        try:
            year = int(source_and_year[-4:])
            if not (1000 <= year <= 3000):
                year = None
            else:
                year = str(year)
        except ValueError:
            continue

        if found:
            break
    return authors, year

class GoogleScholarPaper:
    
    def __init__(self, meta):
        self.title = meta.get('title')
        self.link = meta.get('link')
        self.cites = meta.get('cites')
        self.pdf_link = meta.get('pdf_link')
        self.year = meta.get('year')
        self.authors = meta.get('authors')
        self.is_downloadable = True if meta.get('pdf_link') is not None else True
    
    def get_file_name(self):
        try:
            # remove all non-word characters (everything except numbers and letters)
            title = re.sub('[^\w\s]', '', self.title)
            # remove all runs of whitespace with '_'
            title = re.sub(r"\s+", "_", title)
            # turn all into lower-case
            title = title.lower()
            return title + ".pdf"
        except:
            return "none.pdf"    

class GoogleScholarHTMLParser:
    
    def parse(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        tag_ls = soup.findAll("div", class_="gs_r gs_or gs_scl")
        paper_tag_ls = [tag for tag in tag_ls if tag_is_not_book(tag)]
        paper_ls = []
        for tag in paper_tag_ls:
            meta = PaperMetadataTemplate().get()
            tag = paper_tag_ls[0]
            meta["title"], meta["link"] = get_title_and_link(tag)
            meta["cites"], meta["pdf_link"] = get_citation_and_pdf_link(tag)
            meta["authors"], meta["year"] = get_authors_and_year(tag)
            paper_ls.append(GoogleScholarPaper(meta))
        return paper_ls