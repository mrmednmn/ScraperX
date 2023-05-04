#Developer: Mohamed Naamane
#Contact: naamanemohamedtheprogrammer@gmail.com
import sys
sys.dont_write_bytecode = True
from scrapers.base import Scraper
from html_data.google_map import GoogleMapHtml
from saving_strategies.base import SavingStrategy
from jlib.js_functions import get_elements_by_css_selector 
from jlib.js_functions import get_element_by_css_selector 
from jlib.js_functions import click_element_by_css_selector as css_click_in
from jlib.js_functions import is_page_loaded
from jlib.js_functions import get_element_from_element
from jlib.js_functions import get_elements_from_element
from jlib.js_functions import get_url_from_element
from jlib.js_functions import remove_element_by_selector
import time

class GoogleMapScraper(Scraper):
    def __init__(self, page,saving_strategy:SavingStrategy):
        self.page=page
        self.target_elements=GoogleMapHtml().get()
        self.url="https://www.google.com/search?tbs=&tbm=lcl&sxsrf=&q="
        self.NA='N/A'
        self.curr_keyword=self.NA
        self.details={}
        self.saving_strategy=saving_strategy
        self.init_details()
        self.name="Google map scraper"

    def init_details(self):
        self.details["Facebook"]=self.NA
        self.details["Instagram"]=self.NA
        self.details["LinkedIn"]=self.NA
        self.details["Twitter"]=self.NA
        self.details["address"]=self.NA
        self.details["description"]=self.NA
        self.details["houres"]=self.NA
        self.details["merchant_description"]=self.NA
        self.details["phone"]=self.NA
        self.details["title"]=self.NA
        self.details["votes"]=self.NA
        self.details["website"]=self.NA

    def clear_data(self):
        for k in self.details:
            self.details[k]=self.NA

    def set_saving_strategy(self,saving_strategy:SavingStrategy):
        self.saving_strategy=saving_strategy


    def fix_keyword(self,keyword:str):#change spaces to +
        return keyword.replace(' ', '+')
        
    def get_all_map_objects(self):
        while not is_page_loaded(self.page.get()):
            pass
        map_objs_selector=self.target_elements['map_objects_css']
        all_objects= get_elements_by_css_selector(self.page.get(),map_objs_selector)
        max_wait=2
        start_time=time.time()
        while all_objects is None and time.time() - start_time < max_wait:
            self.page.sleep_for(0.01,0.5)
            all_objects= get_elements_by_css_selector(self.page.get(),map_objs_selector)
        return all_objects

    def get_business_card(self):
        business_card_selector=self.target_elements['business_card_css']
        business_card= get_element_by_css_selector(self.page.get(),business_card_selector)
        while business_card is None:
            self.page.sleep_for(0.01,0.5)
            business_card= get_element_by_css_selector(self.page.get(),business_card_selector)
        return business_card

    def get_data_from_business_card(self,business_card,key,target_selector):
        html_elem = get_element_from_element(self.page.get(),business_card,target_selector)
        while html_elem is None:
            self.page.sleep_for(0.01,0.5)
            html_elem = get_element_from_element(self.page.get(),business_card,target_selector)
        try:
            if html_elem is not None:
                self.details[key] = html_elem.text
            else:
                self.details[key] = self.NA
        except Exception as e:
            self.page.log(key+": " + str(e))

        #self.page.log(key + " = " + self.details[key])

    def get_url_from_business_card(self,business_card,key,target_selector):
        html_elem = get_element_from_element(self.page.get(),business_card,target_selector)
        max_wait=2
        start_time=time.time()
        while html_elem is None and time.time() - start_time < max_wait:
            self.page.sleep_for(0.01,0.5)
            html_elem = get_element_from_element(self.page.get(),business_card,target_selector)
        url = get_url_from_element(self.page.get(),html_elem)
        max_wait=2
        start_time=time.time()
        while url is None and time.time() - start_time < max_wait:
            #self.page.log("url is none")
            self.page.sleep_for(0.01,0.5)
            url = get_url_from_element(self.page.get(),html_elem)
        if url is not None:
            self.details[key] = url
        else:
            self.details[key]=self.NA
        #self.page.log(key + " = " + self.details[key])

    def click_to_obj(self, obj):
        max_wait=2
        start_time= time.time()
        while time.time() - start_time < max_wait:
            try:
                remove_element_by_selector(self.page.get(),self.target_elements['overlay'])
                obj.click()
            except:
                pass    
        
    def get_obj_with_wait(self, css_selector, max_wait):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as CON
        from selenium.webdriver.common.by import By
        try:
            element = WebDriverWait(self.page.get(), max_wait).until(CON.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            return element
        except:
            return None


    def click_to_obj_with_driver(self,target_selector:str, max_wait):
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as CON
            from selenium.webdriver.common.by import By
            wait = WebDriverWait(self.page.get(), max_wait)
            next_button = wait.until(CON.visibility_of_element_located((By.CSS_SELECTOR,target_selector)))
            next_button.click()
            time.sleep(5)
            return True
        except:
            return False

    def show_houres(self, business_card):
        show_houres = get_element_from_element(self.page.get(),business_card,self.target_elements['houres_arrow_css'])
        max_wait=2
        start_time=time.time()
        while show_houres is None and time.time() - start_time < max_wait:
            #self.page.log("show_houres is none")
            self.page.sleep_for(0.01,0.5)
            show_houres = get_element_from_element(self.page.get(),business_card,self.target_elements['houres_arrow_css'])
        try:
            if show_houres is not None:
                self.click_to_obj(show_houres)
                return True
            return False
        except Exception as e:
            self.page.log("cant click to show_houres " + str(e))
            return show_houres(business_card,start_time,max_wait)

    def save_houres(self,business_card):
        if not self.show_houres(business_card):
            self.details['houres']=self.NA
            return
        houres_table = get_element_from_element(self.page.get(),business_card,self.target_elements['houres_table_css'])
        max_wait=2
        start_time = time.time()
        while houres_table is None:
            if time.time() - start_time < max_wait:
                self.details['houres']=self.NA
                return
            #self.page.log("houres_table is none")
            self.page.sleep_for(0.01,0.5)
            houres_table = get_element_from_element(self.page.get(),business_card,self.target_elements['houres_table_css'])
        tr="tr"
        rows =get_elements_from_element(self.page.get(),houres_table, tr)
        max_wait=2
        start_time = time.time()
        while rows is None:
            if time.time() - start_time < max_wait:
                self.details['houres']=self.NA
                return
            #self.page.log("rows is none")
            self.page.sleep_for(0.01,0.5)
            rows =get_elements_from_element(self.page.get(),houres_table, tr)

        data = []
        td="td"
        for row in rows:#Loop through each row and extract the data
            cells = get_elements_from_element(self.page.get(),row,td)
            max_wait=2
            start_time = time.time()
            while cells is None:
                #self.page.log("cells is none")
                if time.time() - start_time < max_wait:
                    self.details['houres']=self.NA
                    return
                self.page.sleep_for(0.01,0.5)
                cells = get_elements_from_element(self.page.get(),row,td)
            try:
                data.append(cells[0].text + "\t" + cells[1].text)
            except:
                pass 

        data = list(set(data))#Remove duplicates from the data list
        result = ",".join(data)
        self.details['houres']=result
        #self.page.log('houres = '+ self.details['houres'])

    def votes_to_number(self, votes:str):
        try:
            no_symbols = votes.replace(",", "").replace("(", "").replace(")", "")
            if no_symbols.endswith("k"):
                return str(int(float(no_symbols[:-1]) * 1000))
            elif no_symbols.isdigit():
                return str(int(no_symbols))
            else:
                return votes
        except:
            return votes

    def get_info_with_wait(self,business_card,key,target_selector,max_time):
        html_elem = get_element_from_element(self.page.get(),business_card,target_selector)
        max_wait=max_time
        start_time = time.time()
        while html_elem is None and time.time() - start_time < max_wait:
            self.page.sleep_for(0.01,0.5)
            html_elem = get_element_from_element(self.page.get(),business_card,target_selector)
        self.page.sleep_for(0.01,0.1)
        try:
            html_text=html_elem.text
            if key =="votes":
                html_text=self.votes_to_number(html_text)
            if key in self.details and self.details[key]==self.NA:
                self.details[key] = html_text
        except:
            if key in self.details:
                self.details[key] = self.NA

        #self.page.log(key + " = " + self.details[key])
    def get_website(self,business_card):
        website_elem = get_element_from_element(self.page.get(),business_card,self.target_elements['website_css'])
        max_wait=2
        start_time = time.time()
        while website_elem is None and time.time() - start_time < max_wait:
            self.page.sleep_for(0.01,0.5)
            website_elem = get_element_from_element(self.page.get(),business_card,self.target_elements['website_css'])
        if website_elem:
            website_url=get_url_from_element(self.page.get(), website_elem)
            max_wait=1
            start_time = time.time()
            while website_url is None and time.time() - start_time < max_wait:
                self.page.sleep_for(0.01,0.2)
                website_url=get_url_from_element(self.page.get(), website_elem)
            if website_url:
                return website_url
            else:
                return self.NA
        else:
            return self.NA


    def get_all_social_elements(self,business_card):
        social_elements = get_elements_from_element(self.page.get(),business_card,self.target_elements['social_elements'])
        max_wait=2
        start_time=time.time()
        while social_elements == None and time.time() - start_time < max_wait:
            self.page.sleep_for(0.01,0.5)
            social_elements = get_elements_from_element(self.page.get(),business_card,self.target_elements['social_elements'])
        return social_elements

    def get_social_links(self,business_card,target_list):#get a panel contains all social media available
        social_elements = self.get_all_social_elements(business_card)
        for elem in social_elements:
            link = get_url_from_element(self.page.get(), elem)
            social_name_obj=get_element_from_element(self.page.get(),elem,self.target_elements['social_name'])
            if link != None and social_name_obj != None:
                try:
                    social_name=social_name_obj.text
                    for curr_name in target_list:
                        if curr_name==social_name:
                            if curr_name in self.details and self.details[curr_name]==self.NA:
                                self.details[curr_name]=link
                except:
                    pass
    
    def save_website(self,business_card):
        web_url = self.get_website(business_card)
        self.details['website']=web_url

        
    def save_business_details(self):
        business_card=self.get_business_card()
        self.get_info_with_wait(business_card,'title',self.target_elements['title_css'],2)
        self.get_info_with_wait(business_card,'votes',self.target_elements['votes_css'],2)
        self.get_info_with_wait(business_card,'description',self.target_elements['description_css'],2)
        self.save_website(business_card)
        self.get_info_with_wait(business_card,'address', self.target_elements['address_css'],2)#save the address
        self.save_houres(business_card)
        self.get_info_with_wait(business_card,'phone', self.target_elements['phone_css'],2)#save the phone
        self.get_info_with_wait(business_card,'merchant_description', self.target_elements['merchant_description'],1)#save the merchant description if available before 5 seconds ends.
        self.get_social_links(business_card,["Facebook", "Instagram", "LinkedIn", "Twitter"])

    def scrape_all_pages(self):
        while True:
            all_map_objs = self.get_all_map_objects()
            all_map_objs_len = len(all_map_objs)
            rows_added = 0
            for map_obj in all_map_objs:
                self.click_to_obj(map_obj)
                self.page.sleep_for(0.70,1)
                self.save_business_details()

                #dont repeat a row with a value according to the saving strategy.
                curr_strategy=self.saving_strategy.get_name()
                if curr_strategy =="excel" or curr_strategy=="xml":
                    self.saving_strategy.save(self.details,donot_repeat='title')
                else:
                    self.saving_strategy.save(self.details,donot_repeat=9)

                self.clear_data()
                rows_added += 1
                percentage = (rows_added / all_map_objs_len) * 100 #Calculate the percentage
                self.page.clear_terminal()
                self.saving_strategy.notify(f'Progress: {rows_added} of {all_map_objs_len} rows added ({percentage:.2f}%)')
            
           
            next_btn = self.get_obj_with_wait(self.target_elements['next_page_btn'],10)
            if next_btn:
                next_url = next_btn.get_attribute("href")
                self.page.go_to_url(next_url)
                self.page.sleep_for(4,7)
                #time.sleep(5)#wait for the next page to load.
            else:
                break
        self.saving_strategy.notify(self.name + ": "+ "Data collection complete, " + str(all_map_objs_len) + " pages.")

    #override
    def scrape(self,keyword=''):
        self.curr_keyword=keyword#store the curr kwd.
        self.page.go_to_url(self.url+self.fix_keyword(keyword))
        self.scrape_all_pages()  
    