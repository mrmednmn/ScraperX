import sys
sys.dont_write_bytecode = True
from gui.base import Gui
from scrapers.google_map import GoogleMapScraper
from scrapers.maroof import MaroofScraper
from scraper_options.maroof import MaroofOptions
from scraper_options.maroof import MaroofOptions
from saving_strategies.csv.strategy import CsvSavingStrategy
from saving_strategies.excel.strategy import ExcelSavingStrategy
from saving_strategies.xml.strategy import XmlSavingStrategy
from managers.scraper_manager import ScraperManager
from jlib.chrome_driver import Chrome 
from system_health.network_status import NetworkStatusChecker

class ScraperFactory:
    def __init__(self,folder_name, file_name,keyword_list,target_platform, save_type, gui:Gui):
        self.folder_name=folder_name
        self.file_name=file_name
        self.keyword_list=keyword_list
        self.target_platform=target_platform
        self.save_type=save_type
        self.gui=gui
        self.maroof_options=MaroofOptions()
        self.GOOGLE_MAP_HEADINGS=["Facebook","Instagram","LinkedIn","Twitter","address", "description", "houres", "merchant_description","phone", "title","votes","website"]
        self.MAROOF_HEADINGS=["إجمالي التقييمات","إنستقرام", "الاسم التجاري", "التقييمات","بريد إلكتروني", "بيانات العنوان", "تصنيف العمل", "تليجرام", "تويتر", "خدمة عملاء", "رقم السجل التجاري", "رقم معروف", "فيسبوك", "موقع ويب", "نبذه عن العمل", "نوع العمل الرئيسي", "هاتف", "واتس اب"]
       
    def set_gui(self,gui:Gui):
        self.gui=gui

    def set_folder_name(self, folder_name):
        self.folder_name=folder_name

    def set_file_name(self,file_name):
        self.file_name=file_name

    def set_keyword_list(self,keyword_list):
        self.keyword_list=keyword_list

    def set_target_platform(self,target_platform):
        self.target_platform=target_platform

    def set_save_type(self,save_type):
        self.save_type=save_type

    #set maroof options
    def set_maroof_options(self,check_box,main_work,second_work,country,city):
        self.maroof_options = MaroofOptions(check_box,main_work,second_work,country,city)


    def get_strategy(self,headings):
        if "csv" in self.save_type:
            saving_strategy=CsvSavingStrategy(self.folder_name, self.file_name, logger=self.gui.log)
            saving_strategy.init_csv(headings)
        elif "xml" in self.save_type:
            saving_strategy=XmlSavingStrategy(self.folder_name, self.file_name, logger=self.gui.log)
            saving_strategy.init_xml_file(headings)
        else:
            saving_strategy=ExcelSavingStrategy(self.folder_name, self.file_name,logger=self.gui.log)
            saving_strategy.init_excel(headings)
        return saving_strategy

    def run_google_map_scraper(self,chome_version,is_hidden):
        try:
            saving_strategy=self.get_strategy(self.GOOGLE_MAP_HEADINGS)
            scraper = GoogleMapScraper(Chrome(chome_version, hidden=is_hidden),saving_strategy)
            scraper_manager = ScraperManager(scraper)
            scraper_manager.collect_from_list(self.keyword_list,self.gui.log)
        except:
            raise Exception("google map scraper internal error")

    def run_maroof_scraper(self,chome_version,is_hidden):
        try:
            saving_strategy=self.get_strategy(self.MAROOF_HEADINGS)
            scraper = MaroofScraper(Chrome(chome_version, hidden=is_hidden),saving_strategy, self.maroof_options)
            scraper_manager = ScraperManager(scraper)
            scraper_manager.collect_from_list(self.keyword_list,self.gui.log)
        except:
            raise Exception("maroof scraper internal error.")

    def build(self, chome_version, is_hidden):
        internet_checker = NetworkStatusChecker()
        while not internet_checker.can_connect():
            self.gui.log("Internet Connection not available..")

        if self.target_platform=="maroof":
            self.run_maroof_scraper(chome_version,is_hidden)    
        else:
            self.run_google_map_scraper(chome_version,is_hidden)
