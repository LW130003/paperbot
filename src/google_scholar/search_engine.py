class SearchEngine:
    number_of_results_per_page = 10    
    def __init__(self, query: str, min_date=None):
        self.query = query
        self.min_date = min_date
        
    @property
    def url(self):
        url = r"https://scholar.google.com/scholar?hl=en&q="+self.query+"&as_vis=1&as_sdt=1,5&start=[START_PAGE]"
        if self.min_date!=None:
            url += "&as_ylo="+["MIN_DATE"] #str(min_date)        
        return url
    
    def get_url(self, idx: int):
        url = self.url
        url = url.replace(
            '[START_PAGE]', 
            str(self.number_of_results_per_page * (idx-1)))
        return url