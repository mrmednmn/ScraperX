import sys
sys.dont_write_bytecode = True
from saving_strategies.base import SavingStrategy
from saving_strategies.xml.header import XmlHeader
import os
import xml.etree.ElementTree as ET

class XmlSavingStrategy(SavingStrategy):
    def __init__(self,folder_name:str,file_name:str, logger):
        self.logger=logger
        self.name="xml"
        self.create_folder(self.name)
        self.path_head = os.path.join(os.getcwd(),self.name,folder_name)
        self.create_folder(self.path_head)
        self.file_name=os.path.join(self.path_head, file_name+".xml")
        self.notify("Save Location: " + self.file_name)
        self.header = XmlHeader()
        self.NA="N/A"
        self.root='header'

    #override
    def get_name(self):
        return self.name

    #override
    def notify(self,data):
        self.logger(data)


    def init_xml_file(self, headings):
        self.header.set_headings(headings)
        if not os.path.isfile(self.file_name):
            #Create the root element and add it to the XML tree
            root = ET.Element('data')
            tree = ET.ElementTree(root)
            tree.write(self.file_name, encoding='utf-16', xml_declaration=True)


    def create_folder(self, folder_name: str):
        folder_path = os.path.join(os.getcwd(), folder_name)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

    def log(self,msg):
        print(msg,end='\n')

    #def clear_data(self,data):
        #for k in data:
            #data[k]=self.NA
    

    def add_row(self,data, do_not_repeat):
        #Parse the XML file
        parser = ET.XMLParser(encoding='utf-16')
        tree = ET.parse(self.file_name, parser=parser)
        root = tree.getroot()

        for elem in root.findall('.//{}'.format(do_not_repeat)):
            if elem.text == data[do_not_repeat]:
                self.notify("row already exists, ignore..")
                return False

        #Check if a row with the same key already exists
        #key_val = data[do_not_repeat]
        #for row in root.findall('row'):
            #if row.find(do_not_repeat).text == key_val:
                #self.notify("row already exists, ignore..")
                #return

       # Key does not exist in the XML file, append the dictionary
        elem = ET.Element('data')
        for k, v in data.items():
            subelem = ET.SubElement(elem, k)
            subelem.text = v
        root.append(elem)
        tree = ET.ElementTree(root)
        #Write the XML tree to the file
        tree.write(self.file_name, encoding='utf-16', xml_declaration=True)
        
    #override
    def save(self,data,donot_repeat):
        data = {key: data[key] for key in sorted(data)}
        self.add_row(data,donot_repeat)

