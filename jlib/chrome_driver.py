import sys
sys.dont_write_bytecode = True
import undetected_chromedriver as un_chrome
import random
import time
from os import system

class Chrome:
    def __init__(self,chrome_version,incogneto=True,hidden=False,profile=""):
        self.VERSION=chrome_version
        self.INCOGNETO=incogneto
        self.CURR_URL=None
        self.BLANK="about:blank"
        self.BROWSER=None
        self.IS_HIDDEN=hidden
        self.init(profile)

    def log(self,msg):
        print(msg,end='\n')

    #clear the screen
    def clear_terminal(self):
        system("cls" if sys.platform == "win32" else "clear")

    def close(self):
        if self.BROWSER!= None:
            try:
                self.BROWSER.close()
            except Exception as ex:
                self.log(str(ex))

    def quit(self):
        if self.BROWSER != None:
            try:
                self.BROWSER.quit()
                self.BROWSER=None
            except Exception as ex:
                self.log(str(ex))

    #generate chrome options
    def get_options(self,profile=""):
        options = un_chrome.ChromeOptions()
        
        if profile!="":
            options.add_argument(r'--user-data-dir='+profile)

        if self.INCOGNETO:
            options.add_argument("--incognito")

        options.headless=self.IS_HIDDEN

        options.add_argument("--start-maximized")
        options.add_argument("--disable-popup-blocking")
        #disable images
        options.add_argument('--blink-settings=imagesEnabled=false')
        return options

    #quit the browser ad start again
    def init(self,profile=""):
        self.quit()
        options=self.get_options(profile)
        un_chrome.TARGET_VERSION =self.VERSION
        try:
            self.BROWSER = un_chrome.Chrome(use_subprocess=True, options=options)
        except Exception as ex:
            self.log("Internal Error: "+ str(ex))


    def sleep_for(self,begin,end):
        time.sleep(round(random.uniform(begin, end),2))


    def die_with_code(self,code):
        self.quit()
        sys.exit(code)

    def get(self):
        return self.BROWSER

    def refresh(self):
        try:
            self.BROWSER.execute_script('location.reload();')
            return self.BROWSER
        except:
            pass

    def go_to_url(self,url: str):
        try:
            self.BROWSER.execute_script(f'window.location.href = "{url}";')
            return self.BROWSER
        except:
            self.log("Internal error while moving to:"+url)

    def go_back(self):
        try:
            self.BROWSER.back() 
        except:
            self.log("Internal error while moving back.")