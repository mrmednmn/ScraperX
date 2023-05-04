import sys
sys.dont_write_bytecode = True
from os import getcwd
import json
from os import system
from os import name


def clear_terminal():
    system('cls' if name=='nt' else 'clear')

#setup
def scraperx_setup():
    req_file= open(getcwd()+"\\requirements.txt",'r')
    all_pkgs=req_file.readlines()
    for curr_pkg in all_pkgs:
        system("pip install "+curr_pkg if name=='nt' else "pip3 install "+curr_pkg)
        clear_terminal()
    req_file.close()


#fix_requiremets
def fix_requiremets():
    clear_terminal()
    print("Checking for ScraperX requirements...")
    json_record={}
    conf_file = open(getcwd()+"\\config.json",'r+')
    
    for record in conf_file:
        json_record = json.loads(record)
    conf_file.seek(0)
    if json_record["requ_installed"]=="False":
        scraperx_setup()
        json_record["requ_installed"]="True"
        json.dump(json_record,conf_file)
        conf_file.truncate()

    conf_file.close()
    
    #sys.path.insert(0, getcwd())
    print("OK.")

def try_fix_requiremets():
    try:
        fix_requiremets()
    except Exception as ex:
        print(str(ex),end='\n')

