#Developer: Mohamed Naamane
#Contact: naamanemohamedtheprogrammer@gmail.com
"""
This project is a web scraping tool that allows users to collect data from Google Maps and Maroof Platform with ease. 
Users can effortlessly save the data in various file formats such as XLS, CSV, or XML by simply selecting the platform of their choice and specifying the folder that holds the data files.
Additionally, users can specify the data file name and add any desired keywords for their search.
For instance, in Google Maps, users can search for restaurants in the USA by typing in relevant keywords.
Users can also schedule multiple scrapers to run at different times, This project provides a streamlined solution for anyone seeking to efficiently collect data from online platforms.
"""
import sys
sys.dont_write_bytecode = True
from system_health.cleaner import TempFileManager
from gui.web.view import start_gui
from system_health.package_installer import try_fix_requiremets           

if __name__ == "__main__":
    TempFileManager().clear_temp_folder()
    try_fix_requiremets()
    start_gui()
    




