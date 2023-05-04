#target css selectors or xpaths for google map
import sys
sys.dont_write_bytecode = True

class GoogleMapHtml:
    def __init__(self):
        self.copy={}#dict for html css selectors or xpaths
        self.copy['map_objects_css']='div.rllt__details'
        self.copy['business_card_css']='.xpdopen'
        self.copy['next_page_btn']='#pnnext'
        self.copy['title_css']='*[data-attrid*="title"] span:last-child'
        self.copy['votes_css']='.RDApEe.YrbPuc'
        self.copy['description_css']='.YhemCb:last-child'
        self.copy['website_css']='.hBPSMc.qDBO2c' #'.dHS6jb'
        self.copy['address_css']='.LrzXr'
        self.copy['houres_arrow_css']='.BTP3Ac'
        self.copy['houres_table_css']='.WgFkxc>tbody'
        self.copy['phone_css']='span.LrzXr:nth-child(1) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1)'
        self.copy['merchant_description']='div.wDYxhc:nth-child(8) > c-wiz:nth-child(1) > div:nth-child(1) > div:nth-child(2)'
        self.copy['overlay']='.rlfl__loading-overlay'
        self.copy['curr_index']='.YyVfkd > span:nth-child(1)'
        self.copy['social_elements']='.fl.w23JUc.ap3N9d'
        self.copy['social_name']='.CtCigf'

    def get(self):
        return self.copy