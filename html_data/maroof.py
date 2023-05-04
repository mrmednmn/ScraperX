#target css selectors or xpaths for maroof
import sys
sys.dont_write_bytecode = True

class MaroofHtml:
    def __init__(self):
        self.copy={}#dict for html css selectors or xpaths
        self.copy['search_input']='.search-input'
        self.copy['search_btn']='.search-btn'
        self.copy['options']='.search-block.position-relative.mb-4'
        self.copy['golden']='#inputCr'
        self.copy['silver']='#inputFl'
        self.copy['no_data']='.noData-title'
        self.copy['search_card']='.storeCard'
        self.copy['card_title']='.storeCard-title'
        self.copy['next_btn']='a.page-link[aria-label="Next"]'
        self.copy['work_data']='.col-12.mt-3'
        self.copy['info_details']='.info-details'
        self.copy['media_card']='.media-info'
        self.copy['media_text']='.media-header'
        self.copy['store_number']='.store-number>span:last-child'
        self.copy['address_info']='.address-details span:nth-child(1)'
        self.copy['address_info1']='.address-details span:nth-child(2)'
        self.copy['votes']='.rating-text'
        self.copy['total_votes']='.align-items-lg-end > div:nth-child(1) > div:nth-child(2) > span'

    def get(self):
        return self.copy

