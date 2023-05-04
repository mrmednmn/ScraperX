import sys
sys.dont_write_bytecode = True
from scrapers.base import Scraper
from saving_strategies.base import SavingStrategy


class ScraperManager:
    def __init__(self, scraper:Scraper):
        self.scraper = scraper

    def set_strategy(self, saving_strategy:SavingStrategy):
        self.scraper.set_saving_strategy(saving_strategy)

    def set_scraper(self, scraper:Scraper):
        self.scraper = scraper

    def collect(self,curr_keyword=''):
        self.scraper.scrape(curr_keyword)

    def collect_from_list(self, keyword_list,notify):
        for curr_keyword in keyword_list:
            self.collect(curr_keyword)
        notify("Data collection complete!.")
    
    def __del__(self):
        self.scraper.page.quit()