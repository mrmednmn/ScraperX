#excel csv file headings
import sys
sys.dont_write_bytecode = True

class CsvHeader:
    def __init__(self):
        self.headings= []

    def set_headings(self, headings):
        self.headings=headings

    def get_headings(self):
        return self.headings
