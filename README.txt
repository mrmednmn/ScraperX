Dear users,

Thank you for choosing to use my open source project! If you have found it useful, please consider supporting its ongoing development by making a donation on PayPal. Your support will help me to continue improving and maintaining this project for the benefit of the wider community.

To donate, simply visit your PayPal account and send your donation to mohamednmn28105@gmail.com. Any amount, no matter how small, is greatly appreciated.

Thank you again for your support!


This project is a web scraping tool that allows users to collect data from Google Maps and Maroof Platform with ease. 
Users can effortlessly save the data in various file formats such as XLS, CSV, or XML by simply selecting the platform of their choice and specifying the folder that holds the data files.
Additionally, users can specify the data file name and add any desired keywords for their search.
For instance, in Google Maps, users can search for restaurants in the USA by typing in relevant keywords.
Users can also schedule multiple scrapers to run at different times, This project provides a streamlined solution for anyone seeking to efficiently collect data from online platforms.


To use this tool, simply follow these steps:

*If you are using Git, you can easily clone this project by running the following command in your cmd:
git clone https://github.com/amzapis/ScraperX.git scraperX


Alternatively, you can download the project as a ZIP file by clicking the green "Code" button on GitHub and selecting "Download ZIP". After downloading and extracting the ZIP file, you can rename the main folder to "scraperX".



1.Update google chrome go to Help->About Google Chrome to update your chrome browser, the default version used is 112, to manualy change the chrome version: in gui/web/view.py change return 112 to return YOUR_CHEOME_VERSION_HERE

2.Download and install python 3.11 https://www.python.org/ , make sure to add python to path during instalation.

3.run ScraperX.exe

OR

3.Go to the main folder with cmd, (admin mode preferred, open cmd with admin mode and write cd MAIN_FOLDER_PATH_HERE).

IN CMD:

4.write "python.exe -m pip install --upgrade pip"

5.write "pip install -r requirements.txt".

6. To make sure the packaged is up to date write "pip install -r requirements.txt --upgrade".

7.after packages installed, write "cls" to clean the cmd.

8.write "main.py" or "python main.py" to run the tool.


A few important notes for users of this program:

1.If you need to read data from an Excel, XML, or CSV file while the program is actively working with it, it is strongly recommended that you make a copy of the original file and use the copy instead. This will help to prevent any accidental data loss or corruption that could result from simultaneous access to the same file.

2.If you prefer to run this program in "headless" mode, which hides the browser window, you can do so by modifying the code in the gui/web/view.py file. To hide the browser window, open view.py in a text editor like Notepad++ and change the line self.is_hidden = False to self.is_hidden = True. Please note that this setting is currently set to False by default to demonstrate how the program works.

 
