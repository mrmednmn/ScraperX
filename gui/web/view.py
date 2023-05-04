import sys
sys.dont_write_bytecode = True
from gui.base import Gui
from factories.scraper_factory import ScraperFactory
import eel
import os
import time
import winreg

class WebGui(Gui):
    def __init__(self):
        self.web_folder="web"
        self.main_html="index.html"
        self.web_folder_path=os.path.join(os.getcwd(),"gui",self.web_folder)
        self.start_index=os.path.join(self.web_folder_path,self.main_html)
        self.size=(1024,768)
        self.chrome_version = self.detect_chrome_browser()
        self.is_hidden = False
        self.scrapers=[]
        self.running= 0
        self.finished=0

    def detect_chrome_browser(self):#auto detect chrome version.
        if os.name == 'nt':
            try:
                reg_path = r"SOFTWARE\Google\Chrome\BLBeacon"
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
                value, _ = winreg.QueryValueEx(reg_key, "version")
                major_version = value.split('.')[0]
                return major_version
            except WindowsError:
                reg_path = r"SOFTWARE\Wow6432Node\Google\Chrome\BLBeacon"
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
                value, _ = winreg.QueryValueEx(reg_key, "version")
                major_version = value.split('.')[0]
                if not major_version:
                   return 112
                return major_version
        else:
            return 112


    def get_options(self):
        #img = os.path.join(self.web_folder_path, "img", "bzoogh_logo.png")
        chrome_options ={
        'startup_args': ['--no-sandbox', '--disable-translate'],
        'app_mode': True,
        'port': 0,
        #'icon_path': img
        }
        return chrome_options 
        
    #override
    def log(self, data):
        eel.log(data)

    #override
    def start(self):#Launch the gui.
        eel.init(self.web_folder_path)
        eel.start(self.start_index,chrome_options=self.get_options(),size=self.size)

    def add_scraper(self,folder_name, file_name, keyword_list, target_platform, save_type):
        #self.chrome_version=int(chrome_version)
        try:
            scraper =ScraperFactory(folder_name, file_name, keyword_list, target_platform, save_type,self)
            self.scrapers.append(scraper)
            return True
        except:
            return False

    #set maroof options
    def set_maroof_options(self,check_box,main_work,second_work,country,city):
        if len(self.scrapers)>0:#set options to the current maroof scraper
            self.scrapers[-1].set_maroof_options(check_box,main_work,second_work,country,city)
            return True 
        return False

    def build_all_scrapers(self):
        try:
            scrapers_len=len(self.scrapers)
            if scrapers_len>0:
                for scraper in self.scrapers:
                    self.running=1
                    scraper.build(self.chrome_version, self.is_hidden)
                    self.finished+=1
                    self.running=0  

            self.log(str(scrapers_len) + " Scrapers Finished..")
            time.sleep(2)
            self.scrapers.clear()
            self.log("There is no Scrapers..")
            time.sleep(2)
            eel.navToMain()
        except:
            pass

    def scrapers_size(self):
        return len(self.scrapers)

    def get_running(self):
        return str(self.running)

    def get_finished(self):
        return str(self.finished)


gui = WebGui()

def start_gui():
    gui.start()


@eel.expose
def add_scraper(folder_name, file_name, keyword_list, target_platform, save_type):
    keyword_list = [s.replace("\r", "") for s in keyword_list]
    is_added =  gui.add_scraper(folder_name, file_name, keyword_list, target_platform, save_type)
    return is_added


@eel.expose
def set_maroof_options(check_box,main_work,second_work,country,city):
    options_added = gui.set_maroof_options(check_box,main_work,second_work,country,city)
    return options_added

@eel.expose
def scrapers_size():
    curr_size = gui.scrapers_size()
    return curr_size

@eel.expose
def get_running():
    running =gui.get_running()
    return running
        

@eel.expose
def get_finished():
    finished= gui.get_finished()
    return finished


@eel.expose
def build_all_scrapers():
    gui.build_all_scrapers()


