import sys
sys.dont_write_bytecode = True
from scrapers.base import Scraper
from saving_strategies.base import SavingStrategy
from html_data.maroof import MaroofHtml
from scraper_options.maroof import MaroofOptions
from jlib.js_functions import is_page_loaded
from jlib.js_functions import get_elements_by_css_selector 
from jlib.js_functions import get_element_by_css_selector 
from jlib.js_functions import send_string_to_element_char_by_char as send_str
from jlib.js_functions import get_element_from_element
from jlib.js_functions import get_url_from_element
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as CON
import time

class MaroofScraper(Scraper):
    def __init__(self, page,saving_strategy:SavingStrategy, options:MaroofOptions):
        self.page=page
        self.saving_strategy=saving_strategy
        self.target_elements=MaroofHtml().get()
        self.url='https://maroof.sa/businesses'
        self.NA='N/A'
        self.curr_keyword=self.NA
        self.details={}
        self.visited_card={}
        self.curr_page=0
        self.NO_RESULTS=-1
        self.END_RESULTS=-2
        self.rows_added=0
        self.percentage=0
        self.init_details()
        self.name="Maroof Scraper"
        self.options = options

    def init_details(self):
        self.details["إنستقرام"] = self.NA
        self.details["الاسم التجاري"] = self.NA
        self.details["بريد إلكتروني"] = self.NA
        self.details["بيانات العنوان"] = self.NA
        self.details["تصنيف العمل"] = self.NA
        self.details["تليجرام"] = self.NA
        self.details["تويتر"] = self.NA
        self.details["خدمة عملاء"] = self.NA
        self.details["رقم السجل التجاري"] = self.NA
        self.details["رقم معروف"] = self.NA
        self.details["فيسبوك"] = self.NA
        self.details["موقع ويب"] = self.NA
        self.details["نبذه عن العمل"] = self.NA
        self.details["نوع العمل الرئيسي"] = self.NA
        self.details["هاتف"] = self.NA
        self.details["واتس اب"] = self.NA
        self.details['التقييمات']=self.NA
        self.details['إجمالي التقييمات']=self.NA

    def clear_data(self):
        for k in self.details:
            self.details[k]=self.NA

    def is_next_btn_available(self):
        try:
            wait = WebDriverWait(self.page.get(), 5)
            obj = wait.until(CON.element_to_be_clickable((By.CSS_SELECTOR,self.target_elements["next_btn"])))
            if obj:
                return True
            return False
        except: 
            return False
        


    def click_to_obj_with_driver(self,target_selector:str,max_wait):
        try:
            wait = WebDriverWait(self.page.get(), max_wait)
            obj = wait.until(CON.element_to_be_clickable((By.CSS_SELECTOR,target_selector)))
            obj.click()
            return True
        except:
            return False

    def select_text_from_dropdown(self,placeholder, option_text):
        try:
            wait = WebDriverWait(self.page.get(), 10)
            dropdown = wait.until(CON.element_to_be_clickable((By.XPATH, f'//ng-select[contains(@placeholder, "{placeholder}")]')))
            dropdown.click()
            option = wait.until(CON.element_to_be_clickable((By.XPATH, f'//span[contains(text(), "{option_text}")]')))
            option.click()
        except:
            pass

    def get_obj_with_wait(self, css_selector, max_wait):
        try:
            element = WebDriverWait(self.page.get(), max_wait).until(CON.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            return element
        except:
            return None


    #def get_obj_with_wait(self, css_selector, max_wait):
        #target_element = get_element_by_css_selector(self.page.get(),css_selector)
        #start_time=time.time()
        #while target_element is None and time.time() - start_time < max_wait:
            #self.page.sleep_for(0.01,0.3)
            #target_element = get_element_by_css_selector(self.page.get(),css_selector)
        #return target_element

    def get_objs_with_wait(self, css_selector, max_wait):
        try:
            elements = WebDriverWait(self.page.get(), max_wait).until(CON.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
            return elements
        except:
            return None

    #def get_objs_with_wait(self, css_selector,max_wait):
        #driver=self.page.get()
        #target_elements=driver.find_elements_by_css_selector(css_selector)
        #target_elements = get_elements_by_css_selector(self.page.get(),css_selector)
        #start_time=time.time()
        #while target_elements is None and time.time() - start_time < max_wait:
            #self.page.sleep_for(0.01,0.3)
            #target_elements = get_element_by_css_selector(self.page.get(),css_selector)
            #target_elements=self.page.get().find_elements_by_css_selector(css_selector)
        #return target_elements

    def check_golden(self):
        self.click_to_obj_with_driver(self.target_elements['golden'],30)
        
    def check_silver(self):
        self.click_to_obj_with_driver(self.target_elements['silver'],30)

    def check_gold_or_silver(self, choice):
        if choice == "1":
            self.check_golden()
        else:
            self.check_silver()

    def select_from_work_class(self,option):
        placeholder="اختر تصنيف العمل الرئيسي"
        self.select_text_from_dropdown(placeholder,option)

    def select_from_second_work_class(self,option):
        placeholder="اختر تصنيف العمل الفرعي"
        try:
            self.select_text_from_dropdown(placeholder,option)
        except:
            pass

    def select_from_country(self,option):
        placeholder="اختر المنطقة"
        self.select_text_from_dropdown(placeholder,option)

    def select_from_city(self,option):
        placeholder="اختر المدينة"
        self.select_text_from_dropdown(placeholder,option)

    def is_search_resutls_available(self):#check if search results is available
        data_found = self.get_obj_with_wait(self.target_elements['no_data'],2)
        if data_found is None:
            return True
        return False

    def get_child_element(self,parent_elem, child_css):
        child_elem = get_element_from_element(self.page.get(), parent_elem, child_css)
        max_wait=2
        start_time=time.time()
        while child_elem is None and time.time() - start_time < max_wait:
            self.page.sleep_for(0.01,0.5)
            child_elem = get_element_from_element(self.page.get(), parent_elem, child_css)
        return child_elem

    #def get_child_elements(self,parent_elem, child_css):
        #child_elems = get_elements_from_element(self.page.get(), parent_elem, child_css)
        #max_wait=2
        #start_time=time.time()
        #while child_elems is None and time.time() - start_time < max_wait:
            #self.page.sleep_for(0.01,0.5)
            #child_elems = get_elements_from_element(self.page.get(), parent_elem, child_css)
        #return child_elems

    #get all search results 
    def get_card_info(self,card):
        try:
            card_title = self.get_child_element(card, self.target_elements['card_title'])
            if card_title is None:
                return False #invalid card
            if card_title.text in self.visited_card:
                return False #visited card
            self.visited_card[card_title.text]=True
            card.click()
            return True #new card handled
        except Exception as e:
            self.page.log("cant click to card " + str(e))
            return False
 
          
    def put_keyword(self, keyword):
        search_input = self.get_obj_with_wait(self.target_elements['search_input'],5)
        send_str(self.page.get(), search_input, keyword)
        self.click_to_obj_with_driver(self.target_elements['search_btn'],30)
        self.page.sleep_for(3,6)

    def select_maroof_options(self):
        if self.options.check_box !="":
            self.check_gold_or_silver(self.options.check_box)
            self.page.sleep_for(3,6)

        if self.options.main_work!="":
            self.select_from_work_class(self.options.main_work)
            self.page.sleep_for(3,6)

        if self.options.second_work !="":
            self.select_from_second_work_class(self.options.second_work)
            self.page.sleep_for(3,6)

        if self.options.country != "":
            self.select_from_country(self.options.country)
            self.page.sleep_for(3,6)

        if self.options.city != "":
            self.select_from_city(self.options.city)
            self.page.sleep_for(3,6)
    
    #get all search results
    def get_all_cards(self):
        all_cards = self.get_objs_with_wait(self.target_elements['search_card'],10)
        return all_cards

    def init_scraping(self, keyword):
        while not is_page_loaded(self.page.get()):
            pass

        if keyword!='':
            self.put_keyword(keyword)
        
        self.select_maroof_options()

        if self.curr_page>0:#go the curr page because the platform return to page1 after move back.
            for i in range(0,self.curr_page):
                is_btn_clicked = self.click_to_obj_with_driver(self.target_elements['next_btn'],20)
                if is_btn_clicked == False:
                    return self.END_RESULTS
                self.page.sleep_for(3,6)                    

        
        
        if self.is_search_resutls_available():
            return self.get_all_cards()
        return self.NO_RESULTS
           
    #save info to details
    def save_info_with_wait(self,key,target_selector,max_time):
        try:
            html_elem = get_element_by_css_selector(self.page.get(),target_selector)
            max_wait=max_time
            start_time = time.time()
            while html_elem is None and time.time() - start_time < max_wait:
                self.page.sleep_for(0.01,0.5)
                html_elem = get_element_by_css_selector(self.page.get(),target_selector)
        
            try:
                html_text=html_elem.text
                if key in self.details:
                    self.details[key] = html_text
            except:
                if key in self.details:
                    self.details[key] = self.NA
        except:
            pass

    def save_pairs(self,css_selector):
        try:
            pairs = self.get_objs_with_wait(css_selector,5)
            for pair in pairs:
                key_element = self.get_child_element(pair,".data-key")
                value_element = self.get_child_element(pair,".data-value")
                if key_element is not None and value_element is not None:
                    key_text = key_element.text
                    value_text=value_element.text
                    if key_text in self.details:
                        self.details[key_text]=value_text
        except:
            pass

    def get_url_from_obj(self, obj,max_wait):
        url_txt = get_url_from_element(self.page.get(),obj)
        start_time=time.time()
        while url_txt is None and time.time() - start_time < max_wait:
            self.page.sleep_for(0.01,0.4)
            url_txt = get_url_from_element(self.page.get(),obj)
        return url_txt

    def get_social_media_links(self):
        try:
            social_cards = self.get_objs_with_wait(self.target_elements['media_card'],5)
            for social_card in social_cards:
                header = self.get_child_element(social_card, self.target_elements['media_text'])
                url = self.get_url_from_obj(social_card, 2)
                if header is not None and  url is not None:
                    header_text = header.text
                    if header_text in self.details:
                        self.details[header_text]=url
        except:
            pass

    def save_address(self):
        try:
            details_key="بيانات العنوان"
            add1 = self.get_obj_with_wait(self.target_elements['address_info'],2)
            add2=self.get_obj_with_wait(self.target_elements['address_info1'],2)
        
            if add1 is not None and add2 is not None:
                add1_text = add1.text
                add2_text= add2.text
                total_text = add1_text+" " + add2_text
                self.details[details_key]=total_text
            elif add1 is not None:
                add1_text = add1.text
                self.details[details_key]=add1_text
            elif add2 is not None:
                add2_text = add2.text
                self.details[details_key]=add1_text
            else:
                self.details[details_key]=self.NA
        except:
            pass

    def save_votes(self):
        try:
            votes_key='التقييمات'
            votes_elem = self.get_obj_with_wait(self.target_elements['votes'],2)
            if votes_elem is not None:
                votes_txt = votes_elem.text
                self.details[votes_key]=votes_txt
            else:
                self.details[votes_key]=self.NA
        except:
            pass

    def save_total_votes(self):
        try:
            total_votes_key='إجمالي التقييمات'
            total_votes = self.get_obj_with_wait(self.target_elements['total_votes'],2)
            if total_votes is not None:
                total_votes_txt = total_votes.text
                total_votes_txt=total_votes_txt.replace(total_votes_key, "")
                self.details[total_votes_key]=total_votes_txt
            else:
                self.details[total_votes_key]=self.NA
        except:
            pass


    def scrape_all_pages(self,keyword,all_cards):
        if all_cards == self.NO_RESULTS or all_cards == self.END_RESULTS or all_cards is None:
            return all_cards
        
        all_cards_len = len(all_cards)

        visited_cards_len = len(self.visited_card)
        
        
        if visited_cards_len>0:
            if visited_cards_len>=all_cards_len:
                is_btn_clickable = self.is_next_btn_available()
                if not is_btn_clickable:
                    return self.END_RESULTS
                self.curr_page+=1
                self.rows_added=0
                self.percentage=0
                self.visited_card.clear()
                

        for card in all_cards:
            if not self.get_card_info(card):# if this card is visited, just skip.
                continue
            self.page.sleep_for(3,6)
            #save the data to self.details dict.
            self.save_pairs(self.target_elements['work_data'])
            self.save_pairs(self.target_elements['info_details'])#save the info details to self.details dict
            self.get_social_media_links()#social media links.
            self.save_info_with_wait("رقم معروف",self.target_elements['store_number'],2)#save store number
            #self.save_info_with_wait("بيانات العنوان",self.target_elements['address_info'],2)
            self.save_address()
            self.save_votes()
            self.save_total_votes()
            #self.details = {key: self.details[key] for key in sorted(self.details)}
            curr_strategy=self.saving_strategy.get_name()
            if curr_strategy =="excel" or curr_strategy=="xml":#dont repeat a value accoring to the saving strategy.
                self.saving_strategy.save(self.details,donot_repeat="بريد إلكتروني")
            else:
                self.saving_strategy.save(self.details,donot_repeat=4)
            self.clear_data()
            self.rows_added += 1
            self.percentage = (self.rows_added / all_cards_len) * 100 #Calculate the percentage
            #self.page.clear_terminal()
            self.saving_strategy.notify(f'Progress: {self.rows_added} of {all_cards_len} rows added ({self.percentage:.2f}%)')
            self.page.go_back()
            self.page.sleep_for(3,6)
            break
        all_cards= self.init_scraping(keyword)
        return self.scrape_all_pages(keyword,all_cards)
                 
    #override
    def scrape(self,keyword=''):
        self.curr_keyword=keyword
        self.page.go_to_url(self.url)
        all_cards= self.init_scraping(keyword)
        scrape_result = self.scrape_all_pages(keyword,all_cards)
        if scrape_result is self.NO_RESULTS:
            self.saving_strategy.notify(self.name+ ": No data available!")
        else:
            self.saving_strategy.notify(self.name+ ": " + str(scrape_result) + " end search.")  
