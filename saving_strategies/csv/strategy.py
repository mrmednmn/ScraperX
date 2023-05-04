import sys
sys.dont_write_bytecode = True
from saving_strategies.base import SavingStrategy
from saving_strategies.csv.header import CsvHeader
import csv
import os

class CsvSavingStrategy(SavingStrategy):
    def __init__(self,folder_name:str,file_name:str,logger):
        self.logger=logger
        self.NA="N/A"
        self.name="csv"
        self.create_folder(self.name)
        self.path_head = os.path.join(os.getcwd(),self.name,folder_name)
        self.create_folder(self.path_head)
        self.file_name=os.path.join(self.path_head, file_name+".csv")
        self.logger("Save Location: " + self.file_name)  
        self.header = CsvHeader()

    #override
    def get_name(self):
        return self.name

    #override
    def notify(self,data):
        self.logger(data)

    def log(self,msg):
        print(msg,end='\n')

    def create_folder(self, folder_name: str):
        folder_path = os.path.join(os.getcwd(), folder_name)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
    
    def init_headings(self):
        with open(self.file_name, 'a+', newline='',encoding='utf-16') as csv_file:
            #Check if the file is empty
            csv_file.seek(0)
            is_empty = csv_file.read(1) == ''
            if is_empty:
                writer = csv.writer(csv_file,delimiter='\t')
                writer.writerow(self.header.headings)
                
               
    def init_csv(self, headings):#create the csv header from a list headings
        self.header.set_headings(headings)
        self.init_headings()

    def add_row(self, data, donot_repeat):
        #Open the file in read and write mode
        with open(self.file_name, 'r+', newline='', encoding='utf-16') as target_file:
            handler = csv.reader(target_file,delimiter='\t')
            #Check if the title already exists in the file
            if any(row[donot_repeat] == data[donot_repeat] for row in handler):
                self.notify(f"Skipping row since value '{data['{donot_repeat}']}' already exists")
                return
            #Append the data to the file
            handler = csv.writer(target_file,delimiter='\t')
            handler.writerow(data)
             
    def init_csv(self, headings):
        self.header.set_headings(headings)
        self.init_headings()

    #def clear_data(self,data):
        #for k in data:
            #data[k]=self.NA

    #override
    def save(self,data,donot_repeat):
        data = {key: data[key] for key in sorted(data)}
        data_values = list(data.values())
        self.add_row(data_values,donot_repeat)
        #self.clear_data(data)