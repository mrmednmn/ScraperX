import sys
sys.dont_write_bytecode = True
from tempfile import gettempdir
from shutil import rmtree
from os import makedirs

class TempFileManager:
    def __init__(self):
        self.temp_dir=gettempdir()

    def clear_temp_folder(self):
        try:
            rmtree(self.temp_dir)
            makedirs(self.temp_dir)
        except:
            pass




