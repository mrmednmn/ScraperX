#excel file columns and headings used to form the excel file head.
import sys
sys.dont_write_bytecode = True

class ExcelHeader:
    def __init__(self):
        self.columns = []
        self.headings= []

    #def set_columns(self, columns):
        #self.columns=columns

    def set_headings(self, headings):
        self.headings=headings
    



